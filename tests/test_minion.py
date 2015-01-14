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
        clean_directory()

    def test_note(self):
        ''' Test creating a default note. '''
        minion.minion_note(_TEST_ARGS)

    def test_here(self):
        ''' Test creating a default note in the current directory. 
        
        Messy. May re-add later, when sure that cleanup 
        won't be destructive.
        
        '''
        pass
        # minion.minion_here(_TEST_ARGS)

    def test_remind(self):
        ''' Test create a reminder. 
        Functionally no different that test note,
        but has a different entrypoint.
        '''
        minion.minion_remind(_TEST_ARGS)

    def test_template(self):
        ''' Test creating a note from a template.'''
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

    def test_open(self):
        ''' Just make sure it doesn't explode.'''
        minion.minion_open(_TEST_ARGS)

    def test_openall(self):
        ''' Just make sure it doesn't explode.'''
        minion.minion_openall(_TEST_ARGS)

    def test_strays(self):
        ''' Just make sure it doesn't explode.'''
        # Interactive method is distruptive. 
        # Disabled unless needed.
        # minion.minion_strays(_TEST_ARGS)
        pass

    def test_view(self):
        ''' Just make sure it doesn't explode.'''
        minion.minion_view(_TEST_ARGS)

    def test_summary(self):
        ''' Just make sure it doesn't explode.'''
        minion.minion_summary(_TEST_ARGS)


if __name__ == '__main__':
    unittest.main()
