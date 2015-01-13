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

# Quick = True avoids opening editor during testing...
_TEST_ARGS = {'--archives': False,
 '--config': '~/.minion',
 '--days': None,
 '--files': False,
 '--folder': None,
 '--help': False,
 '--max': '10',
'--quick': True,
 '--template': None,
 '--version': False,
 '--year': None,
 '<command>': None,
 '<comment>': [],
 '<filename>': None,
 '<log>': None,
 '<template>': [],
 '<text>': ['testing'],
 'collect': False,
 'command': False,
 'count': False,
 'dates': False,
 'favorites': False,
 'find': False,
 'folder': False,
 'folders': False,
 'here': False,
 'last': False,
 'list': False,
 'log': False,
 'note': True,
 'open': False,
 'openall': False,
 'recent': False,
 'remind': False,
 'sample': False,
 'sort': False,
 'strays': False,
 'summary': False,
 'tags': False,
 'template': False,
 'view': False}

# Use custom mock settings.
@patch('brain_of_minion.get_setting', new=mock_get_setting)
class TestMinionMethods(unittest.TestCase):
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
        TestMinionMethods.clean_directory()

        # Create it elsewhere than the inbox.
        PARAMS = {
            'topic_fragments': [],
            'note_template': 'journal',
            'notes_dir': TEST_DATA_NOT_INBOX,
            'quick': True
        }
        args = _TEST_ARGS
        args.update({
            '<template>': ['journal'],
            '<text>':'',
        })

        minion.minion_template(args)

if __name__ == '__main__':
    unittest.main()
