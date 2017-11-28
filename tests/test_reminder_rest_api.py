#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests functions from the reminder rest api.

Copyright 2017, Luis Liñán (luislivilla@gmail.com)

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>
"""

# External imports
import unittest
import hug
import json

# Local imports
import context
from bot_calendario_telegram.settings import TESTING_VARS
import bot_calendario_telegram.reminder_rest_api as rest

assert context, TESTING_VARS


# === Clase test ===
class ReminderTestApiTest(unittest.TestCase):
    """Reminder api rest test class."""

    def test_index(self):
        """Check if the root path of the application returns status ok."""
        result_status = hug.test.get(rest, '/').status
        result_data = hug.test.get(rest, '/').data

        self.assertEqual(result_status, '200 OK', 'Not expected result')
        self.assertEqual(result_data, {'status': 'OK'}, 'Not expected result')

    def test_status(self):
        """Check if the root path of the application returns status ok."""
        result_status = hug.test.get(rest, '/status').status
        result_data = hug.test.get(rest, '/status').data

        self.assertEqual(result_status, '200 OK', 'Not expected result')
        self.assertEqual(result_data, {'status': 'OK'}, 'Not expected result')

    def test_get_all(self):
        """Check if returns all events."""
        result_status = hug.test.get(rest, '/all').status
        result_data = hug.test.get(rest, '/all').data

        self.assertEqual(result_status, '200 OK', 'Not expected result')
        self.assertEqual(result_data, reminder_object['event'],
                         'Not expected result')

    def test_events_number(self):
        """Check if the number is correct."""
        result_status = hug.test.get(rest, '/number').status
        result_data = hug.test.get(rest, '/number').data

        self.assertEqual(result_status, '200 OK', 'Not expected result')
        self.assertEqual(result_data,
                         len(reminder_object['event']), 'Not expected result')

    def test_get_one(self):
        """Check if the number is correct."""
        result_status = hug.test.get(rest, '/get/1').status
        result_data = hug.test.get(rest, '/get/1').data
        result_error_status = hug.test.get(rest, '/get/19').status
        result_error_data = hug.test.get(rest, '/get/19').data

        for rem in reminder_object['event']:
            if rem['id_event'] == '1':
                should_result_data = rem

        self.assertEqual(result_status, '200 OK', 'Not expected result')
        self.assertEqual(result_data, should_result_data,
                         'Not expected result')
        self.assertEqual(result_error_status, '200 OK', 'Not expected result')
        self.assertEqual(result_error_data,
                         {'id_event': None,
                          "data_event": None}, 'Not expected result')


def setUpModule():
    """Set up Module method."""
    global reminder_object
    global TESTING_VARS

    with open(TESTING_VARS['REMINDER_DATA_FILE'], 'r') as file:
        reminder_object = json.loads(file.read())


if __name__ == '__main__':
    unittest.main()
