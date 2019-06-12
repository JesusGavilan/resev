from utils.errors.base import AppError
from collections import OrderedDict
from utils.errors.messages import *


class DatabaseError(AppError):
    def __init__(self, error, args=None, params=None):
        super().__init__(error)
        obj = OrderedDict()
        obj['details'] = ', '.join(args)
        obj['params'] = str(params)
        self.error['description'] = obj


class NotValidParameterError(AppError):
    def __init__(self, description=None):
        super().__init__(ERROR_NOT_VALID_PARAMETER)
        self.error['description'] = description


class NotSupportedError(AppError):
    def __init__(self, method=None, url=None):
        super().__init__(ERROR_NOT_SUPPORTED)
        if method and url:
            self.error['description'] = 'method: %s , url: %s' % (method, url)


class OperationError(AppError):
    def __init__(self, description=None):
        super().__init__(ERROR_OPERATION)
        self.error['description'] = description


class UserNotExistsError(AppError):
    def __init__(self, description=None):
        super().__init__(ERROR_USER_NOT_EXISTS)
        self.error['description'] = description


class InvalidPassword(AppError):
    def __init__(self, description=None):
        super().__init__(ERROR_INVALID_PASSWORD)
        self.error['description'] = description


class AuthorizationError(AppError):
    def __init__(self, description=None):
        super().__init__(ERROR_AUTH)
        self.error['description'] = description