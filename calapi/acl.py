from .query import Query, _camelify
from .exceptions import InvalidJsonError
from .service import Service

class Acl(Service):

    def __init__(self, session_credentials):
        super().__init__(session_credentials)

    def insert(self, query, calendar_id='primary'):
        if isinstance(query, Query):
            rule = query.json(camelify=True)
        elif isinstance(query, dict):
            rule = _camelify(query)
        else:
            raise InvalidJsonError()
        return self.service.acl().insert(
                    calendarId=calendar_id,
                    body=rule
                ).execute()

    def get(self, rule_id, calendar_id='primary'):
        return self.service.acl().get(
                    calendarId=calendar_id,
                    ruleId=rule_id
                ).execute()

    def delete(self, rule_id, calendar_id='primary'):
        return self.service.acl().delete(
                    calendarId=calendar_id,
                    ruleId=rule_id
                ).execute()
    
    def list(self, calendar_id='primary'):
        return self.service.acl().list(calendarId=calendar_id).execute()

    def update(self, rule_id, query, calendar_id='primary'):
        if isinstance(query, Query):
            rule = query.json(camelify=True)
        elif isinstance(query, dict):
            rule = _camelify(query)
        else:
            raise InvalidJsonError()

        updated_rule = self.service.acl().get(
                    calendarId=calendar_id,
                    ruleId=rule_id
                ).execute()

        for params in rule:
            updated_rule[params] = rule[params]

        return self.service.acl().update(
                    calendarId=calendar_id,
                    ruleId=rule_id,
                    body=updated_rule
                ).execute()

    def patch(self):
        raise NotImplementedError("Patch API Wrapper Function Not Implemented")

    def watch(self):
        raise NotImplementedError("Watch API Wrapper Function Not Implemented")

    def __getattr__(self, name):
        if name == 'query':
            return Query()
