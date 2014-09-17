################################################################################
# IMPORTS
################################################################################

import subprocess
import shutil
import os
from datetime import date, timedelta, datetime, time
import re
from ConfigParser import SafeConfigParser
from collections import defaultdict
import logging
import platform
import sys

LOGGER = logging.getLogger(__name__)

################################################################################
# GLOBAL CONSTANTS
################################################################################

CONFIG_FILE = '~/.minion'

# Linux preferred apps to view files:
NON_TEXT_VIEWERS = {
    'default': 'cat %s | less',
    '.pdf': 'evince',
    '.jpg': 'eog',
    '.jpeg': 'eog',
    '.png': 'eog',
    '.doc': 'libreoffice',
    '.docx': 'libreoffice',
    '.xls': 'libreoffice',
    '.xlsx': 'libreoffice',
}

# Mac OSX 10.9 preferred apps to view files:
if 'Darwin' in platform.platform():
    NON_TEXT_VIEWERS = {
        'default': '/usr/bin/open',
        '.doc': '/usr/bin/open',
        '.docx': '/usr/bin/open',
        '.gdoc': '/usr/bin/open',
        '.gdraw': '/usr/bin/open',
        '.gsheet': '/usr/bin/open',
        '.gslides': '/usr/bin/open',
        '.jpg': '/usr/bin/open',
        '.jpeg': '/usr/bin/open',
        '.pdf': '/usr/bin/open',
        '.xls': '/usr/bin/open',
        '.xlsx': '/usr/bin/open',
    }

# Cygwin preferred apps to view files:
if 'CYGWIN' in platform.platform():
    NON_TEXT_VIEWERS = {
        'default': 'cat %s | less',
        '.pdf': 'cmd /q /c start "Launched by Minion"',
        '.jpg': 'cmd /q /c start "Launched by Minion"',
        '.jpeg': 'cmd /q /c start "Launched by Minion"',
        '.png': 'cmd /q /c start "Launched by Minion"',
        '.doc': 'cmd /q /c start "Launched by Minion"',
        '.docx': 'cmd /q /c start "Launched by Minion"',
        '.xls': 'cmd /q /c start "Launched by Minion"',
        '.xlsx': 'cmd /q /c start "Launched by Minion"',
    }


################################################################################
# FUNCTIONS
################################################################################

def _settings_parser(default_notes_dir='~/minion/notes'):
    ''' Create the parser for the settings file. '''

    # Default notes settings
    settings = SafeConfigParser()
    settings.add_section('notes')
    settings.set('notes', 'home', default_notes_dir)
    settings.set('notes', 'favorites', 'inbox, today, next, soon, someday')
    settings.set('notes', 'notes_included_extensions', '*')
    settings.set('notes', 'notes_excluded_extensions', '~')
    settings.set('notes', 'default_template', 'note')
    settings.set('notes', 'default_recent_days', '14')
    settings.set('notes', 'archive_folders_date_format', '%%y.%%m')
    # Default composition settings
    settings.add_section('compose')
    default_template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    settings.set('compose', 'templates', default_template_dir)
    settings.set('compose', 'extension', '.txt')
    settings.set('compose', 'filename_sep', '-')
    settings.set('compose', 'editor', 'vim')
    settings.set('compose', 'tagline', ':tags:')
    settings.set('compose', 'tags_case_sensitive', 'false')
    # Default note date format
    settings.add_section('date')
    settings.set('date', 'format', '%%Y-%%m-%%d')
    # Sort actions
    settings.add_section('sort_actions')

    return settings


def get_settings():
    minion_file = os.path.expanduser(CONFIG_FILE)

    settings = _settings_parser()

    # Load if available, write defaults if not.
    if os.path.exists(minion_file):
        settings.read([minion_file])
    else:  # pragma: no cover
        f = open(minion_file, 'w')
        settings.write(f)
        f.close()

    # Pre-process some settings

    # Filename separator can be entered in .minion file with quotes around it
    # so we can also enter space as a separator (' '). We will extract that
    # single character below and stick it back into the settings structure.
    filename_separator = settings.get('compose', 'filename_sep')
    if len(filename_separator) > 1:
        filename_separator = filename_separator[1]
        settings.set('compose', 'filename_sep', filename_separator)

    return settings


GLOBAL_SETTINGS = get_settings()


def get_setting(section, key):
    return GLOBAL_SETTINGS.get(section, key)


def parse_sort_actions_settings():
    return GLOBAL_SETTINGS.items('sort_actions')


def get_date_format():
    return get_setting('date', 'format')


def get_global_data():
    ''' Return global data common to many template operations.
    '''
    date_format = get_date_format()
    data = {}
    TODAY = date.today()
    data['today'] = TODAY.strftime(date_format)
    monday = TODAY - timedelta(days=TODAY.weekday())
    for i, day in enumerate(('sunday', 'monday', 'tuesday', 'wednesday',
                             'thursday', 'friday', 'saturday', 'sunday')):
        data[day] = (monday + timedelta(days=i-1)).\
            strftime(date_format)
    data['day_of_week'] = TODAY.weekday()
    return data


GLOBAL_DATA = get_global_data()


