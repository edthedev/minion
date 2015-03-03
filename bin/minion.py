#!/usr/bin/env python2.7
"""Creates and manages a folder full of reminder files.

Usage:
    minion collect [options] <text> ...
    minion count [options] <text> ...
    minion command [options] <command> <filename>
    minion dates [options] [<text>] ...
    minion find [options] <text> ...
    minion favorites [options]
    minion folder [options] <text> ...
    minion folders [options]
    minion here [options] <text> ...
    minion last [options]
    minion list [options] <text> ...
    minion log [options] <log> <comment> ...
    minion make_config [options]
    minion note [options] <text> ...
    minion open [options] <text> ...
    minion openall [options] <text> ...
    minion recent [options] <text> ...
    minion remind [options] <text> ...
    minion sample [options] <text> ...
    minion sort [options] <text> ...
    minion strays [options]
    minion summary [options]
    minion view [options] <text> ...
    minion tags [options]
    minion template <template> ...

Options:
    -a --archives            Search archive folders for matches.
    -d --days=<days>         Show notes modified last N days .
    -f --files               Display raw file names when listing files.
    -F --folder=<folder>     Place the new note into the given folder.
    -h --help                Show this help.
    -m --max=<max>           Maximum results to display. [default: 10]
    -q --quick               Create without opening in an editor
    -r --config=<config>     Use a different .minion file for this command. [default: ~/.minion]
    -t --template=<template> Use template. [default: 'note']
    -y --year=<year>         Limit results to those created in the given year.
    -v --version             Show version.

Command descriptions:
    count - display a count of the results
    dates - display matching files with dates, in date order
    find - like list, but returns *any* match to *any* given keyword.
    favorites - like summary, but displays only folders configured as favorites
    folder - find and open a folder
    folders - reduce folders by sorting items in folders with fewer items
    here - create a note in the current working directory
    last - reopen the last modified file (by file system modified date/time)
    list - list files matching keywords
    log - add a line with the current date and time to a file.
    note - create a new note and then open it - <text> becomes filename
    open - open an existing note
    openall - open all matches found
    recent - list recent notes with given keywords
    remind - create a new file where <text> becomes filename
    sample - find up to 5 random results that match <text>
    sort - step through results matching <text>
            tag, rename, and sort files into folders
    strays - interactively sort any files whose folder only contains
            a few items.
    summary - list all folders and the item counts in those folders
    view - print the contents of all matches to the terminal standard output
    tags - list all tags
    template - start a note from a specialized template. Try 'week' and
            'journal' to get started.
"""
# #babyTeddySays: m'0']..p p j\[ ''
# #babyDeeDeeSays: /..........................


# Copyright 2011-2014 Edward Delaporte <edthedev@gmail.com>
# Licensed under the GPLv2.
# Created: 2011-04-28

# A life is like a garden. Perfect moments can be had, but not preserved, except in memory.  LLAP - Leonard Nimoy

###############################################################################
# IMPORTS
###############################################################################

import os
import datetime
# DocOpt is awesome. https://github.com/docopt/docopt
from docopt import docopt
import brain_of_minion as brain
from brain_of_minion import get_date_format
import sys
import logging


###############################################################################
# CONSTANTS
###############################################################################

VERSION = "1.9.2"

CLEAN_SORT_MESSAGE = '''*~*~*~*~*~*~*~*~*~*~*~*
 No items to be sorted
*~*~*~*~*~*~*~*~*~*~*~*
'''

CLEAN_STRAYS_MESSAGE = '''*~*~*~*~*~*~*~*
 No stray items
*~*~*~*~*~*~*~*
'''

###############################################################################
# Set up Logging
###############################################################################
_LOGGER = logging.getLogger(__name__)
log_to_file = logging.FileHandler('minion.log')
log_to_console = logging.StreamHandler()
log_to_file.setLevel(logging.DEBUG)
log_to_console.setLevel(logging.ERROR)
_LOGGER.addHandler(log_to_console)
_LOGGER.addHandler(log_to_file)
_LOGGER.setLevel(logging.DEBUG)

