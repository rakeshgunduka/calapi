from .query import Query, _camelify
from .exceptions import InvalidJsonError
from .service import Service


class Calendars(Service):

    def __init__(self, session_credentials):
        super().__init__(session_credentials)

    def clear(self, calendar_id):
        return self.service.calendars().clear(calendar_id).execute()

    def insert(self, query):
        if isinstance(query, Query):
            calendar = query.json(camelify=True)
        elif isinstance(query, dict):
            calendar = _camelify(query)
        else:
            raise InvalidJsonError()
        return self.service.calendars().insert(
                    body=calendar
                ).execute()

    def get(self, calendar_id):
        return self.service.calendars().get(
                    calendarId=calendar_id,
                ).execute()

    def delete(self, calendar_id):
        return self.service.calendars().delete(calendarId=calendar_id).execute()

    def list(self, calendar_id, page_token=None):
        return self.service.calendars().list(
                    calendarId=calendar_id,
                    pageToken=page_token
                ).execute()

    def update(self, query, calendar_id):
        if isinstance(query, Query):
            calendar = query.json(camelify=True)
        elif isinstance(query, dict):
            calendar = _camelify(query)
        else:
            raise InvalidJsonError()

        updated_calendar = self.service.calendars().get(
                    calendarId=calendar_id,
                ).execute()

        for params in calendar:
            updated_calendar[params] = calendar[params]

        return self.service.calendars().update(
                    calendarId=calendar_id,
                    body=updated_calendar
                ).execute()

    def patch(self):
        raise NotImplementedError("Patch API Wrapper Function Not Implemented")

    def __getattr__(self, name):
        if name == 'query':
            return Query()
