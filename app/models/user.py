from . import IdMixin, TimestampMixin, Base
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from marshmallow import Schema, fields, validates, ValidationError, validates_schema

"""
Defines user-related tables and schemas.
"""


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True, error_messages={'required': 'Email address is required.'})
    fn = fields.Str(required=True, error_messages={'required': 'First name is required.'})
    ln = fields.Str(required=True, error_messages={'required': 'Last name is required.'})
    password = fields.Str(required=True, error_messages={'required': 'Password is required.'})
    token = fields.Str(dump_only=True)
    role = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class LoginSchema(Schema):
    email = fields.Email(required=True, error_messages={'required': 'Email address is required.'})
    password = fields.Str(required=True, error_messages={'required': 'Password is required.'})


class User(IdMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, index=True, unique=True)
    fn = Column(String, nullable=False)
    ln = Column(String, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String, default=uuid4())
    active = Column(Boolean, default=True)
    role = Column(Integer, ForeignKey('roles.id'))

    surveys = relationship("Survey")
    blocks = relationship("Block")
    items = relationship('Item')


