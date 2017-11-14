# -*- coding: utf-8 -*-
"""
Short description of the module.

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

import sys
import os

# Obtain project root path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Variables for testing
TEST_REMINDER_DATA_PATH = project_root + '/data/test_reminder_data.json'
TEST_DATABASE_PATH = project_root + '/data/test_reminder_database.db'

# For finding modules to test
sys.path.insert(0, project_root + '/bot_calendario_telegram')
