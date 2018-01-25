"""Global variables of bot_calendario_telegram module."""

import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TESTING_VARS = {
    'REMINDER_DATA_FILE': BASE_DIR + '/data/test_reminder_data.json',
    'DB_NAME': BASE_DIR + '/data/test_reminder_database.db'
}

REMINDER_REST_API_PORT = config('PORT', default=17995, cast=int)

HEROKU_PG_DATABASE_URL = config('DATABASE_URL', default=None)

NEXTCLOUD_MIDLEWARE_URL = 'https://middleware-nextcloud.herokuapp.com/'

BOT_TOKEN = config('TG_CALENDAR_BOT_TOKEN', cast=str)
