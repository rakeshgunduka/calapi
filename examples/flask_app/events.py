import json

from datetime import datetime, timedelta
from flask import Blueprint
from flask import request, jsonify

from calapi import Session

mod = Blueprint('events', __name__)


@mod.route('/api/google/calendar/events/insert')
def google_calendar_insert():
    is_calendar_connected = request.cookies.get('is_calendar_connected')
    if not is_calendar_connected:
        return "Calendar Not Connected", 400
    user_google_auth_credentials = request.cookies.get('user_google_auth_credentials')
    session_credentials = json.loads(user_google_auth_credentials)
    session = Session(session_credentials=session_credentials)
    now = datetime.now()
    after_1_hour = now + timedelta(hours=1)

    query = session.events.query.start(
                date_time=now.isoformat(),
                time_zone='Asia/Kolkata'
            ).end(
                date_time=after_1_hour.isoformat(),
                time_zone='Asia/Kolkata'
            ).attendees([
                {'email': 'lp_age@example.com'},
                {'email': 'sbrin@example.com'},
            ]).summary(
                'Calapi Flask App Testing'
            ).description(
                "A light weight python wrapper for Google's Calendar API v3"
            ).recurrence([
                'RRULE:FREQ=DAILY;COUNT=2'
            ]).reminders({
                'use_default': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            })
    created_event = session.events.insert(query)
    print(created_event)
    return jsonify(created_event)


@mod.route('/api/google/calendar/events/get')
def google_calendar_get_event():
    is_calendar_connected = request.cookies.get('is_calendar_connected')
    if not is_calendar_connected:
        return "Calendar Not Connected", 400
    user_google_auth_credentials = request.cookies.get('user_google_auth_credentials')
    session_credentials = json.loads(user_google_auth_credentials)
    session = Session(session_credentials=session_credentials)

    event_id = request.args.get('eventId')
    event = session.events.get(event_id)
    return jsonify(event)


@mod.route('/api/google/calendar/events/delete')
def google_calendar_get_delete():
    is_calendar_connected = request.cookies.get('is_calendar_connected')
    if not is_calendar_connected:
        return "Calendar Not Connected", 400
    user_google_auth_credentials = request.cookies.get('user_google_auth_credentials')
    session_credentials = json.loads(user_google_auth_credentials)
    session = Session(session_credentials=session_credentials)

    event_id = request.args.get('eventId')
    session.events.delete(event_id)
    return "Event Deleted", 200
