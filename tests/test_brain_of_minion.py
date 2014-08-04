'''Unit tests for Brain of Minion '''
import os
import sys
import unittest
import datetime
from mock import MagicMock, mock_open, patch, call

# Our stuff
# Ensure we can load the brain library.
sys.path.insert(0, os.path.abspath('.'))
import brain_of_minion as brain
from mock_data import mock_settings

from tests.mock_data import *

# Mock objects
my_mock_open = mock_open()
my_mock_os = MagicMock()


# Use custom mock settings.
@patch('brain_of_minion.get_settings', new=mock_settings)
class TestFileStuff(unittest.TestCase):
    ''' Run tests that create or look for files.
    '''

    @staticmethod
    def clean_directory():
        os.system('rm -rf ' + TEST_DATA_DIRECTORY + '/*')

    def setUp(self):
        os.mkdir(TEST_DATA_DIRECTORY)

    def test_archive_note(self):
        ''' archive a note.'''
        # Make a note
        TestFileStuff.clean_directory()
        file_path, _ = brain.create_new_note(TEST_TOPIC, template='note')
        file_count = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(len(file_count), 1)

        # Tag and find it.
        brain.add_tags_to_file(TEST_TAG_STRING, file_path)

        args = {
            'keyword_string': ' '.join(TEST_TAGS),
            'archives': False,
            'full_text': True,
        }

        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 1)

        # Archive it.
        brain.archive(file_path)

        # Is it gone (from tag find?)
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 0)

    def test_find_note(self):
        ''' Make a note and find it again. '''
        # Make a note
        TestFileStuff.clean_directory()
        file_path, _ = brain.create_new_note(TEST_TOPIC, template='note')
        # Did we make a note?
        file_count = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(len(file_count), 1)

        # Tag it for retrieval
        brain.add_tags_to_file(TEST_TAG_STRING, file_path)

        # Can we find the note?
        args = {
            'keyword_string': ' '.join(TEST_TAGS),
            'archives': False,
            'full_text': True,
        }
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 1)

        # Can we remove the tags?
        brain.remove_tags_from_file(TEST_TAGS, file_path)

        # This time we should not find it.
        match_files = brain.get_keyword_files(**args)
        self.assertEqual(len(match_files), 1)

    def test_create_new_note(self):
        TestFileStuff.clean_directory()

        filename = brain.string_to_file_name(TEST_TOPIC)
        self.assertEqual(filename, TEST_FILENAME)

        file_path = brain.get_filename_for_title(TEST_TOPIC, notes_dir=None)
        self.assertEqual(file_path, TEST_FILE_PATH)

        file_path, _ = brain.create_new_note(TEST_TOPIC, template='note')
        file_count = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(len(file_count), 1)
        self.assertEqual(file_path, TEST_FILE_PATH)

        content = brain.get_file_content(TEST_FILE_PATH)
        self.assertTrue(TEST_FILE_INITIAL_CONTENT in content)

    def test_create_note_internal_with_simple_template(self):
        # Arrange
        TestFileStuff.clean_directory()
        template_text = '{topic}\n:date: {today}\n'
        topic = 'test note 347'
        expected_filename = 'test-note-347.txt'
        expected_line = 4
        # Act
        (actual_filename, actual_line) = brain.create_note_internal(
            topic,
            template_text,
            TEST_DATA_DIRECTORY)
        # Assert
        # assert on return values
        self.assertEqual(TEST_DATA_DIRECTORY + '/' + expected_filename,
                         actual_filename)
        self.assertEqual(expected_line, actual_line)
        # assert the file was successfully created
        files = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(expected_filename, files[0])
        # TODO: assert the content of the file

    def test_create_note_internal_with_mildly_more_complex_template(self):
        # Arrange
        TestFileStuff.clean_directory()
        template_text = '{topic}~~{today}\n{topic_underline}\n:date: {today}\n'
        topic = 'test note 348'
        today_date = datetime.date.today()
        expected_filename = 'test-note-348~~' + today_date.isoformat() + '.txt'
        expected_line = 5
        # Act
        (actual_filename, actual_line) = brain.create_note_internal(
            topic,
            template_text,
            TEST_DATA_DIRECTORY)
        # Assert
        self.assertEqual(TEST_DATA_DIRECTORY + '/' + expected_filename,
                         actual_filename)
        self.assertEqual(expected_line, actual_line)
        files = os.listdir(TEST_DATA_DIRECTORY)
        self.assertEqual(expected_filename, files[0])

    def tearDown(self):
        os.system('rm -rf ' + TEST_DATA_DIRECTORY)


class TestFetchMethods(unittest.TestCase):
    ''' Run some basic search methods.

    This is just a kick the tires kind of test set.
    We won't assert much - just make sure we run things to avoid typos.

    '''
    def test_strays(self):
        brain.list_stray_files()


