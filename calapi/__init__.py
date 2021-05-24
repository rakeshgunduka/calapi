import json
import sqlite3
import google_auth_oauthlib.flow
import google.oauth2.service_account
import apiclient.discovery.build


class Client(object):

    def __init__(
        self,
        credentials,
        scopes,
        api_version='v3',
        db_storage=True,
        db_name='ga_calendar_sessions'
    ):
        self.__credentials = credentials
        self.scopes = scopes
        credentials = google.oauth2.service_account.Credentials.from_service_account_info(
            credentials
        )
        self.service = apiclient.discovery.build(
            'calendar',
            'v3',
            credentials=credentials
        )
        self.db_storage = db_storage
        self.conn = None
        if self.db_storage:
            self.__conn = sqlite3.connect('{}.db'.format(db_name))
            self.init_db()


    def init_db(self):
        self.__conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id integer PRIMARY KEY AUTOINCREMENT,
                session text,
            );'''
        )

    def create_session(self, session):
        cursor = self.__conn.cursor()
        cursor.execute('''
            INSERT INTO sessions (session) VALUES ({});'''.format(
                json.dumps(session)
            )
        )
        self.current_session_id = cursor.lastrowid


    def get_session(self):
        cursor = self.__conn.cursor()
        row = cursor.execute('''
            SELECT * from sessions where id = {};'''.format(
                self.current_session_id
            )
        )
        return row


    def get_authorization_url(
        self,
        redirect_uri,
        access_type='offline',
        include_granted_scopes='true'
    ):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.__credentials,
            scopes=self.__scopes
        )
        flow.redirect_uri = redirect_uri
        self.redirect_uri = redirect_uri
        authorization_url, state = flow.authorization_url(
            access_type=access_type,
            include_granted_scopes=include_granted_scopes
        )
        return authorization_url

    def on_auth_callback(self, state, authorization_response):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            self.__credentials,
            scopes=self.__scopes
            state=state
        )
        flow.redirect_uri = self.redirect_uri
        authorization_response = '{}{}'.format(
            settings.BASE_URL, request.get_full_path())

        flow.fetch_token(authorization_response=authorization_response)
        
        if self.db_storage:
            self.create_session(flow.credentials)
        return flow.credentials




scopes = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.readonly'
]
