import json
import settings

from flask import Blueprint, render_template, redirect
from flask import request, g, jsonify, make_response, abort
from calapi import Oauth

client = Oauth(
    credentials_path=settings.OAUTH_CREDENTIALS_PATH,
    scopes=settings.CALENDAR_API_SCOPES
)
mod = Blueprint('auth', __name__)


@mod.route('/')
def auth():
    is_calendar_connected = request.cookies.get('is_calendar_connected')
    return render_template('auth.html',
                    BASE_URL=settings.APP_BASE_URL,
                    is_calendar_connected=is_calendar_connected
                )


@mod.route('/api/google/calendar/connect')
def connect_google_calendar():
    '''
    First step is to get users consent for using calendar APIs
    Steps:
    - Get Consent Url 
    - Redirect with callback url 
    (Callback APP api url Eg. https://example.com/api/google/calendar/callback )
    '''
    callback_url = '{}/api/google/calendar/callback'.format(settings.APP_BASE_URL)
    oauth_consent_url = client.get_authorization_url(redirect_uri=callback_url)
    return redirect(oauth_consent_url)


@mod.route('/api/google/calendar/callback')
def google_calendar_callback():
    '''
    After user consent is provided, google provides state & code
    using which we have to get User credentials
    Steps:
    - Get state and code from query
    - Call on_auth_callback function using state and code
    - You can get users credentials using get_user_credentials function
    (You can store and reuse those credentials for calendar actions)
    '''
    state = request.args.get('state')
    code = request.args.get('code')
    client.on_auth_callback(state, code)
    user_google_auth_credentials = client.get_user_credentials()
    # print('User Google Auth Creds', user_google_auth_credentials)
    resp = make_response(render_template('auth_success.html'))
    resp.set_cookie('is_calendar_connected', 'true')
    
    # Note: Storing creds in cookies for demonstration purpose only
    # You should keep it in some database
    resp.set_cookie('user_google_auth_credentials', json.dumps(user_google_auth_credentials))
    return resp
