''' Data structures used for unit testing. '''
from datetime import datetime
import brain_of_minion as brain


TEST_DATA_DIRECTORY = '/tmp/test_minion'
TEST_DATA_INBOX = '/tmp/test_minion/inbox'
TEST_DATA_NOT_INBOX = '/tmp/test_minion/not_inbox'

LOG_NAME = 'testing_log'
TEST_LOG_FILTER = ['testing_log']
TEST_LOG_LINE = 'This is a line to add to a log file.'


def mock_get_setting(section, key):
    ''' Always return the default settings. '''
    settings = brain._settings_parser(TEST_DATA_DIRECTORY)
    return settings.get(section, key)


EXPECTED_DATE = datetime(2014, 04, 14, 0, 0)

TEST_FILE_CONTENT = \
'''Weekend Plan for 2014-04-14
==============================
:date: 2014-04-14

The topic is: This is a great topic.

Goals
------
Wow. Such goals. So accomplish.'''

TEST_FILE_CONTENT_WITH_TAGS = \
'''Weekend Plan for 2014-04-14
==============================
:date: 2014-04-14

The topic is: This is a great topic.

Goals
------
Wow. Such goals. So accomplish.
:tags: BAR Ninja foo'''

TEST_FILE_CONTENT_WITH_ONE_TAG = \
'''Weekend Plan for 2014-04-14
==============================
:date: 2014-04-14

The topic is: This is a great topic.

Goals
------
Wow. Such goals. So accomplish.
:tags: Ninja'''

# This 'tag' should not appear in file content for testing.
TEST_GIBBERISH = 'Slartibarfast'

# This 'tag' should appear in various file content for testing.
TEST_TAG = 'Ninja'
TEST_TAGS_IN = ['foo', 'BAR', 'Ninja']
TEST_TAGS_OUT = ['BAR', 'Ninja', 'foo']
# As we would add it to the file:
TEST_TAG_LINE = ':tags: BAR Ninja foo'

TEST_FILE_INITIAL_CONTENT = \
    "/tmp/test_minion/inbox/This-is-a-test-topic.txt " +\
    "This is a test topic.\n" +\
    "=====================\n" +\
    ":date: "

TEST_FILE_PATH = '/tmp/test_minion/inbox/This-is-a-test-topic.txt'

TEST_DATE_STRING = '2014-08-12'

TEST_FILENAME_WITH_DATE = \
    '%s/This-is-a-test-topic-%s.txt' % (TEST_DATA_INBOX, TEST_DATE_STRING)

TEST_REMOVE_TAGS = ['foo', 'BAR']

TEST_TOPIC = 'This is a test topic.'
