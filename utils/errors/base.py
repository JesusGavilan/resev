import falcon
import json

from utils.errors.messages import *
from collections import OrderedDict


class AppError(Exception):
    def __init__(self, error=ERROR_UNKNOWN, description=None):
        self.error = error
        self.error['description'] = description

    @property
    def title(self):
        return self.error['title']

    @property
    def status(self):
        return self.error['status']

    @property
    def description(self):
        return self.error['description']

    @staticmethod
    def handle(exception, req, res, error=None):
        res.status = exception.status
        meta = OrderedDict()
        meta['message'] = exception.title
        if exception.description:
            meta['description'] = exception.description
        res.body = json.dumps({'meta': meta})