###############################################################################
# HELPER FUNCTIONS
###############################################################################

def get_match_files(args, days=None):
    matches = brain.find_files(
        filter=args['<text>'],
        archives=args['--archives'],
        days=days)
    return matches

def should_collect(filename):
    ''' Decide whether is plain text,
    and eligible to be added to a collection. '''
    filename, ext = os.path.splitext(filename)
    allowed_ext = ['.txt', '.rst']
    if ext in allowed_ext:
        # Hack to avoid collecting collections.
        if 'Collected' not in filename:
            return True
    return False


def date_sort(filename):
    '''Provide a date sort that puts None first.'''
    content = brain.get_file_content(filename)
    first_date = brain.get_first_date(content)
    if first_date:
        return first_date
    return datetime.datetime.now()


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


###############################################################################
# ENTRY POINT FUNCTIONS
###############################################################################

# Methods that creates notes. 
# ----------------------------

def minion_template(args):
    '''Create a Minion note from a specialized template.'''
    # Use the template specified on the command line
    params = get_params(args)
    templates = args['<template>']
    if len(templates) != 1:
        print 'Please specify exactly one template.'
    params['note_template'] = templates[0]
    brain.new_note_interactive(**params)

def minion_remind(args):
    '''Set a quick reminder.'''
    # Don't open it, just make it.
    params = get_params(args)
    params['quick'] = True
    brain.new_note_interactive(**params)

def minion_here(args):
    '''Create a Minion note in the current working directory.'''
    params = get_params(args)
    # Use current directory
    params['notes_dir'] = os.curdir
    brain.new_note_interactive(**params)

def minion_note(args):
    '''Create a Minion note.'''
    # It's the most common use, so use the default PARAMS exactly.
    params = get_params(args)
    brain.new_note_interactive(**params)

def minion_log(args):
    '''Add a quick additional line to an existing (or new) Minion file.'''

    # Find the log file.
    params = {
        'filter': [args['<log>']],
        'archives': args['--archives'],
    }
    filename, match_files = brain.choose_file(**params)
    if not filename:
        title = ("Too many matches for log "
                 "function with keyword '{}'").format(args['<log>'])
        brain.display_output(title, match_files, max_display=10)
        return False

    params = {
        'filename': filename,
        'line': ' '.join(args['<comment>']),
    }

    brain.log_line_to_file(**params)



# Methods organize notes. 
# ----------------------------

def minion_sort(params):
    '''Interactively sort all matches.'''
    match_files = get_match_files(args)
    if len(match_files) == 0:
        print CLEAN_SORT_MESSAGE
    else:
        brain.sort_files_interactive(match_files)

def minion_strays(args):
    ''' Run an interactive sort on the contents of any folders that
        only have one or two items.
    '''
    match_files = brain.list_stray_files()
    total = len(match_files)
    if total == 0:
        print CLEAN_STRAYS_MESSAGE
        sys.exit()
    else:
        # print brain.getOutput('cal')
        brain.sort_files_interactive(match_files)

# Methods access notes. 
# ----------------------------

def minion_open(args):
    match_files = get_match_files(args)
    search_filter = args['<text>']

    if len(match_files) > 0:
        (_, filename) = brain.select_file(match_files, args['--max'])
        brain.open_in_editor(filename)
    else:
        brain.display_output(title=search_filter, output=match_files)


def minion_openall(args):
    match_files = get_match_files(args)
    brain.open_files(match_files, max=args['--max'])



def minion_view(args):
    ''' Dump the contents of the chosen file(s) to standard out. '''
    match_files = get_match_files(args)
    print "Outputting contents of %(number)d matches to search terms \
        '%(terms)s'.".format(number=len(match_files), terms=args['<text>'])
    for filename in match_files:
        brain.file_to_stdout(filename)