def list_stray_files(count=2):
    ''' Find all files whose folder only has one or two files. '''
    notes_home = get_notes_home()
    folders = os.listdir(notes_home)
    results = []
    for folder in folders:
        if 'archive' not in folder:
            full_folder = os.path.join(notes_home, folder)
            if os.path.isdir(full_folder):
                files = os.listdir(full_folder)
                if len(files) <= count:
                    for filename in files:
                        results.append(os.path.join(full_folder, filename))

    return results


def sort_files_interactive(match_files):
    ''' Interactively sort the list of files. '''
    print "Enter '?' to see available actions."
    total = len(match_files)
    count = 0
    to_open = []
    for item in match_files:
        count += 1
        # Show progress...
        print
        print to_bar(count, total)
        # The main call...
        files_to_open = doInboxInteractive(item)
        to_open.extend(files_to_open)

    if len(to_open) > 0:
        print "Files to open:\n  %s" % '\n  '.join(to_open)
        open_files(to_open)


def get_unique_dates(content):
    '''Return all the unique dates in the content'''

    recognizers = {
        '\d{1,2}\.\d{1,2}\.\d{4}\D': '%m.%d.%Y',
        '\d{1,2}\.\d{1,2}\.\d{2}\D': '%m.%d.%y',
        '\d{1,2}/\d{1,2}/\d{4}\D': '%m/%d/%Y',
        '\d{1,2}/\d{1,2}/\d{2}\D': '%m/%d/%y',
        '\d{4}-\d{2}-\d{2}\D': '%Y-%m-%d'}

    # Find dates in the content
    dates = []
    for key in recognizers:
        r = re.compile(key)
        matches = r.findall(content)
        if matches:
            date_format = recognizers[key]
            for match in matches:
                try:
                    # We have to remove the last character from 'match'.
                    # It is the first non-digit character at the end.
                    new_date = datetime.strptime(match[:-1], date_format).date()
                    # Double check we are picking up a valid dates
                    if (new_date > date(2010, 1, 1)) and\
                       (new_date < date(2049, 12, 31)):
                        dates.append(new_date)
                except ValueError:
                    pass
                except TypeError:
                    print "Ignored " + match

    if len(dates) == 0:
        return None
    # find all unique dates and sort them
    dates = list(set(dates))
    dates.sort()

    return dates


def get_first_date(content):
    '''Return the earliest date written in the file name or contents.
       For backwards compatibility return as datetime type.
    '''
    return datetime.combine(get_unique_dates(content)[0], time())


def get_file_content(filename, include_filename=True):
    ''' Yep. '''
    content = ""

    # Don't try to get non-text content.
    _, extension = os.path.splitext(filename)
    extension.lower()
    if extension not in NON_TEXT_VIEWERS:
        f = open(filename, 'r')
        content = f.read()
        f.close()

    # Always treat the filename as if part of the content.
    if include_filename:
        content = filename + ' ' + content

    return content


def limit_to_year(year, file_list):
    '''Return only files from the list whose first date is within
    the specified year.

    Sorts the list by date, while at it.
    '''
    results = defaultdict(list)
    for filename in file_list:
        content = get_file_content(filename)
        first_date = get_first_date(content)
        if hasattr(first_date, 'year'):
            if str(first_date.year) == str(year):
                results[first_date].append(filename)

    # TODO: Sort the collection
    sorted_results = []
    for _, files in results.items():
        for filename in files:
            sorted_results.append(filename)

    return sorted_results


def get_total_file_count(include_archives=False):
    '''Return the count of the total number of files available to Minion.
       This is useful for context when a search unexpectedly returns no results.
    '''
    total_files = find_files(archives=include_archives)
    total = len(total_files)
    return total


def get_favorites_summary():
    ''' Return the count of items in each of the favorite folders. '''
    favorites = get_setting('notes', 'favorites').replace(' ', '')
    favs = favorites.split(',')
    results = []
    summary = get_folder_summary()
    for line in summary:
        for fav in favs:
            if fav in line:
                results.append(line)
    return results


def get_folder_summary(archives=False):
    summary = []
    notes_home = get_notes_home()
    folders = os.listdir(notes_home)
    for folder in folders:
        if 'archive' not in folder:
            full_folder = os.path.join(notes_home, folder)
            if os.path.isdir(full_folder):
                files = os.listdir(full_folder)
                summary.append((len(files), folder))

    summary.sort(reverse=True)
    return summary


def select_file(match_files, max_files=10):
    '''Interactively select a file from the given list.
       Returns a tuple with the chosen keywords and the final selected item.
    '''
    choice_path = ''
    if len(match_files) == 0:
        return (choice_path, '')

    while len(match_files) > 1:
        if len(match_files) > max_files:
            print "%d matches." % len(match_files)
        else:
            display_output('Notes (most recent first):', match_files,
                           max_display=20)
            choice = raw_input(
                "Selection? ('!' selects the first file, 'q' quits): ")
        if choice == '!':
            break
        if choice == 'q':
            print "Exiting ...\n"
            sys.exit()
        less_match_files = limit_notes(choice, match_files, True)
        if len(less_match_files) == 0:
            print "No %s %s matches." % (choice_path, choice)
        else:
            choice_path += '-' + choice
            match_files = less_match_files

    return (choice_path, match_files[0])


