"""Provide responses for some routes in the app."""

# System imports
import hug
import peewee
import json
import os
import sqlite3
from urllib import parse

# Local imports
import context
from bot_calendario_telegram.settings import (
    TESTING_VARS,
    REMINDER_REST_API_PORT,
    HEROKU_PG_DATABASE_URL,
)
from bot_calendario_telegram.reminder import Reminder

assert context

# Create the reminder object
reminder = None


# === Get / ===
@hug.get('/')
def index():
    """Return web status."""
    return {'status': 'OK'}


# === Get /status ===
@hug.get('/status')
def status():
    """Return web status."""
    return {'status': 'OK'}


# === Get /event/count ===
@hug.get('/event/count')
def get_count():
    """Return the number of events."""
    return reminder.get_all_events_count()


# === Get /event/get/{event_id} ===
@hug.get('/event/get/{event_id}')
def get_one(event_id: hug.types.text):
    """Return an event from it id."""
    return reminder.get_event(event_id=event_id)


# === Get /event/get/{event_id} ===
@hug.get('/event/next')
def get_next():
    """Return an event from it id."""
    return reminder.next_event()


# === Get /event/list ===
@hug.get('/event/list')
def get_all():
    """Return all events."""
    return reminder.get_all_events()


# === Post /event/new ===
@hug.post('/event/new')
def new_event(body):
    """Insert a new event in the database."""
    return reminder.save_event(
        event_id=body.get('event_id'),
        reminder_datetime=body.get('reminder_datetime'))


# === Put /event/update ===
@hug.put('/event/update')
def update_event(body):
    """Update an event."""
    return reminder.update_event(
        event_id=body.get('event_id'),
        new_reminder_datetime=body.get('reminder_datetime'),
    )


# === Put /event/delete/{event_id} ===
@hug.delete('/event/delete/{event_id}')
def delete_event(event_id: hug.types.text):
    """Delete an event."""
    return reminder.delete_event(event_id=event_id)


def main():
    """Main program function."""
    global reminder

    # Check if we are in production or in local testing
    if HEROKU_PG_DATABASE_URL:
        # Obtain the database url and split it into necesary parts
        parse.uses_netloc.append('postgres')
        db_url = parse.urlparse(HEROKU_PG_DATABASE_URL)

        # Create the database object
        database = peewee.PostgresqlDatabase(
            db_name=db_url.path[1:],
            user=db_url.username,
            password=db_url.password,
            host=db_url.hostname,
            port=db_url.port)
    else:
        with open(TESTING_VARS['REMINDER_DATA_FILE'], 'r') as f:
            reminder_test_data = json.loads(f.read()).get('event_reminder')

        test_data = [(k['event_id'], k['reminder_datetime'])
                     for k in reminder_test_data]

        # Createconnection and connect
        conn = sqlite3.connect(TESTING_VARS['DB_NAME'])
        c = conn.cursor()
        # Create table
        c.execute('DROP TABLE IF EXISTS \'event_reminder\'')
        c.execute('CREATE TABLE event_reminder(id INTEGER PRIMARY KEY, \
event_id varchar(255) NOT NULL UNIQUE,reminder_datetime datetime NOT NULL);')
        # Insert the test data into the database
        c.executemany('INSERT INTO event_reminder (event_id, \
reminder_datetime) VALUES (?, ?)', test_data)
        # Save (commit) the changes and close
        conn.commit()
        conn.close()
        database = peewee.SqliteDatabase(TESTING_VARS['DB_NAME'])

    # Create the reminder object and initialize it with the database
    reminder = Reminder()
    reminder.initialize(database)

    try:
        # Start hug web rest api
        hug.API(__name__).http.serve(REMINDER_REST_API_PORT)
    except KeyboardInterrupt:
        if TESTING_VARS['DB_NAME'] != ':memory:':
            os.remove(TESTING_VARS['DB_NAME'])
        reminder.close()
        print('Rest api ended.')


if __name__ == '__main__':
    main()
