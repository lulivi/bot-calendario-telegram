import sys
import os

# Obtain current file directory
working_dir = os.path.dirname(os.path.abspath(__file__))

# Obtain project root path
project_abs_path = '/'.join(working_dir.split('/')[:-1])

# Variables for testing
TEST_REMINDER_DATA_PATH = project_abs_path + '/data/test_reminder_data.json'
