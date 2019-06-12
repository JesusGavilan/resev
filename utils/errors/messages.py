import falcon

OK = {
    'status': falcon.HTTP_200
}

ERROR_UNKNOWN = {
    'status': falcon.HTTP_500,
    'title': 'Unknown error'
}

ERROR_AUTH = {
    'status': falcon.HTTP_401,
    'title': 'Authentication required'
}

ERROR_NOT_VALID_PARAMETER = {
    'status': falcon.HTTP_400,
    'title': 'Not valid parameter',
}

ERROR_DATABASE_ROLLBACK = {
    'status': falcon.HTTP_500,
    'title': 'Database rollback Error'
}

ERROR_NOT_SUPPORTED = {
    'status': falcon.HTTP_404,
    'title': 'Not supported'
}

ERROR_OPERATION = {
    'status': falcon.HTTP_781,
    'ttile': 'Operation error'
}
ERROR_USER_NOT_EXISTS = {
    'status': falcon.HTTP_404,
    'title': 'Not supported'
}

ERROR_INVALID_PASSWORD = {
    'status': falcon.HTTP_400,
    'title': 'Password invalid'
}