def remind(text):
    filename = "%s/%s" % (get_inbox(), string_to_file_name(text))
    f = open(filename, 'a')
    f.write(text)
    f.close()
    return filename


def remove_archives(file_list):
    return remove_notes(file_list, ['archive'])


def get_remove_tags(text_string):
    tag_re = re.compile("-[\@\w]*")
    tags = tag_re.findall(text_string)
    tags = [x.lstrip('-') for x in tags]
    return tags


def get_tags_from_string(text_string):
    tag_re = re.compile("\+[\@\w]*")
    tags = tag_re.findall(text_string)
    results = [x.lstrip('+') for x in tags]
    return results


def sort_by_tag(file_list):
    all_tags = {'no tags': []}
    file_list = list(set(file_list))
    for item in file_list:
        tags = get_tags_from_string(item)
        if len(tags) == 0:
            all_tags['no tags'].append(item)
        placed = False
        for tag in tags:
            if not placed:
                if tag in all_tags:
                    placed = True
                    all_tags[tag].append(item)
                else:
                    placed = True
                    all_tags[tag] = [item]
    return all_tags


def format_output_list(output, by_tag, max_display, separator, raw_files):
    if not raw_files:
        output = clean_output(output)
    if max_display:
        remain = len(output) - max_display
        output = output[:max_display]
        if remain > 0:
            output.append("{} more results...".format(remain))

    if by_tag:
        all_tags = sort_by_tag(output)
        output = ''
        for tag in all_tags:
            if len(all_tags[tag]) > 0:
                output += '\n\t' + tag
                output += "\n-------------------\n"
                output += separator.join(all_tags[tag])
    else:
        output = [x.replace('\n', '') for x in output]
        output = separator.join(output)
    return output


def format_output_dict(output, separator, raw_files):
    output_lines = []
    for key in sorted(output):
        if type(output[key]) is list:
            item = [str(key), format_output_list(
                output[key],
                by_tag=False,
                max_display=False,
                separator='\n',
                raw_files=raw_files)]
            line = '\n'.join(item)
        else:
            if not raw_files:
                output[key] = clean_output(output[key])
            item = [str(key), str(output[key])]
            line = '\t-\t'.join(item)
        output_lines.append(line)

    return separator.join(output_lines)


def display_output(title, output, by_tag=False,
                   raw_files=False, max_display=None):
    # If empty list or empty string, etc:
    if not output:
        print "No %s items.\n" % title
        return

    # Print dictionaries as key - value
    if type(output) is dict:
        output = format_output_dict(output, '\n', raw_files)
    # Print lists with one item per line
    elif type(output) is list:
        output = format_output_list(output, by_tag, max_display, '\n',
                                    raw_files)
    else:
        if not raw_files:
            output = clean_output(output)
        if max_display:
            remain = len(output) - max_display
            output = output[:max_display]
            if remain > 0:
                output.append("{} more results...".format(remain))

    if title:
        print "---- %s: " % title

    print output


def clean_output(output):
    if type(output) is list:
        clean_list = []
        for item in output:
            clean_list.append(clean_string(item))
        return clean_list
    else:
        return clean_string(output)


def clean_string(output):
    notes_folder = get_notes_home()
    no_folder = output.replace(notes_folder, '')
    name_sep = get_setting('compose', 'filename_sep')
    no_separators = no_folder.replace(name_sep, ' ')
    no_slashes = no_separators.replace('/', ' : ')
    no_extensions = no_slashes.replace(get_setting('compose', 'extension'), '')
    return no_extensions


def content_has_tag(content, tag):
    ''' Return true if the file content's tags line has the given tag. '''
    content = content.split('\n')
    TAG_INDICATOR = get_setting('compose', 'tagline')
    if get_setting('compose', 'tags_case_sensitive') != 'true':
        tag = tag.lower()
    for line in content:
        if TAG_INDICATOR in line:
            if tag in line:
                return True
    return False


def has_tag(filename, tag):
    ''' Return true if the file's tags line has the given tag. '''
    content = get_file_content(filename)
    return content_has_tag(content, tag)


def limit_notes(choice, notes, full=False):
    ''' Only return notes who have the text in choice in at least one of:
            The :tags: line in the file.
            or
            The filename.
    '''
    new_array = []
    for note in notes:
        choice = choice.lower()
        low_note = note.lower()
        if (choice in low_note) or has_tag(note, choice):
            if 'swp' not in note:
                new_array.append(note)
        else:
            if full:
                content = ''
                try:
                    f = open(note, 'r')
                    content = f.readlines()
                    f.close()
                except:
                    pass
                content = ' '.join(content)
                content = content.lower()
                if choice in content:
                    new_array.append(note)
    return new_array


def remove_notes(file_list, terms):
    new_list = []
    for f in file_list:
        matches_term = False
        low_f = f.lower()
        for term in terms:
            term = term.lower()
            if low_f.count(term) > 0:
                matches_term = True
        if not matches_term:
            new_list.append(f)
    return new_list


def clean_file_name(text):
    return text.replace(' ', '-').replace('/', '-')


def get_viewer(filename):
    return get_editor(filename, view=True)


