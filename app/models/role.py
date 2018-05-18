from . import IdMixin, TimestampMixin, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

"""
Defines the user roles table and schema.
"""


class RoleSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True, error_messages={'required': 'Role name is required.'})
    code = fields.Str(required=True, error_messages={'required': 'Role code is required.'})
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)


class Role(IdMixin, TimestampMixin, Base):
    __tablename__ = 'roles'

    name = Column(String, nullable=False)
    code = Column(String, nullable=False)

    users = relationship('User')
