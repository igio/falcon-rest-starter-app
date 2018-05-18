import falcon
from app.utils import log
from app.config.config import SECRET_KEY
import jwt

LOG = log.get_logger()


class AuthenticatedRoute(object):
    """
    Middleware used to require authentication for all resources/routes
    except login.
    """
    def process_request(self, req, res, resource=None):
        if req.path not in ['/v1/users/self/login']:
            if req.auth is not None:
                LOG.info('Authentication header present')
                u = jwt.decode(req.auth, SECRET_KEY, algorithms=['HS256'])
                if u:
                   req.context['user'] = u
                else:
                    raise falcon.HTTPUnauthorized('Invalid authorization token.')
            else:
                raise falcon.HTTPUnauthorized('Authorization token is required for this resource.')