def get_editor(filename, view=False):
    # make a copy of non-text viewers
    apps = dict()
    apps.update(NON_TEXT_VIEWERS)

    if not view:
        apps['default'] = get_setting('compose', 'editor')

    extension = os.path.splitext(filename)[1]
    extension = extension.lower()
    if extension in apps:
        editor = apps[extension]
    else:
        try:
            editor = os.environ['EDITOR']
        except:
            editor = apps['default']

    return editor


def file_to_stdout(filename):
    ''' Print the contents of the file to standard output. '''
    f = open(filename, 'r')
    content = f.read()
    f.close()
    print content
    # One extra line break is wise, in case the file does not end with one.
    print '\n'


def get_windows_path(cygwin_path):
    ''' Converts cygwin bash path to windows path in CYGWIN environment'''

    # Escape the special characters in the cygwin_path
    cygwin_path = cygwin_path.replace(' ', '\ ')
    cygwin_path = cygwin_path.replace('(', '\(')
    cygwin_path = cygwin_path.replace(')', '\)')

    # Call external path converter (cygpath is part of CygWin environment)
    cmd_line = 'cygpath -w ' + cygwin_path
    w_path = subprocess.Popen(cmd_line, shell=True,
                              stdout=subprocess.PIPE).stdout.read()

    # remove carriage returns at the end of the w_path and
    # add quotes around the path to preserve backslashes and filename spaces
    w_path = '"' + w_path.strip('\n') + '"'

    return w_path


def open_file(program, file_list, line=0):
    ''' Use the selected program to open the selected files.

        Where possible, jump to the specified line/position in the file.
    '''

    # Special treatment if launching windows programs in CygWin
    if program.startswith('cmd '):
        # Convert file paths if running on CygWIN to support launching windows
        # viewers/programs
        if 'CYGWIN' in platform.platform():
            # convert CygWin paths to Windows paths
            file_list = [get_windows_path(fi) for fi in file_list]

    # add initial line parameter for launching vim
    if program.startswith('vim'):
        program += ' +' + str(line)

    # escape spaces in the filenames, but only if not launching cmd on CygWin
    if not program.startswith('cmd'):
        file_list = [fi.replace(' ', '\ ') for fi in file_list]

    # insert filenames placeholder to the command line if not already there
    if "%s" not in program:
        program = program + ' %s'

    # apply the filename placeholder
    program = program % ' '.join(file_list)

    # call the external program
    subprocess.call(program, shell=True)


def open_in_editor(filename, line=0):
    ''' Select an appropriate editor and open the file. '''
    program = get_editor(filename)
    open_file(program, [filename], line)


def open_files(filenames, max=10):
    ''' Open all the files in the list.
        But stop at the given max, or 10 if not specified.
    '''
    if len(filenames) > max:
        filenames = filenames[:max]

    # Choose editors
    editors = {}
    for filename in filenames:
        editor = get_editor(filename)
        if editor not in editors:
            editors[editor] = []
        editors[editor].append(filename)

    # Open files with editors
    for editor in editors:
        # Open each file list with the chosen editor.
        open_file(editor, editors[editor])


def preview_file(filename):
    program = get_viewer(filename)
    open_file(program, [filename])


def get_notes_home():
    notes_home = get_setting('notes', 'home')
    notes_home = os.path.expanduser(notes_home)
    if not os.path.exists(notes_home):
        os.mkdir(notes_home)
    return notes_home


def get_inbox():
    inbox = "%s/inbox" % get_notes_home()
    if not os.path.exists(inbox):
        os.mkdir(inbox)
    return inbox


def get_keyword_files(keyword_string, archives=False, full_text=False):
    ''' Get all files that match space-separated keywords. '''
    keywords = keyword_string.split(' ')
    match_files = find_files(filter=keywords, archives=archives,
                             full_text=full_text)
    return match_files


def get_inbox_files():
    ''' Get all inbox files. '''
    match_files = find_files(filter=['inbox'], archives=False)
    return match_files


def get_folder(folder):
    '''Return a full path, relative to the notes home.  '''
    # Convert 'archive' to 'archive.2012.08'
    if folder == 'archive':
        date_format = get_setting('notes', 'archive_folders_date_format')
        year_month = date.today().strftime(date_format)
        folder = "archive.%s" % (year_month)

    notes_home = get_notes_home()
    directory = os.path.join(notes_home, folder)

    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def limit_notes_interactive(notes):
    while len(notes) > 1:
        display_output('Multiple Matches', notes)
        choice = raw_input('Choice? ')
        notes = limit_notes(choice, notes)
    return notes[0]


def expand_short_command(command):
    # Hardwired sort actions
    commands = {
        'r': '!rename',
        'e': '!edit',
        'v': '!view',
        'q': '!quit',
        'a': '!archive',
        'd': '!delete',
        '?': '!help'
    }
    # Add configurable sort actions
    commands.update(parse_sort_actions_settings())

    if command in commands:
        return commands[command]
    return command


def get_tags(filename):
    ''' Return tags from file's tag line. '''
    content = get_file_content(filename)
    return get_content_tags(content)


