'''Unit tests for Brain of Minion '''
import os
import sys
import unittest
from datetime import date
from mock import MagicMock, mock_open, patch, call

# Our stuff
# Ensure we can load the brain library.
sys.path.insert(0, os.path.abspath('.'))
import brain_of_minion as brain
from tests.mock_data import *

# Mock objects
my_mock_open = mock_open()
my_mock_os = MagicMock()


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

    def test_template_duplicates(self):
        ''' Test that template does not recreate a file
        if a file with the same name alreadye exists. '''

        # Start clean
        TestFileStuff.clean_directory()

        # Create it elsewhere than the inbox.
        params = {
            'topic_fragments': ['testing', 'note', 'template'],
            'note_template': 'note',
            'notes_dir': TEST_DATA_NOT_INBOX,
            'quick': True
        }
        brain.new_note_interactive(**params)

        # Then create another copy, without specifying where.
        params = {
            'topic_fragments': ['testing', 'note', 'template'],
            'note_template': 'note',
            'quick': True
        }
        brain.new_note_interactive(**params)

        dir_contents = os.listdir(TEST_DATA_NOT_INBOX)
        # Inbox exists.
        self.assertEqual(len(dir_contents), 1, '1 in not_inbox')

        # See if we can find more than one.
        params = {
            'filter': ['testing', 'note', 'template'],
        }
        results = brain.find_files(**params)
        self.assertEqual(len(results), 1,
                         'note_template created ' + str(len(results)) +
                         ' files instead of exactly 1.')

    def test_strays(self):
        ''' Run the strays method. '''

        # Arrange
        TestFileStuff.clean_directory()
        # Since we didn't tag it, it is considered 'stray'
        _, _ = brain.create_new_note(TEST_TOPIC, note_template='note')

        # Act
        results = brain.list_stray_files()

        # Assert
        self.assertEqual(len(results), 1)

    def test_archive_note(self):
        ''' archive a note.'''
        # Make a note
        TestFileStuff.clean_directory()
        file_path, _ = brain.create_new_note(TEST_TOPIC, note_template='note')
        dir_contents = os.listdir(TEST_DATA_INBOX)
        # Inbox exists.
        self.assertEqual(len(dir_contents), 1, '1 in inbox')

        # Tag and find it.
        brain.add_tags_to_file(TEST_TAGS_IN, file_path)
        tags_found = brain.get_tags(file_path)
        for tag in TEST_TAGS_OUT:
            self.assertTrue(tag in tags_found, msg='Find tag ' + tag)

        args = {
            'keyword_string': ' '.join(TEST_TAGS_IN),
            'archives': False,
            'full_text': True,
        }

        EXPECTED_MATCH = '/tmp/test_minion/inbox/This-is-a-test-topic.txt'
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 1, 'found file by tags')
        self.assertEqual(match_files, [EXPECTED_MATCH])

        # Try finding it again, because it was the last modified file.
        match_file = brain.get_last_modified()
        self.assertEqual(match_file, EXPECTED_MATCH)

        # Archive it.
        brain.archive(file_path)

        # Is it gone (from tag find?)
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 0, 'archived, so cannot find')

    def test_find_date_in_filename(self):
        ''' Find a date in a filename. '''

        os.mkdir(TEST_DATA_INBOX)
        f = open(TEST_FILENAME_WITH_DATE, 'w')
        f.writelines(['Some random content.'])
        f.close()

        # Can we find the note?
        args = {
            'keyword_string': TEST_DATE_STRING,
            'archives': False,
            'full_text': True,
        }
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 1, msg='date in filename')

    def test_find_note(self):
        ''' Make a note and find it again. '''
        # Make a note
        TestFileStuff.clean_directory()
        file_path, _ = brain.create_new_note(TEST_TOPIC, 'note')
        # Did we make a note?
        file_count = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(len(file_count), 1, msg='os.listdir')

        # Tag it for retrieval
        brain.add_tags_to_file(TEST_TAGS_IN, file_path)

        # Can we find the note?
        args = {
            'keyword_string': ' '.join(TEST_TAGS_IN),
            'archives': False,
            'full_text': True,
        }
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 1, msg='get_keyword_files')

        # Can we remove the tags?
        brain.remove_tags_from_file(TEST_TAGS_IN, file_path)

        # This time we should not find it.
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 0, 'get_keyword_files find 0')

    def test_log_a_string(self):
        ''' Give the Minion log method a try. '''
        # Arrange
        TestFileStuff.clean_directory()
        inbox_content = os.listdir(brain.get_inbox()),
        self.assertEqual(
            inbox_content,
            ([], ),
            'inbox did not start clean: ' + str(inbox_content))

        # Act
        params = {
            'filter': TEST_LOG_FILTER,
            'archives': False,
        }
        filename, match_files = brain.choose_file(**params)

        # Log a thing...
        params = {
            'filename': filename,
            'line': TEST_LOG_LINE,
        }
        brain.log_line_to_file(**params)

        # Assert
        # Can we find the log file.
        params = {
            'keyword_string': LOG_NAME,
            'archives': False,
            'full_text': False,
        }
        match_files = brain.get_keyword_files(**params)
        self.assertEqual(len(match_files), 1, msg='find log file: ' + LOG_NAME)

    def test_string_to_file_name_with_default_filename_template(self):
        # Arrange
        topic = "one two three four"
        filename_template = "{topic}"
        expected_filename = "one-two-three-four.txt"
        # Act
        actual_filename = brain.string_to_file_name(topic, filename_template)
        # Assert
        self.assertEqual(expected_filename, actual_filename)

    def test_string_to_file_name_with_filename_template_with_date(self):
        # Arrange
        topic = "one two three"
        filename_template = "{today}-{topic}"
        today_string = date.today().isoformat()
        expected_filename = today_string + "-one-two-three.txt"
        # Act
        actual_filename = brain.string_to_file_name(topic, filename_template)
        # Assert
        self.assertEqual(expected_filename, actual_filename)

    def test_create_new_note(self):
        TestFileStuff.clean_directory()

        file_path, _ = brain.create_new_note(TEST_TOPIC, note_template='note')
        file_count = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(len(file_count), 1)
        self.assertEqual(file_path, TEST_FILE_PATH)

        content = brain.get_file_content(TEST_FILE_PATH)
        self.assertTrue(TEST_FILE_INITIAL_CONTENT in content)

    def test_create_new_note_with_default_template_and_filename(self):
        # Arrange
        TestFileStuff.clean_directory()
        topic = 'test note 347'
        expected_filename = 'test-note-347.txt'
        expected_line = 4
        # Act
        (actual_filename, actual_line) = brain.create_new_note(
            topic,
            notes_dir=TEST_DATA_DIRECTORY)
        # Assert
        # assert on return values
        self.assertEqual(TEST_DATA_DIRECTORY + '/' + expected_filename,
                         actual_filename)
        self.assertEqual(expected_line, actual_line)
        # assert the file was successfully created
        files = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(expected_filename, files[0])

    def test_create_new_note_with_mildly_complex_filename_template(self):
        # Arrange
        TestFileStuff.clean_directory()
        topic = 'test note 348'
        today_date = date.today()
        expected_filename = today_date.isoformat() + '-test-note-348.txt'
        expected_line = 4
        # Act
        (actual_filename, actual_line) = brain.create_new_note(
            topic,
            notes_dir=TEST_DATA_DIRECTORY,
            filename_template='{today}-{topic}')
        # Assert
        self.assertEqual(TEST_DATA_DIRECTORY + '/' + expected_filename,
                         actual_filename)
        self.assertEqual(expected_line, actual_line)
        files = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(expected_filename, files[0])

    def test_list_recent_with_recent_file(self):
        # Arrange
        TestFileStuff.clean_directory()
        recent_file_path, _ = brain.create_new_note(TEST_TOPIC, 'note')
        expected = dict()
        expected[datetime.today().date()] = [recent_file_path]
        # Act
        match_files = brain.find_files(filter=[], days=1)
        actual = brain.list_recent(match_files)
        # Assert
        self.assertEqual(expected, actual)

    def test_list_recent_with_old_file(self):
        if not sys.platform == 'darwin':
            # Arrange
            TestFileStuff.clean_directory()
            recent_file_path, _ = brain.create_new_note(TEST_TOPIC, 'note')
            old_date = 2014-04-01
            os.utime(recent_file_path, (old_date, old_date))
            expected = dict()

            # Act
            match_files = brain.find_files(filter=[], days=1)
            actual = brain.list_recent(match_files)

            # Assert
            self.assertEqual(expected, actual)

    def tearDown(self):
        os.system('rm -rf ' + TEST_DATA_DIRECTORY)


