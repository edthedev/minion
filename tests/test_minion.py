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

def setup_test_dir():
    ''' Make sure content directory exists. '''
    try:
        os.mkdir(TEST_DATA_DIRECTORY)
    except OSError:
        print ''

def clean_directory():
    ''' Make sure content directory is empty. '''
    os.system('rm -rf ' + TEST_DATA_DIRECTORY + '/*')

# Use custom mock settings.
@patch('brain_of_minion.get_setting', new=mock_get_setting)
class TestMinionWrite(unittest.TestCase):
    ''' Run tests that create or look for files.'''

    def setUp(self):
        setup_test_dir()

    def test_template(self):
        ''' Test creating a note from a template.'''
        # Start clean
        clean_directory()

        # Create it elsewhere than the inbox.
        args = _TEST_ARGS
        args.update({
            '<template>': ['journal'],
            '<text>':'',
        })

        minion.minion_template(args)

@patch('brain_of_minion.get_setting', new=mock_get_setting)
class TestMinionListMethods(unittest.TestCase):
    ''' Test methods that find, list, etc. '''
    def setUp(self):
        setup_test_dir()

    def test_summary(self):
        ''' Just make sure it doesn't explode.'''
        minion.minion_summary(_TEST_ARGS)


if __name__ == '__main__':
    unittest.main()