def get_content_tags(content):
    ''' Return all tags from file content. '''
    TAG_INDICATOR = get_setting('compose', 'tagline')
    content = content.split('\n')
    tags = []
    for line in content:
        tags = parse_tags(line, TAG_INDICATOR)
        if len(tags) > 0:
            break
    return tags


def parse_tags(line, TAG_INDICATOR=None):
    if not TAG_INDICATOR:
        TAG_INDICATOR = get_setting('compose', 'tagline')
    tags = line.split(' ')
    if TAG_INDICATOR in tags:
        tags.pop(tags.index(TAG_INDICATOR))
        return tags
    return []


def create_tag_line(tags, TAG_INDICATOR=None):
    ''' Create a line of text that stores tags
        in a test file.

        Note that all tags are stored in lower case,
        to simplify sorting and retrieval.
    '''
    if not TAG_INDICATOR:
        TAG_INDICATOR = get_setting('compose', 'tagline')

    # Unique-ify
    tags = list(set(tags))
    # Remove any line breaks
    tags = [x.replace('\n', ' ') for x in tags]
    # Make sure all the tags are lower case if case sensitive switch off
    if get_setting('compose', 'tags_case_sensitive') != 'true':
        tags = [x.lower() for x in tags]
    tags = sorted(tags)

    # Always put the tag indicator at the start.
    if TAG_INDICATOR in tags:
        tags.pop(tags.index(TAG_INDICATOR))

    tags.insert(0, TAG_INDICATOR)
    return ' '.join(tags)


def remove_tags_from_content(tags, content):
    TAG_INDICATOR = get_setting('compose', 'tagline')

    # Make sure all the tags are lower case if case sensitive switch off
    if get_setting('compose', 'tags_case_sensitive') != 'true':
        tags = [x.lower() for x in tags]

    all_tags = []
    updated_content = []
    content = content.split('\n')
    for line in content:
        if (TAG_INDICATOR in line):
            all_tags = parse_tags(line, TAG_INDICATOR)
            for tag in tags:
                if tag in all_tags:
                    all_tags.pop(all_tags.index(tag))
            line = create_tag_line(all_tags, TAG_INDICATOR)

        updated_content.append(line)

    # Write back to the file
    updated_content = [line2.rstrip('\n') for line2 in updated_content]
    updated_string = '\n'.join(updated_content)
    return updated_string


def remove_tags_from_file(tags, filename):
    if len(tags) == 0:
        return filename

    # Remove the tags
    content = get_file_content(filename, include_filename=False)
    updated_content = remove_tags_from_content(tags, content)

    # Rewrite the file.
    f = open(filename, 'w')
    f.write(updated_content)
    f.close()
    return filename


def add_tags(tags, content):
    ''' Return the file content with the tags added. '''

    TAG_INDICATOR = get_setting('compose', 'tagline')

    if ' ' in TAG_INDICATOR:
        print "WARNING: Spaces in the [compose] tagline= setting \
            may cause tag duplication."

    all_tags = []
    updated_content = []
    found_tags = False
    # Make sure all the tags are lower case if case sensitive switch off
    if get_setting('compose', 'tags_case_sensitive') != 'true':
        tags = [x.lower() for x in tags]
    for line in content.split('\n'):
        if (TAG_INDICATOR in line):
            found_tags = True
            all_tags = parse_tags(line, TAG_INDICATOR)
            # Add new tags
            all_tags.extend(tags)
            line = create_tag_line(all_tags, TAG_INDICATOR)
        updated_content.append(line)

    # Add a tags line to the end, if we didn't find it sooner.
    if not found_tags:
        tag_line = create_tag_line(tags, TAG_INDICATOR)
        updated_content.append(tag_line)

    # Remove
    updated_content = [line2.rstrip('\n') for line2 in updated_content]
    updated_string = '\n'.join(updated_content)

    return updated_string


def add_tags_to_file(tags, filename):
    # Do not bother if no tags are passed.
    if len(tags) == 0:
        return filename

    # Add tags
    args = {
        'content': get_file_content(filename, include_filename=False),
        'tags': tags,
    }
    updated_content = add_tags(**args)

    f = open(filename, 'w')
    f.write(updated_content)
    f.close()

    return filename


def archive(filename):
    ''' Move the selected file into an archive folder. '''
    # get_folder does some cleverness with the 'archive' name.
    folder = get_folder('archive')
    filename = move_to_folder(filename, folder)
    print "Moved to %s" % folder


def rename_note(filename, new_name):
    if len(new_name) == 0:
        new_name = raw_input('New name? ')
    new_name = string_to_file_name(new_name)
    new_file = "%s/%s" % (get_inbox(), new_name)
    new_file = rename_file(filename, new_file)
    return new_file


def check_add_remove_tags(filename, command):
    # if there are any tags to be added, add them
    tags_to_add = get_tags_from_string(command)
    if len(tags_to_add) > 0:
        add_tags_to_file(tags_to_add, filename)
        print "Tag(s) %s added." % str(tags_to_add)

    # if there are any tags to be removed, remove them
    remove_tags = get_remove_tags(command)
    if len(remove_tags) > 0:
        remove_tags_from_file(remove_tags, filename)
        print "Tag(s) %s removed." % str(remove_tags)

    if len(tags_to_add) > 0 or len(remove_tags) > 0:
        return True
    else:
        return False


