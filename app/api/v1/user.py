import falcon

from app.utils import log
from app.api.base import BaseOptions
from app.utils.auth import hash_password, verify_password
from uuid import uuid4
from app.models import User, UserSchema, LoginSchema
from app.utils.admin import get_roles
from app.config.config import SECRET_KEY
import json
import jwt

LOG = log.get_logger()


class Collection(BaseOptions):
    """
    Handles /v1/users
    List users; Add new user.
    """
    def on_get(self, req, res):
        session = req.context['session']
        users = session.query(User).all()
        schema = UserSchema()
        out = []
        for u in users:
            out.append(schema.dump(u).data)
        res.status = falcon.HTTP_200
        res.body = self.to_json(out)

    def on_post(self, req, res):
        """
        Create a new user. Will test the data passed to the resource.
        """
        session = req.context['session']
        data = json.loads(req.bounded_stream.read().decode())
        result = UserSchema().load(data)
        if result.errors:
            res.status = falcon.HTTP_BAD_REQUEST
            res.body = self.to_json({'errors':result.errors})
        else:
            roles = get_roles()
            user = User(
                email=data['email'],
                fn=data['fn'],
                ln=data['ln'],
                password=hash_password(data['password']),
                role=roles['member']
            )
            session.add(user)
            session.flush()
            schema = UserSchema()
            res.status = falcon.HTTP_200
            res.body = self.to_json(schema.dump(user).data)


class Item(BaseOptions):
    """
    Handle /v1/users/{user_id}
    """
    def on_get(self, req, res, user_id):
        res.status = falcon.HTTP_200
        res.body = self.to_json({'success': user_id})


class Self(BaseOptions):
    """
    Handle /v1/users/self
    """
    pass


class Login(BaseOptions):
    """
    Handle /v1/users/self/login
    """
    def on_post(self, req, res):
        session = req.context['session']
        data = json.loads(req.bounded_stream.read().decode())
        result = LoginSchema().load(data)
        if result.errors:
            res.status = falcon.HTTP_BAD_REQUEST
            res.body = self.to_json({'errors':result.errors})
        else:
            usr = session.query(User).filter_by(email=data['email']).one()
            if usr:
                if verify_password(data['password'], usr.password):
                    u = {
                        "id": usr.id,
                        "name": "%s %s" % (usr.fn, usr.ln)
                    }
                    wt = jwt.encode(u, SECRET_KEY, algorithm='HS256')
                    res.status = falcon.HTTP_200
                    res.body = self.to_json({'jwt': wt.decode('utf-8')})
                else:
                    res.status = falcon.HTTP_401
                    res.body = self.to_json('Bad password.')
            else:
                res.status = falcon.HTTP_NOT_FOUND
                res.body = self.to_json('User not found.')