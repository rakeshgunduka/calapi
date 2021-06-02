import re
import google.oauth2.credentials

from apiclient.discovery import build


class BaseException(Exception):
    def __str__(self):
        return self.msg


class InvalidJsonError(BaseException):
    msg = 'Invalid json request'


def _decamelify(obj):
    def func(string): return re.sub(
        '([a-z0-9])([A-Z])', r'\1_\2', string).lower()
    return modify_object(obj, func)


def _camelify(obj):
    def func(string):
        return re.sub(r'_(\w)', lambda match: match.group(1).upper(), string)
    return modify_object(obj, func)


def modify_object(obj, func):
    if isinstance(obj, dict):
        temp_obj = {}
        for key in obj:
            if isinstance(obj[key], str):
                temp_obj[func(key)] = obj[key]
            else:
                temp_obj[func(key)] = modify_object(obj[key], func)
        return temp_obj
    if isinstance(obj, list):
        temp_obj = []
        for key in obj:
            if isinstance(key, str):
                temp_obj.append(key)
            else:
                temp_obj.append(modify_object(key, func))
        return temp_obj
    if isinstance(obj, bool):
        return obj
    if isinstance(obj, str) and not obj.isupper():
        return func(obj)
    return obj


class Query(object):

    def __init__(self):
        self.query = {}

    def __getattr__(self, name):
        def f(*args, **kw):
            if not getattr(self.query, name, None):
                self.query.setdefault(name, None)
            clean = kw.pop('clean', None)
            if clean:
                self.query[name] = None
            if kw:
                self.query[name] = kw
            elif isinstance(args, list):
                self.query[name] = args
            elif len(args) == 1:
                self.query[name] = args[0]
            return self
        return f

    def json(self, camelify=False):
        if camelify:
            return _camelify(self.query)
        return self.query

    def clone(self, query):
        self.query.update(query.json())
        return self


class Events():

    def __init__(self, session_credentials):
        self.session_credentials = session_credentials
        self.service = None
        if session_credentials:
            credentials = google.oauth2.credentials.Credentials(
                **session_credentials)
            self.service = build(
                'calendar',
                'v3',
                credentials=credentials
            )

    def insert(self, query, calendar_id='primary'):
        if isinstance(query, Query):
            request_params = query.json(camelify=True)
        elif isinstance(query, dict):
            request_params = _camelify(query)
        else:
            raise InvalidJsonError()
        return self.service.events().insert(
            calendarId=calendar_id,
            body=request_params
        ).execute()

    def get(self, event_id, calendar_id='primary'):
        return self.service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()

    def delete(self, event_id, calendar_id='primary'):
        return self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
    
    def list(self, page_token=None, calendar_id='primary'):
        return self.service.events().list(
            calendarId=calendar_id,
            pageToken=page_token
        ).execute()

    def __getattr__(self, name):
        if name == 'query':
            return Query()
