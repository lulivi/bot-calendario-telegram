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

    # === Constructor ===
    def __init__(self, db_file):
        """
        Constructor.

        Asign the data base path to a private variable.

        Args:

        * db_file - Data base path
        """
        self.__db_file = db_file

    # === Open connection ===
    def _open_connection(self):
        """
        Connect to the database.

        Creates a cursor from the connection to iterate and execute query
        sentences.
        """
        try:

            self.__db_connection = sqlite3.connect(self.__db_file)
            self.__db_connection.row_factory = sqlite3.Row
            self.__db_cursor = self.__db_connection.cursor()

        except Exception as e:
            raise

    # === Close connection ===
    def _close_connection(self):
        """
        Close the connection.

        Simple function to close the connection.
        """
        try:

            self.__db_connection.close()

        except Exception as e:
            raise

    # === Save event ===
    def save_event(self, id_event, event_date, preserve=True):
        """
        Save the event in the data base.

        Perform a query sentence to save the event in the data base.

        Args:

        * id_event - ID of the event
        * event_date - Reminder date of the event

        Returns:

        * -1 If there was any exception
        *  0 If everything were correct
        """
        try:
            self._open_connection()

            self.__db_cursor.execute('INSERT INTO EVENTS VALUES(?, ?)',
                                     (id_event, event_date))
            if preserve:
                self.__db_connection.commit()

            self._close_connection()
        except Exception as e:
            return -1
        else:
            return 0

    # === Get event ===
    def get_event(self, id_event):
        """
        Get the event from the data base.

        Perform a query sentence to get the event from the data base.

        Args:

        * id_event - ID of the event

        Returns:

        * -1 If there was any exception
        * date_event If everything were correct
        """
        try:
            self._open_connection()

            selected_event = {}
            selected_event = self.__db_cursor.execute(
                'SELECT EventDate FROM EVENTS WHERE EventId = ?',
                id_event).fetchone()

            self._close_connection()
        except Exception as e:
            return -1
        else:
            return selected_event['EventDate']

    # === Delete event ===
    def delete_event(self, id_event, preserve=True):
        """
        Delete event from Database.

        Perform a query sentence to remove a touple from the data base.

        Args:

        * id_event - ID of the event
        * preserve - If it should execute the query (testing purposes)
        DEFAULT: True

        Returns:

        * -1 If there was any exception
        *  0 If everything were correct
        """
        try:
            self._open_connection()

            self.__db_cursor.execute(
                'DELETE FROM EVENTS WHERE EventId = ?', id_event).fetchone()
            if preserve:
                self.__db_connection.commit()

            self._close_connection()
        except Exception as e:
            return -1
        else:
            return 0

    # === Next event ===
    def next_event(self):
        """
        Nearest event.

        Perform a query sentence to get the nearest event from the data base.

        Returns:

        * -1 If there was any exception
        * next_event If everything was fine
        """
        try:
            self._open_connection()
            next_event = self.__db_cursor.execute(
                'SELECT * FROM EVENTS ORDER BY EventDate').fetchone()

            self._close_connection()

            dict_next_event = dict(next_event)
        except Exception as e:
            return -1
        else:
            return dict_next_event

    # === Get all events ====
    def get_all_events(self, date_sorted=True):
        """
        Return all events sorted by date.

        Perform a query sentence to get every event from the data base.

        Args:

        * date_sorted - If want the results sorted by date DEFAULT: True

        Returns:

        * -1 If there was any exception
        * all_events If everything was fine
        """
        try:
            self._open_connection()
            all_events = self.__db_cursor.execute(
                'SELECT * from EVENTS ORDER BY EventDate;').fetchall()

            self._close_connection()

            dict_all_events = dict(all_events)
        except Exception as e:
            return -1
        else:
            return dict_all_events
