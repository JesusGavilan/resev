import falcon
import json

import log
from utils.encoder import encoder
from collections import OrderedDict
from utils.errors.errors import NotSupportedError
LOG = log.get_logger()


class BaseResource(object):
    def to_json(self, body_dict):
        return json.dumps(body_dict)

    def from_db_to_json(self, db):
        return json.dumps(db, cls=encoder())

    def on_error(self, res, error=None):
        res.status = error['status']
        meta = OrderedDict()
        meta['code'] = error['code']
        meta['message'] = error['message']

        object = OrderedDict()
        object['meta'] = meta
        res.body = self.to_json(object)

    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta['code'] = 200
        meta['message'] = 'OK'

        object = OrderedDict()
        object['meta'] = meta
        object['data'] = data
        res.body = self.to_json(object)

    def on_get(self, req, res):
        if req.path == '/':
            res.status = falcon.HTTP_200
            res.body = self.to_json({'app': 'app'})
        else:
            raise NotSupportedError

    def on_post(self, req, res):
        raise NotSupportedError(method='POST', url=req.path)

    def on_put(self, req, res):
        raise NotSupportedError(method='PUT', url=req.path)

    def on_delete(self, req, res):
        raise NotSupportedError(method='DELETE', url=req.path)