def minion_dates(args):
    '''Display all notes with dates in them and filtered by keywords.'''
    events = dict()
    match_files = get_match_files(args)
    for filename in match_files:
        content = brain.get_file_content(filename)
        dates = brain.get_unique_dates(content)
        if dates:
            for date in dates:
                try:
                    if date in events:
                        events[date].append(filename)
                    else:
                        events[date] = [filename]
                except ValueError:
                    # Date before 1900
                    _LOGGER.warn('Encountered date before 1900.')

    days_back = int(brain.get_setting('notes', 'default_recent_days'))
    recent_date = datetime.datetime.today() - datetime.timedelta(days=days_back)
    recent_date = recent_date.date()
    upcoming = dict()
    recent = dict()
    today = dict()
    # Sort the events into three sets - past, today and upcoming
    today_date = datetime.datetime.today().date()
    for key in events:
        date_str = key.strftime(get_date_format())
        if key > today_date:
            upcoming[date_str] = events[key]
        elif key == today_date:
            today[date_str] = events[key]
        elif key > recent_date:
            recent[date_str] = events[key]

    brain.display_output('Recent Dates', recent)
    print
    brain.display_output('Today', today)
    print
    brain.display_output('Upcoming Dates', upcoming)
    print


def minion_recent(args):
    ''' Show N most recent notes'''
    try:
        days_back = int(args['--days'])
    except (ValueError, TypeError):
        days_back = int(brain.get_setting('notes', 'default_recent_days'))

    match_files = get_match_files(args, days=days_back)
    recent_files = brain.list_recent(match_files)
    print "Notes modified in last %s days (most recent last):" % days_back
    brain.display_output(
        title=args['<text>'],
        output=recent_files,
        raw_files=args['--files'])


def minion_last(args):
    ''' Open the most recently modified file. '''
    filename = brain.get_last_modified(archives=args['--archives'])
    brain.open_in_editor(filename)

###############################################################################
# MAIN SCRIPT
###############################################################################

CONFIG_FILE = ''

PARAMS = {}

###############################################################################
# Shared parameters
#
#   These parameters are used by many function calls below.
###############################################################################

def get_params(args):
    ''' Return some parameters common to many methods. '''
    PARAMS = {
        'topic_fragments': args['<text>'],
        'notes_dir': None,
        'note_template': None,
        'quick': False
    }

# Assign folder per command line parameter
    if args['--folder']:
        folder = os.path.expanduser(args['--folder'])
        notes_home = brain.get_notes_home()
        PARAMS['notes_dir'] = os.path.join(notes_home, folder)

    if args['--template']:
        PARAMS['note_template'] = args['--template']

    if args['--quick']:
        PARAMS['quick'] = True

    return PARAMS

# *************************************************************
# Everything after this point requires searching for matches...
# *************************************************************

# Collect stories
def minion_collect(args):
    search_filter = args['<text>']
    if '<year>' in args:
        YEAR = args['<year>']
        match_files = get_match_files(args)
        collected_matches = brain.limit_to_year(YEAR, match_files)
        collection_title = 'Collected-%s-%s' % (YEAR, ' '.join(search_filter))

        print "%d/%d %s stories occur in year %s" % (
            len(collected_matches),
            len(match_files),
            search_filter,
            str(YEAR),
        )
    else:
        collected_matches = match_files
        collection_title = 'Collected-%s' % (' '.join(search_filter))

    brain.display_output(collection_title, collected_matches)

    collected_string = collection_title

    sorted_matches = sorted(collected_matches, key=date_sort)

    for filename in sorted_matches:
        # Don't include past collections...
        if should_collect(filename):
            f = open(filename, 'r')
            lines = f.read()
            f.close()
            collected_string += '\n'
            collected_string += '\n'
            collected_string += lines

    collected_filename = brain.get_filename_for_title(collection_title)

    f = open(collected_filename, 'w')
    f.write(collected_string)
    f.close()
    brain.display_output('Created Collection', collected_filename)

