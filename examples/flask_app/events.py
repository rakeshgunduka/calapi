import json

from flask import Blueprint, render_template, redirect
from flask import request, g, jsonify, make_response, abort

from calapi import Events

mod = Blueprint('events', __name__)


@mod.route('/api/google/calendar/events/insert')
def google_calendar_insert():
    is_calendar_connected = request.cookies.get('is_calendar_connected')
    if not is_calendar_connected:
        return "Calendar Not Connected", 400
    user_google_auth_credentials = request.cookies.get('user_google_auth_credentials')
    session_credentials = json.loads(user_google_auth_credentials)
    events = Events(session_credentials=session_credentials)

    query = events.query.start(
                date_time='2021-06-03T09:00:00-07:00',
                time_zone='America/Los_Angeles'
            ).end(
                date_time='2021-06-03T09:30:00-07:00',
                time_zone='America/Los_Angeles'
            ).attendees([
                {'email': 'lp_age@example.com'},
                {'email': 'sbrin@example.com'},
            ]).summary(
                'Google I/O 2015'
            ).description(
                '800 Howard St., San Francisco, CA 94103'
            ).recurrence([
                'RRULE:FREQ=DAILY;COUNT=2'
            ]).reminders({
                'use_default': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            })
    created_event = events.insert(query)
    return jsonify(created_event)


@mod.route('/api/google/calendar/events/get')
def google_calendar_get_event():
    is_calendar_connected = request.cookies.get('is_calendar_connected')
    if not is_calendar_connected:
        return "Calendar Not Connected", 400
    user_google_auth_credentials = request.cookies.get('user_google_auth_credentials')
    session_credentials = json.loads(user_google_auth_credentials)
    events = Events(session_credentials=session_credentials)

    event_id = request.args.get('eventId')
    event = events.get(event_id)
    return jsonify(event)


@mod.route('/api/google/calendar/events/delete')
def google_calendar_get_delete():
    is_calendar_connected = request.cookies.get('is_calendar_connected')
    if not is_calendar_connected:
        return "Calendar Not Connected", 400
    user_google_auth_credentials = request.cookies.get('user_google_auth_credentials')
    session_credentials = json.loads(user_google_auth_credentials)
    events = Events(session_credentials=session_credentials)

    event_id = request.args.get('eventId')
    events.delete(event_id)
    return "Event Deleted", 200
