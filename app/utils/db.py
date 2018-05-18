from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.models import Role, User
from app.utils.auth import hash_password

from . import log
from ..config import config

LOG = log.get_logger()


def get_engine(uri):
    """
    Create the SQLAlchemy database engine
    """
    LOG.info('Connecting to database')
    options = {
        "pool_recycle": 3600,
        "pool_size": 10,
        "pool_timeout": 30,
        "max_overflow": 30,
        "echo": config.DB_ECHO,
        "execution_options": {
            'autocommit': config.DB_AUTOCOMMIT
        }
    }
    return create_engine(uri, **options)

db_session = scoped_session(sessionmaker())
engine = get_engine(config.DATABASE_URL)


def load_roles(session):
    """
    Preload the initial user roles if they do not exist
    """
    count_roles = session.query(Role.id).count()
    if count_roles == 0:
        roles = [('Member', 'member'), ('Administrator', 'admin'), ('Supervisor', 'super')]
        rid = 1
        for name, code in roles:
            r = Role(id=rid, name=name, code=code)
            session.add(r)
            rid = rid + 1
        session.flush()
        session.commit()


def load_admin_user(session):
    """
    Load the initial admin user if it doesn't exist.
    """
    count_admin = session.query(User).join(Role, User.role==Role.id).filter(Role.code=='admin').count()
    if count_admin == 0:
        role_id = session.query(Role.id).filter_by(code='admin').one()
        u = User(
            fn = 'Admin',
            ln = 'User',
            email = 'admin@company.com',
            role = role_id,
            password = hash_password('admin')
        )
        session.add(u)
        session.flush()
        session.commit()


def init_session():
    """
    Initialize the database session, create tables if they do not exist,
    and load any initial data if not present.
    """
    db_session.configure(bind=engine)
    from ..models import Base
    Base.metadata.create_all(engine)
    load_roles(db_session)
    load_admin_user(db_session)

