import falcon
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError

from app.utils import log
from app.config import config
import json

LOG = log.get_logger()


class DatabaseSessionManager(object):
    """
    Middleware used to manage the database connection session.
    Make session available to the request context in all resources.
    Raise errors in case something is wrong with database operations.
    Clean session between calls.
    """
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, req, res, resource=None):
        req.context['session'] = self._session_factory

    def process_response(self, req, res, resource=None):
        session = req.context['session']
        if config.DB_AUTOCOMMIT:
            try:
                session.commit()
                self.clean_session(session)
            except SQLAlchemyError as ex:
                session.rollback()
                LOG.error('Database error: ', ex)
                self.clean_session(session)
                res.status = falcon.HTTP_500
                res.body = json.dumps({'Error': True})

    def clean_session(self, session):
        if self._scoped:
            session.remove()
        else:
            session.close()
