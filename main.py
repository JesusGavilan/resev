"""
TODO:
Here the main application in order to run gunicorn and
start serving the API REST
"""
import falcon

import log
from wsgiref import simple_server
from middlewares import AuthorizationHandler, JSONDecoder, DBSessionManager
from resources import base
from resources import users, login
from utils.errors.errors import AppError
from db import db_session, init_session

LOG = log.get_logger()


class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        LOG.info('Starting API Server')

        self.add_route('/', base.BaseResource())
        self.add_route('/resev/v1/users', users.Collection())
        self.add_route('/resev/v1/users/{user_id}', users.Item())

        self.add_route('/resev/v1/users/login', login.Item())

        self.add_route('/resev/v1/users/{user_id}/transfer', users.ItemTransfer())

        self.add_error_handler(AppError, AppError.handle)


init_session()
middleware = [AuthorizationHandler(), JSONDecoder(), DBSessionManager(db_session)]
application = App(middleware=middleware)

if __name__ == "__main__":
    httpd = simple_server.make_server('127.0.0.1', 5000, application)
    httpd.serve_forever()