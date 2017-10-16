#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Remainder test python module.

Tests functions from Reminder Class.
"""

# External imports
import unittest

# Local imports
import __init__ as init
from reminder import Reminder

assert init


# === Clase test ===
class ReminderTest(unittest.TestCase):
    """Reminder test class."""

    __db_file = '../data/test_reminder.db'

    def test_save_event(self):
        """Check if there are any exceptions in the insertion."""
        remind = Reminder(self.__db_file)

        result = remind.save_event(
            'test_event', '2000-01-01 00:00:00', preserve=False)

        self.assertEqual(result, 0, 'No exceptions')

    def test_get_event(self):
        """Check if it returns a correct event."""
        remind = Reminder(self.__db_file)

        result = remind.get_event('1')

        self.assertFalse(result == '', 'It exists')
        self.assertFalse(result == -1, 'No exceptions')
        self.assertEqual(result, '2017-10-18 12:30:00', 'It is correct')

    def test_delete_event(self):
        """Check if the deletion of an event raises any exceptions."""
        remind = Reminder(self.__db_file)

        result = remind.delete_event('1', preserve=False)

        self.assertEqual(result, 0, 'Deleted without errors')

    def test_next_event(self):
        """Check if the next event is the first on a sorted list."""
        remind = Reminder(self.__db_file)
        next_event_date = {"EventId": "5", "EventDate": "2017-10-05 10:40:00"}

        result = remind.next_event()

        self.assertFalse(result == {}, 'Not empty')
        self.assertEqual(result, next_event_date, 'Correct output')

    def test_get_all_events(self):
        """Check if there are any exceptions in the select."""
        remind = Reminder(self.__db_file)
        all_events_json = {
            "1": "2017-10-18 12:30:00",
            "2": "2017-10-20 14:15:00",
            "3": "2017-10-25 16:45:00",
            "5": "2017-10-05 10:40:00"
        }
        all_events_sorted_json = {
            "5": "2017-10-05 10:40:00",
            "1": "2017-10-18 12:30:00",
            "2": "2017-10-20 14:15:00",
            "3": "2017-10-25 16:45:00"
        }

        result1 = remind.get_all_events()
        result2 = remind.get_all_events(date_sorted=False)

        self.assertEqual(result1, all_events_sorted_json,
                         'Date sorted sorted correct output')
        self.assertEqual(result2, all_events_json,
                         'No date sorted sorted correct output')


if __name__ == '__main__':
    unittest.main()