def check_move_note(filename, command):
    folder_re = re.compile('>\S*')
    folders = folder_re.findall(command)
    if len(folders) > 0:
        folder = folders[0]
        folder = folder.replace('>', '')
        folder = os.path.expanduser(folder)
        filename = move_to_folder(filename, folder)
        print "Moved to %s" % folder
    return filename


def delete_note(filename):
    action = raw_input(
        'Delete note %s? (type "YES" to confirm): '
        % filename)
    if action == "YES":
        os.remove(filename)
        print "Note %s was deleted!" % filename
    else:
        print "Note %s was NOT deleted." % filename


def apply_command_to_file(filename, command):
    ''' The core of the interactive file sorting system. '''
    command = expand_short_command(command)
    if '!help' in command:
        print get_sort_menu() + '\n'
        doInboxInteractive(filename)

    if '!edit' in command:
        open_in_editor(filename)
        doInboxInteractive(filename)

    if '!archive' in command:
        archive(filename)

    if '!rename' in command:
        new_filename = rename_note(filename, command.replace('!rename', ''))
        doInboxInteractive(new_filename)
        return new_filename

    if '!delete' in command:
        delete_note(filename)

    if check_add_remove_tags(filename, command):
        doInboxInteractive(filename)

    # If there's a calendar tag...move to the calendar folder.
    if hasCalendarTag(command):
        filename = move_to_folder(filename, 'calendar')
        print "Moved %s to calendar folder." % filename
    else:
        # Move elsewhere if requested.
        filename = check_move_note(filename, command)

    if '!view' in command:
        preview_file(filename)
        doInboxInteractive(filename)

    if '!quit' in command:
        print "Exiting sort ...\n"
        sys.exit()

    return filename


def doInboxInteractive(item):
    to_open = []
    display_output('Selected', item, by_tag=False)
    choice = raw_input('Action? ')
    if len(choice) > 0:
        # some commands can change the name of the file/item
        item = apply_command_to_file(item, choice)
        if choice == 'o':
            to_open.append(item)
    return to_open


def getCalendarTags():
    return ['@Jan', '@Feb', '@Mar', '@Apr', '@May', '@Jun', '@Jul', '@Aug',
            '@Sep', '@Oct', '@Nov', '@Dec', ':Jan', ':Feb', ':Mar', ':Apr',
            ':May', ':Jun', ':Jul', ':Aug', ':Sep', ':Oct', ':Nov', ':Dec']


def hasCalendarTag(text):
    month_tags = getCalendarTags()
    for tag in month_tags:
        if tag in text:
            return True
    return False


def get_files(directory, archives=False):
    ''' Called by find_files to get a list of files, before sorting. '''
    included_exts_string =\
        GLOBAL_SETTINGS.get('notes', 'notes_included_extensions').\
        replace(' ', '')
    excluded_exts_string =\
        GLOBAL_SETTINGS.get('notes', 'notes_excluded_extensions').\
        replace(' ', '')
    included_exts = included_exts_string.split(',')
    excluded_exts = excluded_exts_string.split(',')

    dir_list = os.listdir(directory)
    files = []
    for item in dir_list:
        dirName = os.path.join(directory, item)
        if os.path.isdir(dirName):
            files.extend(get_files(dirName, archives=archives))
        else:
            file_excluded = False
            for excluded_ext in excluded_exts:
                if item.endswith(excluded_ext):
                    file_excluded = True
                    break
            if not file_excluded:
                file_included = False
                for included_ext in included_exts:
                    if (('*' in included_ext) or item.endswith(included_ext)):
                        file_included = True
                        break
            if not file_excluded and file_included:
                files.append("%s/%s" % (directory, item))

    if not archives:
        files = remove_archives(files)

    return files


def log_line_to_file(filename, line):
    '''
    Add a log file line to the file.

    Log lines always start with the current day and time.
    '''
    params = {
        'date': datetime.today().strftime(get_date_format()),
        'time': datetime.today().strftime("%H:%M"),
        'line': line,
    }
    # TODO: Make log_line_template fetch from config file.
    log_line_template = "\n{date} {time} : {line}"
    new_line = log_line_template.format(**params)

    print "Appending new line to %s" % filename
    f = open(filename, 'a')
    f.write(new_line)
    f.close()
    print new_line
    return


def choose_file(filter=[], archives=False, full_text=False):
    '''
    Given the filter, suggest a single match file.

    Also always return all other possible matches.

    When there are too many matches, the first return is None.

    When there are no matches at all,
    the first return is a suggestion for a new file.

    The second return is always the list of possible matches.

    '''
    match_files = find_files(filter=filter, archives=archives,
                             full_text=full_text)

    # Filter word must always match a single file.
    if len(match_files) > 1:
        return None, match_files
    elif len(match_files) == 1:
        filename = match_files[0]
        return filename, [filename]
    else:
        print "No matches, suggesting new filename."
        filename = get_filename_for_topic(' '.join(filter))
        return filename, []


