from app.utils.db import db_session
from app.models import Role, RoleSchema


def get_roles():
    """
    Retrieve the available user roles.
    :return: dict
    """
    roles = db_session.query(Role).all()
    return {r.code: r.id for r in roles}