class TestParsers(unittest.TestCase):
    ''' Test methods that parse through file contents looking for things.'''

    def test_get_first_date(self):
        first_date = brain.get_first_date(TEST_FILE_CONTENT)
        self.assertEqual(first_date, EXPECTED_DATE)

    def test_get_first_date_with_multiple_dates(self):
        # Arrange
        test_file_content = "\
            2014-08-08 Some title\n\
            =====================\n\
            :date: 2014-08-12\n"
        expected_date = datetime(2014, 8, 8, 0, 0)
        # Act
        actual_date = brain.get_first_date(test_file_content)
        # Assert
        self.assertEqual(expected_date, actual_date)

    def test_get_unique_dates_with_different_formats(self):
        # Arrange
        test_file_content = "\
            2014-08-08 Some title\n\
            =====================\n\
            12/15/2014\n\
            12/26/14\n"
        expected_dates = [
            date(2014, 8, 8),
            date(2014, 12, 15),
            date(2014, 12, 26)]
        # Act
        actual_dates = brain.get_unique_dates(test_file_content)

        # Assert
        self.assertEqual(expected_dates, actual_dates)

    def test_get_unique_dates_simple(self):
        # Arrange
        test_file_content = "\
            2014-08-08 Some title\n\
            =====================\n\
            :date: 2014-08-12\n"
        expected_dates = [
            date(2014, 8, 8),
            date(2014, 8, 12)]
        # Act
        actual_dates = brain.get_unique_dates(test_file_content)

        # Assert
        self.assertEqual(expected_dates, actual_dates)

    def test_get_content_tags(self):
        result = brain.get_content_tags(TEST_FILE_CONTENT_WITH_TAGS)
        self.assertEqual(TEST_TAGS_OUT, result)


