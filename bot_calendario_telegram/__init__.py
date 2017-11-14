# -*- coding: utf-8 -*-
"""
Define full path for a file used in this module.

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
import os


# Obtain current file directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Obtain project root path
project_abs_path = '/'.join(working_dir.split('/')[:-1])

# Variables for testing
TEST_REMINDER_DATA_PATH = project_abs_path + '/data/test_reminder_data.json'
