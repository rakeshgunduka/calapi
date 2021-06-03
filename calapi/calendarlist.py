from .query import Query, _camelify
from .exceptions import InvalidJsonError
from .service import Service


class CalendarList(Service):

    def __init__(self, session_credentials):
        super().__init__(session_credentials)

    def insert(self, query, calendar_id):
        if isinstance(query, Query):
            calendar_list_entry = query.json(camelify=True)
        elif isinstance(query, dict):
            calendar_list_entry = _camelify(query)
        else:
            raise InvalidJsonError()
        query['id'] = calendar_id
        return self.service.calendarList().insert(
                    body=calendar_list_entry
                ).execute()

    def get(self, calendar_id):
        return self.service.calendarList().get(
                    calendarId=calendar_id,
                ).execute()

    def delete(self, calendar_id):
        return self.service.calendarList().delete(calendarId=calendar_id).execute()

    def list(self, calendar_id, page_token=None):
        return self.service.calendarList().list(
                    calendarId=calendar_id,
                    pageToken=page_token
                ).execute()

    def update(self, query, calendar_id):
        if isinstance(query, Query):
            calendar_list_entry = query.json(camelify=True)
        elif isinstance(query, dict):
            calendar_list_entry = _camelify(query)
        else:
            raise InvalidJsonError()

        updated_calendar_list_entry = self.service.calendarList().get(
                    calendarId=calendar_id,
                ).execute()

        for params in calendar_list_entry:
            updated_calendar_list_entry[params] = calendar_list_entry[params]

        return self.service.calendarList().update(
                    calendarId=calendar_id,
                    body=updated_calendar_list_entry
                ).execute()

    def patch(self):
        raise NotImplementedError("Patch API Wrapper Function Not Implemented")

    def watch(self):
        raise NotImplementedError("Watch API Wrapper Function Not Implemented")

    def __getattr__(self, name):
        if name == 'query':
            return Query()
