from schemas.user import FIELDS
from cerberus import Validator
from cerberus.errors import ValidationError
from utils.errors.errors import NotValidParameterError


def validate_user_create(req, res, resource, params):
    schema = {
        'username': FIELDS['username'],
        'email': FIELDS['email'],
        'password': FIELDS['password'],
        'details': FIELDS['details'],
        'balance': FIELDS['quantity']
    }
    validate(schema, req)


def validate_money_transfer_create(req, res, resource, params):
    schema = {
        'borrower': FIELDS['username'],
        'quantity': FIELDS['quantity']
    }
    validate(schema, req)


def validate(schema, req):
    v = Validator(schema)
    try:
        if not v.validate(req.context['data']):
            raise NotValidParameterError(v.errors)
    except ValidationError:
        raise NotValidParameterError('Invalid request %s' % req.context)