class TestParsers(unittest.TestCase):
    ''' Test some methods that parse through file contents looking for things.
    '''
    def test_get_first_date(self):
        first_date = brain.get_first_date(TEST_FILE_CONTENT)
        self.assertEqual(first_date, EXPECTED_DATE)


# Tests
class TestGetSetting(unittest.TestCase):

    def test_get_title(self):
        ''' Confirm getting a title. '''
        title = brain.get_title_from_template_content(
            TEST_FILE_TEMPLATE_CONTENT)
        self.assertEqual(title, TEST_FILE_TITLE)

    # TODO: Test a full template fill in, including topic.

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


@patch('__builtin__.open', new_callable=mock_open)
@patch('brain_of_minion.get_settings', new=mock_settings)
@patch('os.mkdir')
class TestRemind(unittest.TestCase):
    def test_remind(self, mkdir_mock, open_mock):
        ''' Test setting a reminder. '''
        brain.remind("Remind me of this thing")
        test_filename = os.path.join(
            os.path.expanduser('~'),
            TEST_DATA_DIRECTORY + '/inbox/Remind-me-of-this-thing.txt')
        open_mock.assert_has_calls([call(test_filename, 'a')])


class TestTags(unittest.TestCase):
    ''' Test suite for tag handling. '''

    def test_create_tag_line(self):
        result = brain.create_tag_line(TEST_TAGS)
        self.assertEqual(result, TEST_TAG_LINE)

    def test_add_tags(self):
        args = {'tags': TEST_TAGS,
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
        self.assertTrue(
            brain.content_has_tag(**args)
            )

        args['tag'] = TEST_GIBBERISH
        self.assertFalse(
            brain.content_has_tag(**args)
            )

# class TestIsValidTag(unittest.TestCase):
#     def test_is_valid_tag(self):
#         # self.assertEqual(expected, isValidTag(tag))
#         assert False # TODO: implement your test here
#
# class TestSortByTag(unittest.TestCase):
#     def test_sort_by_tag(self):
#         # self.assertEqual(expected, sort_by_tag(file_list))
#         assert False # TODO: implement your test here
#
# class TestDisplayOutput(unittest.TestCase):
#     def test_display_output(self):
#         # self.assertEqual(expected,
#         #     display_output(title, output, by_tag, raw_files, max_display))
#         assert False # TODO: implement your test here
#
# class TestCleanOutput(unittest.TestCase):
#     def test_clean_output(self):
#         # self.assertEqual(expected, clean_output(output))
#         assert False # TODO: implement your test here
#
# class TestCleanString(unittest.TestCase):
#     def test_clean_string(self):
#         # self.assertEqual(expected, clean_string(output))
#         assert False # TODO: implement your test here
#
# class TestRemoveTagsFromString(unittest.TestCase):
#     def test_remove_tags_from_string(self):
#         # self.assertEqual(expected, remove_tags_from_string(filename))
#         assert False # TODO: implement your test here
#
# class TestGetMatchingFiles(unittest.TestCase):
#     def test_get_matching_files(self):
#         # self.assertEqual(expected,
#         #     getMatchingFiles(search_terms, file_list))
#         assert False # TODO: implement your test here
#
# class TestGetCurrentProjects(unittest.TestCase):
#     def test_get_current_projects(self):
#         # self.assertEqual(expected, getCurrentProjects())
#         assert False # TODO: implement your test here
#
# class TestLimitNotes(unittest.TestCase):
#     def test_limit_notes(self):
#         # self.assertEqual(expected, limit_notes(choice, notes, full))
#         assert False # TODO: implement your test here
#
# class TestRemoveNotes(unittest.TestCase):
#     def test_remove_notes(self):
#         # self.assertEqual(expected, remove_notes(file_list, terms))
#         assert False # TODO: implement your test here
#
# class TestGetAllFiles(unittest.TestCase):
#     def test_get_all_files(self):
#         # self.assertEqual(expected, getAllFiles(archives, folder))
#         assert False # TODO: implement your test here
#
# class TestCleanFileName(unittest.TestCase):
#     def test_clean_file_name(self):
#         # self.assertEqual(expected, clean_file_name(text))
#         assert False # TODO: implement your test here
#
# class TestGetViewer(unittest.TestCase):
#     def test_get_viewer(self):
#         # self.assertEqual(expected, get_viewer(filename))
#         assert False # TODO: implement your test here
#
# class TestGetEditor(unittest.TestCase):
#     def test_get_editor(self):
#         # self.assertEqual(
#         #     expected,
#         #     get_editor(filename, multiple, graphical, view))
#         assert False # TODO: implement your test here
#
# class TestOpenFile(unittest.TestCase):
#     def test_open_file(self):
#         # self.assertEqual(expected,
#         #     open_file(filename, line, multiple, graphical))
#         assert False # TODO: implement your test here
#
# class TestPreviewFile(unittest.TestCase):
#     def test_preview_file(self):
#         # self.assertEqual(expected, preview_file(filename))
#         assert False # TODO: implement your test here
#
# class TestGetDateFormat(unittest.TestCase):
#     def test_get_date_format(self):
#         # self.assertEqual(expected, get_date_format())
#         assert False # TODO: implement your test here
#
# class TestGetNotesHome(unittest.TestCase):
#     def test_get_notes_home(self):
#         # self.assertEqual(expected, get_notes_home())
#         assert False # TODO: implement your test here
#
# class TestGetInbox(unittest.TestCase):
#     def test_get_inbox(self):
#         # self.assertEqual(expected, get_inbox())
#         assert False # TODO: implement your test here
#
# class TestGetKeywordFiles(unittest.TestCase):
#     def test_get_keyword_files(self):
#         # self.assertEqual(expected, get_keyword_files(keyword_string))
#         assert False # TODO: implement your test here
#
# class TestGetInboxFiles(unittest.TestCase):
#     def test_get_inbox_files(self):
#         # self.assertEqual(expected, get_inbox_files())
#         assert False # TODO: implement your test here
#
# class TestChooseBox(unittest.TestCase):
#     def test_choose_box(self):
#         # self.assertEqual(expected, chooseBox(choice))
#         assert False # TODO: implement your test here
#
# class TestGetFolder(unittest.TestCase):
#     def test_get_folder(self):
#         # self.assertEqual(expected, get_folder(folder))
#         assert False # TODO: implement your test here
#
# class TestLimitNotesInteractive(unittest.TestCase):
#     def test_limit_notes_interactive(self):
#         # self.assertEqual(expected, limit_notes_interactive(notes))
#         assert False # TODO: implement your test here
#
# class TestGetCurrentMonth(unittest.TestCase):
#     def test_get_current_month(self):
#         # self.assertEqual(expected, getCurrentMonth())
#         assert False # TODO: implement your test here
#
# class TestGetNextMonth(unittest.TestCase):
#     def test_get_next_month(self):
#         # self.assertEqual(expected, getNextMonth())
#         assert False # TODO: implement your test here
#
# class TestGetMonthName(unittest.TestCase):
#     def test_get_month_name(self):
#         # self.assertEqual(expected, getMonthName(number))
#         assert False # TODO: implement your test here
#
# class TestGetUpcoming(unittest.TestCase):
#     def test_get_upcoming(self):
#         # self.assertEqual(expected, getUpcoming(full))
#         assert False # TODO: implement your test here
#
# class TestMakeProject(unittest.TestCase):
#     def test_make_project(self):
#         # self.assertEqual(expected, makeProject(filename))
#         assert False # TODO: implement your test here
#
# class TestExpandShortCommand(unittest.TestCase):
#     def test_expand_short_command(self):
#         # self.assertEqual(expected, expand_short_command(command))
#         assert False # TODO: implement your test here
#
# class TestApplyCommandToLine(unittest.TestCase):
#     def test_apply_command_to_line(self):
#         # self.assertEqual(expected,
#         #     applyCommandToLine(filename, line, command))
#         assert False # TODO: implement your test here
#
# class TestAddTagsToFile(unittest.TestCase):
#     def test_add_tags_to_file(self):
#         # self.assertEqual(expected, add_tags_to_file(tags, filename))
#         assert False # TODO: implement your test here
#
# class TestRemoveTagsFromFile(unittest.TestCase):
#     def test_remove_tags_from_file(self):
#         # self.assertEqual(expected, remove_tags_from_file(tags, filename))
#         assert False # TODO: implement your test here
#
# class TestArchive(unittest.TestCase):
#     def test_archive(self):
#         # self.assertEqual(expected, archive(filename))
#         assert False # TODO: implement your test here
#
# class TestApplyCommandToFile(unittest.TestCase):
#     def test_apply_command_to_file(self):
#         # self.assertEqual(expected, apply_command_to_file(filename, command))
#         assert False # TODO: implement your test here
#
# class TestReviewProjectInteractive(unittest.TestCase):
#     def test_review_project_interactive(self):
#         # self.assertEqual(expected, reviewProjectInteractive(filename))
#         assert False # TODO: implement your test here
#
# class TestDoInboxInteractive(unittest.TestCase):
#     def test_do_inbox_interactive(self):
#         # self.assertEqual(expected, doInboxInteractive(item))
#         assert False # TODO: implement your test here
#
# class TestGetCalendarTags(unittest.TestCase):
#     def test_get_calendar_tags(self):
#         # self.assertEqual(expected, getCalendarTags())
#         assert False # TODO: implement your test here
#
# class TestHasCalendarTag(unittest.TestCase):
#     def test_has_calendar_tag(self):
#         # self.assertEqual(expected, hasCalendarTag(text))
#         assert False # TODO: implement your test here
#
# class TestFindFiles(unittest.TestCase):
#     def test_find_files(self):
#         # self.assertEqual(expected,
#         #     find_files(directory, archives, filter, full_text, weekend))
#         assert False # TODO: implement your test here
#
# class TestGetIgnoreString(unittest.TestCase):
#     def test_get_ignore_string(self):
#         # self.assertEqual(expected, getIgnoreString(worktime))
#         assert False # TODO: implement your test here
#
# class TestAddUpdatedLine(unittest.TestCase):
#     def test_add_updated_line(self):
#         # self.assertEqual(expected, addUpdatedLine(filename))
#         assert False # TODO: implement your test here
#
# class TestStringToFileName(unittest.TestCase):
#     def test_string_to_file_name(self):
#         # self.assertEqual(expected, string_to_file_name(text, ext))
#         assert False # TODO: implement your test here
#
# class TestGetUniqueName(unittest.TestCase):
#     def test_get_unique_name(self):
#         # self.assertEqual(expected, get_unique_name(filename))
#         assert False # TODO: implement your test here
#
# class TestRenameFile(unittest.TestCase):
#     def test_rename_file(self):
#         # self.assertEqual(expected, rename_file(filename, new_name))
#         assert False # TODO: implement your test here
#
# class TestMoveToFolder(unittest.TestCase):
#     def test_move_to_folder(self):
#         # self.assertEqual(expected, move_to_folder(filename, folder))
#         assert False # TODO: implement your test here
#
# class TestRecordDone(unittest.TestCase):
#     def test_record_done(self):
#         # self.assertEqual(expected, recordDone(item))
#         assert False # TODO: implement your test here
#
# class TestGetCalendarItems(unittest.TestCase):
#     def test_get_calendar_items(self):
#         # self.assertEqual(expected, getCalendarItems(filename))
#         assert False # TODO: implement your test here
#
# class TestGetInboxMenu(unittest.TestCase):
#     def test_get_inbox_menu(self):
#         # self.assertEqual(expected, get_inbox_menu())
#         assert False # TODO: implement your test here
#
# class TestGetOutput(unittest.TestCase):
#     def test_get_output(self):
#         # self.assertEqual(expected, getOutput(command))
#         assert False # TODO: implement your test here
#
# class TestAppendToFile(unittest.TestCase):
#     def test_append_to_file(self):
#         # self.assertEqual(expected,
#         #     appendToFile(filename, content, timestamp))
#         assert False # TODO: implement your test here
#
# class TestToggleTodo(unittest.TestCase):
#     def test_toggle_todo(self):
#         # self.assertEqual(expected, toggleTodo(line))
#         assert False # TODO: implement your test here
#
# class TestToggleWaiting(unittest.TestCase):
#     def test_toggle_waiting(self):
#         # self.assertEqual(expected, toggleWaiting(line))
#         assert False # TODO: implement your test here
#
# class TestGetDateString(unittest.TestCase):
#     def test_get_date_string(self):
#         # self.assertEqual(expected, getDateString())
#         assert False # TODO: implement your test here
#
# class TestGetUpdatedString(unittest.TestCase):
#     def test_get_updated_string(self):
#         # self.assertEqual(expected, getUpdatedString())
#         assert False # TODO: implement your test here
#
# class TestGetFilenameForTitle(unittest.TestCase):
#     def test_get_filename_for_title(self):
#         # self.assertEqual(expected, get_filename_for_title(topic, notes_dir))
#         assert False # TODO: implement your test here
#
# class TestCreateNewNote(unittest.TestCase):
#     def test_create_new_note(self):
#         # self.assertEqual(expected, create_new_note(keywords))
#         assert False # TODO: implement your test here
#
# class TestNewNote(unittest.TestCase):
#     def test_new_note(self):
#         # self.assertEqual(expected, new_note(args, quick, editor, notes_dir))
#         assert False # TODO: implement your test here
#
# class TestToBar(unittest.TestCase):
#     def test_to_bar(self):
#         # self.assertEqual(expected, to_bar(number, total))
#         assert False # TODO: implement your test here
#
# class TestNumbersToBars(unittest.TestCase):
#     def test_numbers_to_bars(self):
#         # self.assertEqual(expected, numbers_to_bars(text))
#         assert False # TODO: implement your test here
#
# class TestFormat2Cols(unittest.TestCase):
#     def test_format_2_cols(self):
#         # self.assertEqual(expected, format_2_cols(tuple_list))
#         assert False # TODO: implement your test here
#
# class TestFolderSummary(unittest.TestCase):
#     def test_folder_summary(self):
#         # self.assertEqual(expected, folder_summary(archives, limit))
#         assert False # TODO: implement your test here
#
if __name__ == '__main__':
    unittest.main()