def find_files(directory=None, archives=False, filter=[], full_text=False,
               find_any=False, days=None):
    ''' Find matching files... '''
    if directory is None:
        directory = get_notes_home()

    files = get_files(directory, archives)

    if not find_any:
        for tag in filter:
            files = limit_notes(tag, files, full=full_text)
    else:
        raw_files = files
        files = []
        for f in raw_files:
            if has_any_tag(f, filter):
                files.append(f)

    # sort the files according to modification date, most recent first
    file_tuples = []
    for filename in files:
        mod_datetime = datetime.fromtimestamp(os.path.getmtime(filename))
        file_tuples.append((mod_datetime, filename))
    sorted_tuples = sorted(file_tuples, reverse=True)

    # return only files modified within last N days
    if type(days) is int:
        threshold_dt = datetime.today() - timedelta(days=days)
        sorted_files = [x[1] for x in sorted_tuples if x[0] > threshold_dt]
    else:
        sorted_files = [x[1] for x in sorted_tuples]

    return sorted_files


def has_any_tag(filename, tags):
    for tag in tags:
        if tag.lower() in filename.lower():
            return True
        if has_tag(filename, tag):
            return True
    return False


def construct_note_title(topic, template):
    # retrieve the extension
    ext = get_setting('compose', 'extension')
    ext = ext.lstrip('.')

    # merge GLOBAL_DATA into data
    data = {'topic': topic,
            'ext': ext}
    data.update(GLOBAL_DATA)

    # merge data with the note title template
    filename = template.format(**data)

    return filename


def string_to_file_name(topic, template='{topic}'):
    ''' Generates filename based on the topic and filename template.
        Extension is always appended.
    '''
    # replace spaces and '/' with the topic separator
    name_sep = get_setting('compose', 'filename_sep')
    new_topic = topic.replace(' ', name_sep).replace('/', name_sep)

    # the note filename will be the note title
    filename = construct_note_title(new_topic, template)

    # append extension if not already there
    ext = get_setting('compose', 'extension')
    ext = ext.lstrip('.')
    if not filename.endswith(ext):
        filename = '.'.join([filename.rstrip('.'), ext])

    return filename


def get_unique_name(filename):
    final_name = filename
    while os.path.exists(final_name):
        directory = os.path.dirname(final_name)
        short_name = os.path.basename(final_name)
        import uuid
        uid = str(uuid.uuid1())
        if '.' in short_name:
            short_name = short_name.replace('.', '.' + uid + '.', 1)
        else:
            # In case there is no dot.
            short_name = short_name + uid
        final_name = os.path.join(directory, short_name)
        print "Name conflict. Renamed to " + final_name
    return final_name


def rename_file(filename, new_name):
    folder = os.path.dirname(filename)
    new_file = os.path.join(folder, new_name)

    if filename != new_file:
        new_file = get_unique_name(new_file)
        shutil.move(filename, new_file)
        print "Renamed " + filename + " to " + new_file
    return new_file


def move_to_folder(filename, folder):
    ''' Move the file to a different folder. '''
    try:
        origin = os.path.dirname(filename)
        destination = get_folder(folder)
        short_name = os.path.basename(filename)
        final_name = os.path.join(destination, short_name)
        final_name = get_unique_name(final_name)
        shutil.move(filename, final_name)
        remove_empty_folder(origin)
        return final_name
    except Exception as ex:
        raise ex
        destination = get_inbox()
        new_file_name = "%s/%s" % (destination, os.path.basename(filename))
        print "Error: Moved %s to inbox." % new_file_name
        shutil.move(filename, destination)


def remove_empty_folder(folder):
    ''' If the file being moved out was the last file there, remove the folder.
    '''
    if len(os.listdir(folder)) == 0:
        os.rmdir(folder)
        print "Removed empty folder " + folder + "."


def get_sort_menu():
    fixed_actions = "Available actions:\n" +\
        "  q=quit a=archive r=rename e=edit v=view d=delete o=mark to open\n" +\
        "  +{tag}=add {tag} -{tag}=remove {tag} >{folder}=move to {folder}\n" +\
        "  :{3-letter month}=>calendar (e.g. :Jan) <Enter>=next file ?=help\n"
    sort_actions_settings = parse_sort_actions_settings()
    # build the sort menu; insert new_line if line is too long
    configurable_actions = " "
    for (item, value) in sort_actions_settings:
        new_item = " " + item + '=' + value
        if len(configurable_actions + new_item) > 76:
            configurable_actions += "\n "
        configurable_actions += new_item
    return fixed_actions + configurable_actions


def find_file(filename):
    ''' Find a file by name, checking each directory. '''
    home = get_notes_home()
    for root, _, names in os.walk(home):
        for f in names:
            if f == filename:
                return os.path.join(root, f)
    return None


def get_filename_for_topic(topic, notes_dir=None, filename_template='{topic}'):
    # Get location for new file. Create it if it doesn't exist.
    if notes_dir is None:
        notes_dir = get_inbox()
    if not os.path.exists(notes_dir):
        os.mkdir(notes_dir)

    filename = string_to_file_name(topic, filename_template)

    existing_filename = find_file(filename)
    if existing_filename:
        return existing_filename

    full_filename = os.path.join(notes_dir, filename)

    return full_filename


