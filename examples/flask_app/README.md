# Calapi Flask App

Flask APP for demonstrating usage of calapi - Google Calendar API v3


## Install requirements

    pip install -r requirements.txt


## Acquire Google Oauth credentials

**1.  Create a new project on google console dashboard on below link**

https://console.cloud.google.com/apis/dashboard

**2.  Enable Google Calendar API on the below link**

https://console.cloud.google.com/apis/library/calendar-json.googleapis.com

**3.  Configure Oauth Consent Screen**

- Open Link https://console.cloud.google.com/apis/credentials/consent
- Click on "OAuth Consent screen"
- Select User Type and click create
- Provide app name, email and proceed
- Add Required scopes based on your use case
- Proceed and complete the process

**3.  Create Oauth Client ID credentials for Users consent**

- Open Link https://console.cloud.google.com/apis/credentials/consent
- Click on "+ Create Credentials"
- Select "OAuth client ID"
- Select Application Type "Web Application"
- Provide name, authorized javascript URIs, authorized redirect URIs and create
- Download the credentials (Eg. credentials.json)


** Update `credentials.json` path in the settings.py file **

    OAUTH_CREDENTIALS_PATH = './credentials.json'


## Run the app
**After service starts, open `http://localhost:8001` in your browser**

    python serve.py


This App provides you an usage example of calapi for accessing calendars api.
You should be able to do following actions in the App

- Get Users consent for accessing users calendar
- Create an event for next 1 hour
- Get created event
- Delete created event
