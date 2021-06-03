from .query import Query, _camelify
from .exceptions import InvalidJsonError
from .service import Service


class Colors(Service):

    def __init__(self, session_credentials):
        super().__init__(session_credentials)


    def get(self):
        return self.service.colors().get().execute()

    def __getattr__(self, name):
        if name == 'query':
            return Query()
