#!/usr/bin/env python
"""Tests functions from the reminder rest api."""

# External imports
import unittest
import hug
import json
import peewee
import sqlite3
import os

# Local imports
import context
from bot_calendario_telegram.settings import TESTING_VARS
import bot_calendario_telegram.reminder_rest_api as rest

assert context


# === Clase test ===
class ReminderTestApiTest(unittest.TestCase):
    """Reminder api rest test class."""

    def test_index(self):
        """Check if the root path of the application returns status ok."""
        result = hug.test.get(rest, '/')

        self.assertEqual(result.status, '200 OK', 'Not expected result')
        self.assertEqual(result.data, {'status': 'OK'}, 'Not expected result')

    def test_status(self):
        """Check if the root path of the application returns status ok."""
        result_status = hug.test.get(rest, '/status').status
        result_data = hug.test.get(rest, '/status').data

        self.assertEqual(result_status, '200 OK', 'Not expected result')
        self.assertEqual(result_data, {'status': 'OK'}, 'Not expected result')

    def test_event_count(self):
        """Check if the number is correct."""
        result = hug.test.get(rest, '/event/count')

        self.assertEqual(result.status, '200 OK', 'Not expected result')
        self.assertEqual(result.data, len(reminder_test_data),
                         'Not expected result')

    def test_get_one(self):
        """Check if the number is correct."""
        should_result_data = list(
            filter(lambda x: x.get('event_id') == '1', reminder_test_data))[0]

        result = hug.test.get(rest, '/event/get/1')
        result_error = hug.test.get(rest, '/event/get/19')

        self.assertEqual(result.status, '200 OK', 'Not expected result')
        self.assertEqual(result.data, should_result_data,
                         'Not expected result')
        self.assertEqual(result_error.status, '200 OK', 'Not expected result')
        self.assertEqual(result_error.data, {}, 'Not expected result')

    def test_get_next(self):
        """Check if the number is correct."""
        next_event_test = list(
            filter(lambda x: x.get('event_id') == '4', reminder_test_data))[0]

        result = hug.test.get(rest, '/event/next')

        self.assertEqual(result.status, '200 OK', 'Not expected result')
        self.assertEqual(result.data, next_event_test, 'Incorrect output')

    def test_get_all(self):
        """Check if returns all events."""
        sorted_events = sorted(
            reminder_test_data, key=lambda x: x.get('reminder_datetime'))

        result = hug.test.get(rest, '/event/list')

        self.assertEqual(result.status, '200 OK', 'Not expected result')
        self.assertEqual(result.data, sorted_events, 'Not expected result')

    def test_new_update_delete_event(self):
        """Check for exceptions in the insertion/update/deletion."""
        test_insertion = {
            'event_id': 'test_event',
            'reminder_datetime': '2000/01/01 00:00:00'
        }
        test_update = {
            'event_id': 'test_event',
            'reminder_datetime': '2049/01/01 00:00:00'
        }
        insert_wanted_result = {
            'event_id': 'test_event',
            'reminder_datetime': '2000/01/01 00:00:00'
        }

        # Insert a new event
        result_insert = hug.test.post(rest, '/event/new', test_insertion)

        # Update the previuosly inserted event
        result_update = hug.test.put(rest, '/event/update', test_update)

        # Check if the returning of the inserti is the event in essence
        self.assertEqual(result_insert.status, '200 OK', 'Not expected result')
        self.assertEqual(result_insert.data, insert_wanted_result,
                         'Not expected result')

        # Check if there was one line updated
        self.assertEqual(result_update.status, '200 OK', 'Not expected result')
        self.assertEqual(result_update.data, 1, 'No event updated')

        # Check if it is possible to insert another event with the same ID
        with self.assertRaises(peewee.IntegrityError):
            hug.test.post(rest, '/event/new', test_insertion)

        # Delete the previous inserted event
        result_deletion = hug.test.delete(rest, '/event/delete/test_event')
        self.assertEqual(result_deletion.status, '200 OK',
                         'Not expected result')
        self.assertEqual(result_deletion.data, 1, 'No row deleted')

        # Try to delete inexistent event
        result_deletion = hug.test.delete(rest, '/event/delete/non_existent')
        self.assertEqual(result_deletion.status, '200 OK',
                         'Not expected result')
        self.assertEqual(result_deletion.data, 0, 'No row deleted')


def setUpModule():
    """Set up Module method."""
    global reminder_test_data
    global TESTING_VARS

    with open(TESTING_VARS['REMINDER_DATA_FILE'], 'r') as f:
        reminder_test_data = json.loads(f.read()).get('event_reminder')

    # Conexión
    conn = sqlite3.connect(TESTING_VARS['DB_NAME'])

    # Cursor
    c = conn.cursor()

    # Drop table if already exists
    c.execute('DROP TABLE IF EXISTS \'event_reminder\'')

    # Create table
    c.execute('''
    CREATE TABLE event_reminder(
        id INTEGER PRIMARY KEY,
        event_id varchar(255) NOT NULL UNIQUE,
        reminder_datetime datetime NOT NULL
    );
    ''')

    test_data = [(k['event_id'], k['reminder_datetime'])
                 for k in reminder_test_data]

    # Insert the test data into the database
    c.executemany(
        'INSERT INTO event_reminder (event_id, reminder_datetime) VALUES \
(?, ?)', test_data)

    # Save (commit) the changes
    conn.commit()

    # Close the connection if everything is done
    conn.close()

    # Initialize the object to access the database
    database = peewee.SqliteDatabase(TESTING_VARS['DB_NAME'])
    rest.reminder = rest.Reminder()
    rest.reminder.initialize(database)


def tearDownModule():
    """Tear down Module method."""
    # Close the database connection
    rest.reminder.close()

    # Remove the testing database if it is not in memory
    if TESTING_VARS['DB_NAME'] != ':memory:':
        os.remove(TESTING_VARS['DB_NAME'])


if __name__ == '__main__':
    unittest.main()
