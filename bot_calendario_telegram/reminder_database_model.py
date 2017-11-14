# -*- coding: UTF-8 -*-
"""Reminder database model."""
import peewee

database = peewee.SqliteDatabase(None)


class BaseModel(peewee.Model):
    """Data base class."""

    class Meta:
        """Meta class for the database."""

        database = database


class Event(BaseModel):
    """Model for `event` table."""

    id = peewee.PrimaryKeyField()
    id_event = peewee.CharField()
    date_event = peewee.DateTimeField()

    class Meta:
        """Meta class for `events`."""

        db_table = 'event'
