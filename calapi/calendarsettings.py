from .query import Query, _camelify
from .exceptions import InvalidJsonError
from .service import Service


class Settings(Service):

    def __init__(self, session_credentials):
        super().__init__(session_credentials)


    def get(self, setting_id):
        return self.service.settings().get(setting=setting_id).execute()

    def list(self):
        return self.service.settings().list().execute()

    def watch(self):
        raise NotImplementedError("Watch API Wrapper Function Not Implemented")

    def __getattr__(self, name):
        if name == 'query':
            return Query()