class TestGetSetting(unittest.TestCase):

    def test_get_setting(self):
        ''' Make sure some settings can load.'''
        settings = brain.get_settings()

        self.assertNotEqual(None, settings.get('notes', 'home'))
        self.assertNotEqual(None, settings.get('notes', 'favorites'))
        # Default composition settings
        self.assertNotEqual(None, settings.get('compose', 'templates'))
        self.assertNotEqual(None, settings.get('compose', 'extension'))
        self.assertNotEqual(None, settings.get('compose', 'editor'))
        self.assertNotEqual(None, settings.get('compose', 'tagline'))
        # Default date format
        self.assertNotEqual(None, settings.get('date', 'format'))

    def test_get_sort_actions_settings(self):
        ''' Retrieve all the options in the 'sort_actions' section'''
        # Arrange
        # Clean and fill 'sort_actions' section for test purposes
        brain.GLOBAL_SETTINGS.remove_section('sort_actions')
        brain.GLOBAL_SETTINGS.add_section('sort_actions')
        brain.GLOBAL_SETTINGS.set('sort_actions', 't', '>trash')
        brain.GLOBAL_SETTINGS.set('sort_actions', 'w', '>wiki')
        expected_actions = [('t', '>trash'), ('w', '>wiki')]

        # Act
        actual_actions = brain.parse_sort_actions_settings()

        # Assert
        self.assertEqual(expected_actions, actual_actions)


@patch('__builtin__.open', new_callable=mock_open)
@patch('brain_of_minion.get_setting', new=mock_get_setting)
# @patch('os.mkdir')
class TestRemind(unittest.TestCase):
    ''' Doing a bit of fancy mock stuff for remind. '''

    def setUp(self):
        try:
            os.mkdir(TEST_DATA_DIRECTORY)
        except OSError:
            print ''

    def test_remind(self, open_mock):
        ''' Test setting a reminder. '''
        # Arrange
        TestFileStuff.clean_directory()

        # Act
        brain.remind("Remind me of this thing")
        test_filename = os.path.join(
            os.path.expanduser('~'),
            TEST_DATA_DIRECTORY + '/inbox/Remind-me-of-this-thing.txt')

        # Assert
        # Remind should have been called.
        open_mock.assert_has_calls([call(test_filename, 'a')])

        # No files exist,
        # because we mocked over the bit that would have written the file
        match_files = brain.get_inbox_files()
        self.assertEqual(len(match_files), 0)


class TestTags(unittest.TestCase):
    ''' Test suite for tag handling. '''

    def test_create_tag_line(self):
        result = brain.create_tag_line(TEST_TAGS_IN)
        self.assertEqual(result, TEST_TAG_LINE)

    def test_add_tags(self):
        args = {'tags': TEST_TAGS_IN,
                'content': TEST_FILE_CONTENT}
        result = brain.add_tags(**args)
        self.assertEqual(result, TEST_FILE_CONTENT_WITH_TAGS)

    def test_remove_tags(self):
        args = {'tags': TEST_REMOVE_TAGS,
                'content': TEST_FILE_CONTENT_WITH_TAGS}
        result = brain.remove_tags_from_content(**args)
        self.assertEqual(result, TEST_FILE_CONTENT_WITH_ONE_TAG)

    def test_has_tag(self):
        args = {
            'content': TEST_FILE_CONTENT_WITH_TAGS,
            'tag': TEST_TAG,
            }
        self.assertTrue(brain.content_has_tag(**args))

        args['tag'] = TEST_GIBBERISH
        self.assertFalse(brain.content_has_tag(**args))

if __name__ == '__main__':
    unittest.main()
