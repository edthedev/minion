'''Unit tests for Minion command line'''
import os
import sys
import unittest
from datetime import date
from mock import MagicMock, mock_open, patch, call

# Our stuff
# Ensure we can load the brain library.
sys.path.insert(0, os.path.abspath('.'))
import minion
from tests.mock_data import *

# Use custom mock settings.
@patch('brain_of_minion.get_setting', new=mock_get_setting)
class TestFileStuff(unittest.TestCase):
    ''' Run tests that create or look for files.'''

    @staticmethod
    def clean_directory():
        os.system('rm -rf ' + TEST_DATA_DIRECTORY + '/*')

    def setUp(self):
        try:
            os.mkdir(TEST_DATA_DIRECTORY)
        except OSError:
            print ''

    def test_template(self):
        ''' Test creating a note from a template.'''
        # Start clean
        TestFileStuff.clean_directory()

        # Create it elsewhere than the inbox.
        PARAMS = {
            'topic_fragments': ['testing', 'note', 'template'],
            'note_template': 'journal',
            'notes_dir': TEST_DATA_NOT_INBOX,
            'quick': True
        }

        minion.minion_template()
