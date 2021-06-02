from google_auth_oauthlib import flow as oauthflow


class ImproperlyConfigured(Exception):
    pass


class Oauth(object):

    def __init__(self, credentials_path, scopes):
        self.credentials_path = credentials_path
        self.scopes = scopes

    def get_user_credentials(self):
        return self.__session_credentials

    def get_authorization_url(
        self,
        redirect_uri,
        access_type='offline',
        include_granted_scopes='true'
    ):
        flow = oauthflow.Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=self.scopes
        )
        flow.redirect_uri = redirect_uri
        self.redirect_uri = redirect_uri
        authorization_url, state = flow.authorization_url(
            access_type=access_type,
            include_granted_scopes=include_granted_scopes
        )
        return authorization_url

    def on_auth_callback(self, state, code):
        flow = oauthflow.Flow.from_client_secrets_file(
            self.credentials_path,
            scopes=self.scopes,
            state=state
        )
        flow.redirect_uri = self.redirect_uri
        flow.fetch_token(code=code)
        self.__session_credentials = {
            'token': flow.credentials.token,
            'token_uri': flow.credentials.token_uri,
            'client_id': flow.credentials.client_id,
            'client_secret': flow.credentials.client_secret,
            'scopes': flow.credentials.scopes
        }
        return self.__session_credentials
