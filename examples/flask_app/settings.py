APP_BASE_URL = 'http://localhost:8001'

OAUTH_API_SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.readonly'
]
OAUTH_CREDENTIALS_PATH = './samplecredentials.json'
