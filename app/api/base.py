import falcon
import json


class BaseOptions(object):
    """
    Provides a few methods useful to all API resources.
    """
    @staticmethod
    def to_json(data):
        return json.dumps(data)

    @staticmethod
    def from_json(data):
        return json.loads(data)

    @staticmethod
    def gen_message(req):
        return {
            'method': req.method,
            'path': req.path,
            'message': 'Endpoint not implemented.'
        }


class SinkAdapter(BaseOptions, object):
    """
    All routes that do not match are sent here.
    """
    def __call__(self, req, res):
        res.status = falcon.HTTP_NOT_IMPLEMENTED
        res.body = self.to_json(self.gen_message(req))


class BaseResource(BaseOptions):
    """
    Demo/placeholder. Handles the "/" path.
    """
    HI_THERE = 'YaSt says Hello!'

    def on_get(self, req, res):
        if req.path == '/':
            res.status = falcon.HTTP_200
            res.body = self.to_json(self.HI_THERE)

    def on_post(self, req, res):
        res.status = falcon.HTTP_NOT_IMPLEMENTED
        res.body = self.to_json(self.gen_message(req))

    def on_put(self, req, res):
        res.status = falcon.HTTP_NOT_IMPLEMENTED
        res.body = self.to_json(self.gen_message(req))

    def on_delete(self, req, res):
        res.status = falcon.HTTP_NOT_IMPLEMENTED
        res.body = self.to_json(self.gen_message(req))
