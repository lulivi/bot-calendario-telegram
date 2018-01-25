"""Interact with a databae of events."""

# External imports
import peewee
from urllib import parse

import context
import bot_calendario_telegram.reminder_database_model as db_model

assert context


# === Reminder Class ===
class Reminder(object):
    """Checks and modifies a database.

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
    def initialize(self, database):
        """Initialize the database proxy object.

        Sets the database config parameters for connecting to it later

        Args:

        * database - Database object already created
        """
        db_model.database_proxy.initialize(database)

    # === Connect ===
    def connect(self):
        """Connect to the database.

        Starts the connection to perform queries to the database.
        """
        db_model.database_proxy.connect()

    # === Close connection ===
    def close(self):
        """Close the connection.

        Closes the connection after the database use.
        """
        db_model.database_proxy.close()

    # === Save event ===
    def save_event(self, event_id, reminder_datetime):
        """Save the event in the data base.

        Performs a query sentence to save the event in the data base.

        Args:

        * event_id - ID of the event
        * event_date - Reminder date of the event

        Returns:

        * The inserted object if everything went ok
        """
        try:
            insertion = db_model.EventReminder.create(
                event_id=event_id, reminder_datetime=reminder_datetime)
        except peewee.IntegrityError as e:
            raise
        else:
            return {
                'event_id': insertion.event_id,
                'reminder_datetime': insertion.reminder_datetime
            }

    def update_event(self, event_id, new_reminder_datetime):
        """Update an existing event.

        Performs an update query to to an existing event of the database

        Args:

        * event_id - The existing event id
        * new_reminder_datetime - The updated date

        Returns:

        * result - Number of rows updated (should be 1)
        """
        update = db_model.EventReminder.update(
            reminder_datetime=new_reminder_datetime).where(
                db_model.EventReminder.event_id == event_id)
        result = update.execute()

        return result

    # === Delete event ===
    def delete_event(self, event_id):
        """Delete event from Database.

        Performs a query sentence to remove a tuple from the database.

        Args:

        * event_id - ID of the event

        Returns:

        * result - Number of rows deleted (should be 1)
        """
        result = db_model.EventReminder.delete().where(
            db_model.EventReminder.event_id == event_id).execute()

        return result

    # === Get event ===
    def get_event(self, event_id):
        """Get the event from the data base.

        Performs a query sentence to get the event from the data base.

        Args:

        * event_id - ID of the event

        Returns:

        * selected - Dictionary of event_id: reminder_datetime as key: value
        """
        event = db_model.EventReminder.select().where(
            db_model.EventReminder.event_id == event_id).dicts()

        if event:
            result = event[0]
            result.pop('id')
        else:
            result = {}

        return result

    # === Next event ===
    def next_event(self):
        """Return nearest event.

        Performs a query sentence to get the nearest event from the data base.

        Returns:

        * selected - Dictionary of event_id: reminder_datetime as key: value
        """
        next_event = db_model.EventReminder.select().order_by(
            db_model.EventReminder.reminder_datetime).limit(1).dicts()

        if next_event:
            result = next_event[0]
            result.pop('id')
        else:
            result = {}

        return result

    # === Get all events ====
    def get_all_events(self):
        """Return all events sorted by date.

        Performs a query sentence to get every event from the data base.

        Returns:

            events - A list of events ({'event_id': event_id,
            'reminder_datetime': reminder_datetime})
        """
        events = [{
            'event_id': event_id,
            'reminder_datetime': reminder_datetime
        }
                  for id, event_id, reminder_datetime in
                  db_model.EventReminder.select()
                  .order_by(db_model.EventReminder.reminder_datetime).tuples()]

        return events

    def get_all_events_count(self):
        """Return the number of saved reminders."""
        return db_model.EventReminder.select().count()