def get_template_content(template):
    ''' Get the template text. '''
    # Get template file
    data = {
        'type': template,
        'directory': os.path.expanduser(
            get_setting('compose', 'templates')),
        'ext': get_setting('compose', 'extension'),
    }
    template_file_name = "%(type)s_template%(ext)s" % data
    template_file = os.path.join(data['directory'], template_file_name)
    # TODO: Recover gracefully if the expected template is missing.
    f = open(template_file, 'r')
    template_text = f.readlines()
    f.close()
    template_text = ''.join(template_text)
    return template_text


def write_template_to_file(topic, filename, note_template):
    ''' Add templated pre-content to the new note.'''

    template_text = get_template_content(note_template)

    # We need to construct the note title to be able to construct the
    # right length underline string
    note_title_template = template_text.split('\n')[0]
    note_title = construct_note_title(topic, note_title_template)
    underline = '=' * len(note_title)

    # create the data structure to be used for template string substitution
    data = {'topic': topic,
            'filename': filename,
            'topic_underline': underline,
            'underline': underline}
    data.update(GLOBAL_DATA)

    # do the string substitution
    file_text = template_text.format(**data)

    # write the merged string as the new note
    f = open(filename, 'a')
    f.write(file_text)
    f.close()

    # calculate the last line of the note to position the cursor later
    last_line = len(file_text.split('\n'))

    return last_line


def new_note_interactive(topic_fragments, note_template, quick=False,
                         notes_dir=None):
    ''' Create a new note with the filename constructed based on
        the first line in the note template.
    '''

    # construct the topic string
    topic = ' '.join(topic_fragments)
    # create the note
    (filename, last_line) = create_new_note(topic, note_template, notes_dir)
    # Decide whether to open it immediately.
    if not quick:
        open_in_editor(filename, line=last_line)
    else:
        print "Note '%s' created ..." % filename
    return (filename, last_line)


def create_new_note(topic, note_template=None, notes_dir=None,
                    filename_template=None):
    ''' Create a new note, non-interactive.'''

    # When no template, use the default one
    if note_template is None:
        note_template = get_setting('notes', 'default_template')

    # When not defined, put the note in the inbox.
    if notes_dir is None:
        notes_dir = get_inbox()

    # get the first line of the template and use it as filename template
    if filename_template is None:
        template_content = get_template_content(note_template)
        filename_template = template_content.split('\n')[0]
    print "Note template used: " + note_template

    filename = get_filename_for_topic(topic, notes_dir, filename_template)
    last_line = 0

    # only create new note if it does not exist
    if not os.path.exists(filename):
        # Write the template to the file.
        last_line = write_template_to_file(topic, filename, note_template)

    return (filename, last_line)


def to_bar(number, total=10):
    '''Convert a number into a ASCII art progress bar.'''
    pct_complete = number * 1.0 / total
    result = '%s/%s [' % (number, total)

    FULL = '#'
    EMPTY = ' '
    for i in range(1, 10):
        if (i * .1) <= pct_complete:
            result += FULL
        else:
            result += EMPTY
    result += ']'
    return result


def numbers_to_bars(text):
    '''Convert all numbers in the string into ASCII art progress bars.'''
    output = ''
    args = text.split(' ')
    for arg in args:
        bit = None
        try:
            bit = int(arg)
        except:
            output += arg + ' '
        if bit is not None:
            output += to_bar(bit) + ' '
    return output


def format_2_cols(tuple_list):
    SEPARATOR = " - "
    PADDING = ' '
    output = []

    col_max = {}

    # Find longest column members
    for tup in tuple_list:
        line = ""
        col = 0
        for item in tup:
            item = str(item)
            col += 1
            if item not in col_max:
                col_max[col] = 0
            if len(item) > col_max[col]:
                col_max[col] = len(item)

    # Build the string
    for tup in tuple_list:
        col = 0
        line = ""
        for item in tup:
            item = str(item)
            col += 1

            # Separator when needed.
            if len(line) != 0:
                line += SEPARATOR

            # Padded line item.
            while len(item) < col_max[col]:
                item += PADDING
            line += item
        output.append(line)
    output = '\n'.join(output)
    return output


def folder_summary(archives=False, limit=10):
    summary = get_folder_summary(archives)
    summary = summary[:limit]
    output = format_2_cols(summary)
    return output


def print_favorites_summary():
    summary = get_favorites_summary()
    output = format_2_cols(summary)
    return output


def list_recent(match_files):
    ''' Filter match_files. Return only those files that have modification dates
        newer than requested in 'days' parameter. The files are sorted based on
        the modification datetime.
    '''
    recent_files = dict()
    for filename in match_files:
        mod_date = datetime.fromtimestamp(os.path.getmtime(filename)).date()
        if mod_date in recent_files:
            # intentionally inserting at the beginning of the array to match
            #   the reversed chronological list when multiple files per day
            recent_files[mod_date].insert(0, filename)
        else:
            recent_files[mod_date] = [filename]
    return recent_files


def get_last_modified(directory=None, archives=False):
    ''' Return the name of the file (from within the Minion folders)
    last modified, by file system date and time. '''

    if directory is None:
        directory = get_notes_home()

    files = get_files(directory, archives)

    most_recent = None
    result = None

    for filename in files:
        modified = os.path.getmtime(filename)
        if most_recent < modified:
            most_recent = modified
            result = filename

    return result
