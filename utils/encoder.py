import json
import time
import datetime

from sqlalchemy.ext.declarative import DeclarativeMeta


def encoder():
    _objects = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o.__class__, DeclarativeMeta):
                if o in _objects:
                    return None
                _objects.append(o)

                fields = {}
                for field in [x for x in dir(o) if not x.startswith('_') and x != 'metadata']:
                    fields[field] = o.__getattribute__(field)
                return fields
            return json.JSONEncoder.default(self, o)

    return AlchemyEncoder


def passby(data):
    return data


def datetime_to_timestamp(date):
    if isinstance(date, datetime.date):
        return int(time.mktime(date.timetuple()))
    else:
        return None
