#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Remainder python module.

Checks in a data base when an event needs to be reminded.
"""

# External imports
import sqlite3


# === Reminder Class ===
class Reminder:
    """
    Checks and modifies a data base for geting and saving events.

    Methods:

    * save_event
    * get_event
    * delete_event
    * next_event
    * get_all_events
    """

    __db_connection = None
    __db_cursor = None
    __db_file = None

    # ===Constructor===
    def __init__(self, db_file):
        """Constructor."""
        self.__db_file = db_file

    # ===Open connection===
    def _open_connection(self):
        """Connect to the database."""
        self.__db_connection = sqlite3.connect(self.__db_file)
        self.__db_connection.row_factory = sqlite3.Row
        self.__db_cursor = self.__db_connection.cursor()

    # ===Close connection===
    def _close_connection(self):
        """Close the connection without saving."""
        self.__db_connection.close()

    # ===Save event===
    def save_event(self, event_id, event_date, preserve=True):
        """Save the event in the data base."""
        try:
            self._open_connection()

            self.__db_cursor.execute('INSERT INTO EVENTS VALUES(?, ?)',
                                     (event_id, event_date))
            if preserve:
                self.__db_connection.commit()

            self._close_connection()
        except Exception as e:
            raise
            return -1
        else:
            return 0

    # ===Get event===
    def get_event(self, event_id):
        """Get the event from the data base."""
        try:
            self._open_connection()

            selected_event = {}
            selected_event = self.__db_cursor.execute(
                'SELECT EventDate FROM EVENTS WHERE EventId = ?',
                event_id).fetchone()

            self._close_connection()
        except Exception as e:
            raise
            return -1
        else:
            return selected_event['EventDate']

    # ===Delete event===
    def delete_event(self, event_id, preserve=True):
        """Delete the event."""
        try:
            self._open_connection()

            self.__db_cursor.execute(
                'DELETE FROM EVENTS WHERE EventId = ?', event_id).fetchone()
            if preserve:
                self.__db_connection.commit()

            self._close_connection()
        except Exception as e:
            raise
            return -1
        else:
            return 0

    # Next event
    def next_event(self):
        """Return next event in the data base."""
        try:
            self._open_connection()
            next_event = self.__db_cursor.execute(
                'SELECT * FROM EVENTS ORDER BY EventDate').fetchone()

            self._close_connection()

            dict_next_event = dict(next_event)
        except Exception as e:
            raise
            return -1
        else:
            return dict_next_event

    # Gett all events
    def get_all_events(self, date_sorted=True):
        """Return all events sorted by date."""
        try:
            self._open_connection()
            all_events = self.__db_cursor.execute(
                'SELECT * from EVENTS ORDER BY EventDate;').fetchall()

            self._close_connection()

            dict_all_events = dict(all_events)
        except Exception as e:
            raise
            return -1
        else:
            return dict_all_events
