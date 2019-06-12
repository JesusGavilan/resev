import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator
from cerberus.errors import ValidationError

import log
from resources.base import BaseResource
from utils.authorization import verify_password
from models import User, Base
from utils.errors.errors import NotValidParameterError, UserNotExistsError, InvalidPassword, AppError, OperationError
LOG = log.get_logger()


FIELDS = {
    'email': {
        'type': 'string',
        'regex': '[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}',
        'required': True,
        'maxlength': 320
    },
    'password': {
        'type': 'string',
        'regex': '[0-9a-zA-Z]\w{3,14}',
        'required': True,
        'minlength': 8,
        'maxlength': 64
    }
}


def validate_login(req, res, resource, params):
    schema = {
        'email': FIELDS['email'],
        'password': FIELDS['password']
    }
    validate(schema, req)


def validate(schema, req):
    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise NotValidParameterError(v.errors)
    except ValidationError:
        raise NotValidParameterError('Invalid request %s' % req.context)


class Item(BaseResource):
    """
    /resev/v1/users/login
    """
    @falcon.before(validate_login)
    def on_post(self, req, res):
        data = req.context['data']
        email = data['email']
        password = data['password']
        session = req.context['session']
        try:
            user_db = User.find_by_emails(session, email)
            if verify_password(password, user_db.password.encode('utf-8')):
                self.on_success(res, user_db.to_dict())
            else:
                raise InvalidPassword()
        except NoResultFound:
            raise UserNotExistsError('User email: %s' % email)