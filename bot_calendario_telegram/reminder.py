# -*- coding: utf-8 -*-
"""
Interact with a databae of events.

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
import reminder_database_model as db_model
import peewee


# === Reminder Class ===
class Reminder(object):
    """
    Checks and modifies a database.

    Methods:

    * initialize - Initialize the database object.
    * connect - Connect to the database.
    * close - Close the connection.
    * save_event - Save the event in the data base.
    * update_event - Updates an existing event.
    * get_event - Get the event from the data base.
    * delete_event - Delete event from Database.
    * next_event - Return nearest event.
    * get_all_events - Return all events sorted by date.
    """

    # === Initialize connection ===
    def initialize(self, db_name):
        """
        Initialize the database object.

        Sets the database name for connecting to it later

        Args:

        * db_name - The database name
        """
        db_model.database.init(db_name)

    # === Connect ===
    def connect(self):
        """
        Connect to the database.

        Starts the connection to perform queris to the database.
        """
        db_model.database.connect()

    # === Close connection ===
    def close(self):
        """
        Close the connection.

        Closes the connection after the database use.
        """
        db_model.database.close()

    # === Save event ===
    def save_event(self, id_event, date_event):
        """
        Save the event in the data base.

        Performs a query sentence to save the event in the data base.

        Args:

        * id_event - ID of the event
        * event_date - Reminder date of the event

        Returns:

        * The inserted object if everything went ok
        """
        try:
            insertion = db_model.Event.create(
                id_event=id_event, date_event=date_event)
        except peewee.IntegrityError as e:
            raise
        else:
            return {insertion.id_event: insertion.date_event}

    def update_event(self, id_event, new_date_event):
        """
        Update an existing event.

        Performs an update query to to an existing event of the database

        Args:

        * id_event - The existing event id
        * new_date_event - The updated date

        Returns:

        * result - Number of rows updated (should be 1)
        """
        try:
            update = db_model.Event.update(date_event=new_date_event).where(
                db_model.Event.id_event == id_event)
            result = update.execute()
        except Exception as e:
            raise
        else:
            return result

    # === Delete event ===
    def delete_event(self, id_event):
        """
        Delete event from Database.

        Performs a query sentence to remove a tuple from the database.

        Args:

        * id_event - ID of the event

        Returns:

        * result - Number of rows deleted (should be 1)
        """
        try:
            result = db_model.Event.delete().where(
                db_model.Event.id_event == id_event).execute()
        except Exception as e:
            raise
        else:
            return result

    # === Get event ===
    def get_event(self, id_event):
        """
        Get the event from the data base.

        Performs a query sentence to get the event from the data base.

        Args:

        * id_event - ID of the event

        Returns:

        * selected - Dictionary of id_event: date_event as key: value
        """
        try:
            selected = {
                id_event: date_event
                for id, id_event, date_event in db_model.Event.select()
                .where(db_model.Event.id_event == id_event).tuples()
            }
        except Exception as e:
            raise
        else:
            return selected

    # === Next event ===
    def next_event(self):
        """
        Return nearest event.

        Performs a query sentence to get the nearest event from the data base.

        Returns:

        * selected - Dictionary of id_event: date_event as key: value
        """
        try:
            selected = {
                id_event: date_event
                for id, id_event, date_event in db_model.Event.select()
                .order_by(db_model.Event.date_event).limit(1).tuples()
            }
        except Exception as e:
            raise
        else:
            return selected

    # === Get all events ====
    def get_all_events(self):
        """
        Return all events sorted by date.

        Performs a query sentence to get every event from the data base.

        Returns:

        * events - Dictionaries of id_event: date_event as key: value for each
        event
        """
        try:
            events = {
                id_event: date_event
                for id, id_event, date_event in db_model.Event.select()
                .order_by(db_model.Event.date_event).tuples()
            }
        except Exception as e:
            raise
        else:
            return events
