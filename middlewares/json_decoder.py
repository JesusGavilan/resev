import json
import falcon

from utils.errors.errors import NotValidParameterError


class JSONDecoder(object):
    def process_request(self, req, res):
        if req.content_type == 'application/json':
            try:
                raw_json = req.stream.read()
            except Exception:
                message = 'Error reading'
                raise falcon('Bad request', message)
            try:
                req.context['data'] = json.loads(raw_json.decode('utf-8'))
            except ValueError:
                raise NotValidParameterError('Malformed JSON')
            except UnicodeDecodeError:
                raise NotValidParameterError('JSON object can not be decoded by utf-8')
        else:
            req.context['data'] = None