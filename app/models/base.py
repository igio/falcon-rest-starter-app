from sqlalchemy import Column, Integer, TIMESTAMP
from sqlalchemy.sql import func

"""
Mixins used to automatically include the id and 
the timestamp columns.
"""


class IdMixin(object):
    id = Column(Integer, primary_key=True, autoincrement=True)


class TimestampMixin(object):
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())