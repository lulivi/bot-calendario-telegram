#!/usr/bin/env python
"""Tests functions from Reminder Class."""

# External imports
import unittest
import peewee
import json
import sqlite3
import os

# Local imports
import context
from bot_calendario_telegram.settings import TESTING_VARS
import bot_calendario_telegram.reminder as rem
assert context


# === Clase test ===
class ReminderTest(unittest.TestCase):
    """Reminder test class."""

    def test_save_update_delete_event(self):
        """Check for exceptions in the insertion/update/deletion."""
        # Insert a new event
        result_insert = reminder_object.save_event('test_event',
                                                   '2000/01/01 00:00:00')
        # Update the previuosly inserted event
        result_update = reminder_object.update_event('test_event',
                                                     '2049/01/01 00:00:00')

        # Check if the returning of the inserti is the event in essence
        self.assertEqual(result_insert, {
            'event_id': 'test_event',
            'reminder_datetime': '2000/01/01 00:00:00'
        }, 'Not the correct return')
        # Check if there was one line updated
        self.assertEqual(result_update, 1, 'No event updated')

        # Check if it is possible to insert another event with the same ID
        with self.assertRaises(peewee.IntegrityError):
            reminder_object.save_event('test_event', '2049/01/01 00:00:00')

        # Delete the previous inserted event
        result = reminder_object.delete_event('test_event')
        self.assertEqual(result, 1, 'Not one row deleted')

        # Try to delete inexistent event
        result = reminder_object.delete_event('non_existent_event')
        self.assertEqual(result, 0, 'Should not delete nothing')

    def test_get_event(self):
        """Check if it returns a correct event."""
        event_id_1 = list(
            filter(lambda x: x.get('event_id') == '1', reminder_test_data))[0]

        # Test existing event
        result = reminder_object.get_event('1')

        # Test non existing event
        retult_2 = reminder_object.get_event('non_existent_event')

        # Check if it returns the expected event
        self.assertEqual(result, event_id_1,
                         'Didn\'t return the correct event')
        # Check if it returns an empty dictionary
        self.assertEqual(retult_2, {}, 'Non existent event is not empty')

    def test_next_event(self):
        """Check if the next event is the first on a sorted list."""
        next_event_test = list(
            filter(lambda x: x.get('event_id') == '4', reminder_test_data))[0]

        # Test next event
        result = reminder_object.next_event()

        # Should return the next event order by date
        self.assertEqual(result, next_event_test, 'Incorrect output')

    def test_get_all_events(self):
        """Check if there are any exceptions in the select."""
        # Test get all events
        result = reminder_object.get_all_events()

        # Should return the same as `all_events_json`
        self.assertEqual(result,
                         sorted(
                             reminder_test_data,
                             key=lambda x: x.get('reminder_datetime')),
                         'Date sorting is not correct')


def setUpModule():
    """Set up Module method."""
    global reminder_object
    global reminder_test_data
    global TESTING_VARS

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

    # Create the database object
    database = peewee.SqliteDatabase(TESTING_VARS['DB_NAME'])

    # Create Reminder object, init it and connect to the database
    reminder_object = rem.Reminder()
    reminder_object.initialize(database)
    reminder_object.connect()


def tearDownModule():
    """Tear down Module method."""
    global reminder_object

    # Close the database connection of reminder_object
    reminder_object.close()

    # Remove the testing database if it is not in memory
    if TESTING_VARS['DB_NAME'] != ':memory:':
        os.remove(TESTING_VARS['DB_NAME'])


if __name__ == '__main__':
    unittest.main()
