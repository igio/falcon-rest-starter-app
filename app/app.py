import falcon
from .utils import log
from .utils.db import db_session, init_session

# Importing models
from .api import base
from .api.v1 import user

# Importing routing middleware
from .middleware.db import DatabaseSessionManager
from .middleware.auth import AuthenticatedRoute

# Log application startup
LOG = log.get_logger()
LOG.info('Starting API')

# Initialize database session and start the application
init_session()
middleware = [DatabaseSessionManager(db_session), AuthenticatedRoute()]
api = application = falcon.API(middleware=middleware)

# Add a "Sink" route for any unmatched routes.
sink = base.SinkAdapter()
api.add_sink(sink, '/')

# Added resource routes
api.add_route('/', base.BaseResource())
api.add_route('/v1/users', user.Collection())
api.add_route('/v1/users/{user_id}', user.Item())
api.add_route('/v1/users/self/login', user.Login())
