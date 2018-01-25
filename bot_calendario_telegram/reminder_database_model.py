"""Reminder database model."""

import peewee

database_proxy = peewee.Proxy()


class BaseModel(peewee.Model):
    """Data base class."""

    class Meta:
        """Meta class for the database."""

        database = database_proxy


class EventReminder(BaseModel):
    """Model for event table."""

    id = peewee.PrimaryKeyField()
    event_id = peewee.CharField()
    reminder_datetime = peewee.DateTimeField(formats='%Y/%m/%d %H:%M')

    class Meta:
        """Meta class for events."""

        db_table = 'event_reminder'