def minion_command(args):
    if args['<command>'] and args['<filename>']:
        brain.apply_command_to_file(
            args['<filename>'],
            args['<command>'])

def minion_count(args):
    search_terms = "%s: %s" % (
        os.path.basename(brain.get_notes_home()), ','.join(args['<text>'])
    )
    match_files = get_match_files(args)
    count = len(match_files)
    print "%d - %s" % (count, search_terms)
    sys.exit()

# List the results
def minion_find(args):
    search_filter = args['<text>']
    find_any = False
    if args['find']:
        find_any = True
    match_files = brain.find_files(filter=search_filter, archives=args['--archives'],
                                   find_any=find_any)

    # Set archives if no finds...
    total = brain.get_total_file_count(args['--archives'])

    # Display results / total
    notes_home = brain.get_notes_home()
    match_template = "{matching} of {total} files match search " +\
        "'{search}' in directory {directory}"
    print match_template.format(
        directory=notes_home,
        matching=len(match_files),
        search=','.join(search_filter),
        total=total)

    # Display results
    # print match_files
    brain.display_output(
        title=None,
        output=match_files,
        raw_files=args['--files'],
    )

    sys.exit(0)

def minion_list(args):
    minion_find(args)

def minion_favorites(args):
    print brain.print_favorites_summary()

def minion_summary(args):
    summary = brain.get_folder_summary(archives=args['--archives'])
    limit = int(args['--max'])
    summary = summary[:limit]
    output = format_2_cols(summary)
    print output

def minion_folder(args):
    # Do interactive inbox search, but for directories, not files
    print "Not implemented yet."

def minion_folders(args):
    updated_files = []
    # match_files = get_match_files(args)
    match_files = brain.find_files()
    # All poorly used folders
    too_few = 5
    notes_home = brain.get_notes_home()
    for folder in os.listdir(brain.get_notes_home()):
        folder = os.path.join(notes_home, folder)
        if os.path.isdir(folder):
            if len(os.listdir(folder)) < too_few:
                items = brain.find_files(filter=folder)
                for item in items:
                    updated_files.append(item)

    match_files = updated_files

    total = len(match_files)
    count = 0
    for item in match_files:
        count += 1
        print brain.to_bar(count, total)
        _ = brain.doInboxInteractive(item)

def minion_make_config(args):
    ''' Create the default config file. '''
    brain.get_settings(config_file = args['--config'])

def minion_tags(args):
    # Rid of this. Concept of 'tags' does not play well with the
    #       filesystem.
    # Switch to simply using any word as a 'tag'.
    # So what is 'poorly tagged'? Too short of a name? Too many common words?

    # A 'tag cloud' would be pretty awesome...
    notes_home = brain.get_notes_home()
    all_files = brain.find_files()
    word_count = dict()
    for filename in all_files:
        filename = filename.replace(notes_home, '')
        filename = filename.replace('/', '-').replace('.', '-')
        words = filename.split('-')
        print words
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    # word_count.sort()
    print word_count


# Run all the things!!!!
if __name__ == '__main__':

    # Parse the input arguments; see docopt manual on github.com
    args = docopt(__doc__, version=VERSION)
    # _LOGGER.debug(args)
    CONFIG_FILE = args['--config']
    _LOGGER.info('Using config file %s', CONFIG_FILE)
# brain.CONFIG_FILE = CONFIG_FILE
    brain.GLOBAL_SETTINGS = brain.get_settings(CONFIG_FILE)

# Search terms to filter by.
    search_filter = args['<text>']
    if args['<text>'] == ['all']:
        args['<text>'] = []

    # Run any method named in the keyword args.
    # Cool hack: use DocOpt args to call methods in this file.
    # Note that this only avails those methods whose name matches a documented
    #     arg.

    for method in dir():
        argname = method.replace('minion_', '')
        if (argname in args) and args[argname]:
            if hasattr(locals()[method], '__call__'):
                # print "Running {}".format(method)
                locals()[method](args)

    sys.exit(0)
