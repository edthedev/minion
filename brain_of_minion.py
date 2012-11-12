import subprocess
import shutil
import os
import datetime
import re
import socket
import ConfigParser
import string
import random
from string import Template
import string
from ConfigParser import SafeConfigParser

# from bottle import route, run

def remind(text):
    filename = "%s/%s" % (get_inbox(), createFileName(text))
    f = open(filename, 'a')
    f.write(text)
    return filename

class WebTemplate(object):
    def __init__(self, template="", data={}):
        self.Template = template 
        self.Data = data 
    def __str__(self):
        return self.webify(self.Data)
    def render(self):
        web_data = {}
        for key in self.Data:
            web_data[key] = self.webify(key, self.Data[key])
        return string.Template(self.Template).substitute(web_data)
    def __iter__(self):
        return self
    def next(self):
        yield(HTTPResponse(str(self)))

    @staticmethod
    def webify(title, content):
        result = "<div id=" + title + ">"
        result += "<h2>" + title + "</h2>"
        if getattr(content, '__iter__', False):
            result += "<ul>"
            for item in content:
                item = cleanOutput(item)
                result += "<li>" + item + "</li>"
            result += "</ul>"
        else:
            result += content
        result += "</div>"
        return result

# @route('/')
def getStatus():
    data = {}
    data['home'] = get_notes_home()
    data['inbox_content'] = find_files(get_inbox())
    page = """
    Notes home: $home
    <a href='/tags'>tags</a>
    <a href='/folders'>folders</a>
    $inbox_content
    """
    return WebTemplate(page, data).render()

def is_work_time():
    today = datetime.datetime.today()
    weekend = (today.weekday() > 4)    
    if weekend:
        return False
    if today.hour >= 8 and today.hour < 17:
        return True
    return False

# @route('/ignore')
def get_ignore_tags(worktime=False):
    if worktime:
        return [
            "@home",
            "@errand",
            "@house",
            "@wishlist",
            "@garage",
        ]
    else:
        return [
            "@work",
            "asih",
            "ssl",
            "compreg",
            "owasp",
            "scanning",
        ]

def getIgnoredTags(script_name=''):
    cp = ConfigParser.ConfigParser()

    settings_file = string.Template("~/.edthedev/$hostname").substitute(hostname=socket.gethostname())
    #print settings_file
    ignore = []
    settings_file = os.path.expanduser(settings_file)
    if os.path.exists(settings_file):
        result = cp.read([settings_file])
        if len(result) < 1:
            print "Settings file not loaded. %s" % settings_file

        ignore = cp.get('inbox', 'ignore_tags')
        ignore = ignore.replace(' ', ',')
        ignore = ignore.split(',')
    return ignore

#@route('/folders')
# def webFolders(location=None):
#    return webify(getFolders(location)) 

def getFolders(location=None):
    if location == None:
        location = get_notes_home()
    folders = os.listdir(location)
    return folders

def ignoreTags(file_list, tags=[]):
    match_files = []
    for f in file_list:
        success = True
        for term in tags:
            success = success and (term not in f.lower())
        if success:
            match_files.append(f)
    return match_files
    
def getTaggedLines(tags, filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    result = []
    for line in lines:
        low_line = line
        for tag in tags:
            match = True
            if tag not in low_line:
                match = False
            if match:
                result.append(line)
    return result

# @route('/tag/:tags')
def getTaggedFiles(tags, full=False):
    all_files = getAllFiles(archives=False)
    for tag in tags:
        all_files = limitNotes(tag, all_files, full)
    return all_files

def getTodayTags():
    today_tags = [
":%s" % datetime.datetime.today().strftime('%B%d'),
"@%s" % datetime.datetime.today().strftime('%B%d'),
# "@%s%s" % (datetime.datetime.today().strftime('%B'), datetime.datetime.today().strftime('%d').lstrip('0')),
]
    return today_tags

def getTomorrowTags():
    return [
    "@%s" % (datetime.datetime.today()+datetime.timedelta(days=1)).strftime('%B%d'),
    ":%s" % (datetime.datetime.today()+datetime.timedelta(days=1)).strftime('%B%d'),
    ]

# # # # # # # # # @route('/sample/:tags')
def sampleTagged(tags):
    matching_files = getTaggedFiles(tags, full=False)
    non_cal_files = removeNotes(matching_files, ['calendar'])
    if len(non_cal_files) > 0:
        sample_file = random.choice(non_cal_files)
        sample_text = sample_file
        if isProject(sample_file):
            matching_lines = getTaggedLines(tags, sample_file)
            if len(matching_lines) > 0:
                sample_text += '\n' + random.choice(matching_lines)
        return [sample_text] 
    else:
        return [] 

def removeArchives(file_list):
    return removeNotes(file_list, ['archive'])

def removeNotes(file_list, terms):
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

def getRemoveTags(text_string):
    tag_re = re.compile("-@\w*")
    tags = tag_re.findall(text_string)
    return tags

def getTags(text_string):
    tag_re = re.compile("@\w*")
    tags = tag_re.findall(text_string)
    return tags

def tagAfter(first, second):
    big_number = random.randint(0, 100000)
    before_tag = "@before%d" % big_number
    after_tag = "@after%d" % big_number

    tagFile(first, before_tag)
    tagFile(second, after_tag)
    tagFile(second, "@waiting")

def isProject(filename):
    for tag in ['.org', 'project']:
        if tag in filename:
            return True
    return False

def removeWorkNotes(files, worktime=True):
    ignore_tags = get_ignore_tags(worktime)
    return removeNotes(files, ignore_tags)

def isValidTag(tag):
    if tag.isdigit():
        return False
    if tag in ['.txt', 'get', 'not', 'it', 'is', 'a', 'at', 'out', 'of', 'and', 'on', 'in', 'with', 'about', 'to', 'the', 'from', 'for', 'if']:
        return False
    return True

def chooseFileByTags(file_list, tags):
    new_array = []
    for note in file_list:
        match = True
        for tag in tags:
            if not tag in note:
                match = False
        if match:
            new_array.append(note)
    return new_array

def sort_by_tag(file_list):
        all_tags = {'no tags':[]}
        for item in file_list:
                if len(getTags(item)) == 0:
                        all_tags['no tags'].append(item)
                for tag in getTags(item):
                        if all_tags.has_key(tag):
                                all_tags[tag].append(item)
                        else:
                                all_tags[tag] = [item]
        output = ''
        for tag in all_tags:
                if len(all_tags[tag]) > 1:
                        output += '\n\t' + tag
                        output += "\n-------------------\n"
                        output += '\n'.join(all_tags[tag])
        return output

#def remove_duplicate_tasks(tagged_dict):
        #length_by_key = {}
        #for key in tagged_dict:
                #length_by_key[key] = len(tagged_dict[key])
                

def display_output(title, output, by_tag=True):
        if output == None:
                print "No %s tasks." % title
        elif len(output) == 0:
                print "No %s tasks." % title
        else:
                if not type(output) is list:
                        print output
                else:
                        if by_tag:
                                output = sort_by_tag(output)
                        else:
                                output = [x.replace('\n', '') for x in output]
                                output = '\n'.join(output)
                        if title != None:
                                print "\n---- %s: " % title
                                print "-------------------------"
                        print output

def cleanOutput(output):
        notes_folder = get_notes_home()
        no_folder = output.replace(notes_folder, '').replace('/', ' ')
        no_dashes = no_folder.replace('-', ' ')
        no_extensions = no_dashes.replace('.txt', '')
        return no_extensions

def chooseFileByTagsInteractive(file_list, tags=[]):
    file_list = chooseFileByTags(file_list, tags)
    all_tags = tags
    while len(file_list) > 1:
        display_output('Matches', '\n'.join(file_list))
        more_tags = getTags(raw_input("More tags?"))
        all_tags.extend(more_tags)
        file_list = chooseFileByTags(file_list, more_tags)

    if len(file_list) < 1:
        new_file = '%s/%s.txt' % (get_inbox(),'-'.join(all_tags))
        open(new_file, 'w').close() 
        print "Created a new file in inbox called: %s" % new_file
        filename = new_file
    else:
        filename = file_list[0]    
    return filename    

def parseTags(input_string):
    input_string = input_string.replace('\n' ,' ')
    tags = input_string.split(' ')
    #proper_tags = []
    #for tag in tags:
    #    if 
    return tags

#!/bin/python2.5

def getMatchingFiles(search_terms, file_list):
    lower_terms = [item.lower() for item in search_terms]
    match_files = []
    for f in file_list:
        success = True
        for term in lower_terms:
            success = success and (term in f.lower()) 
        if success:
            match_files.append(f)
    return match_files

def getProject(project_name):
    matching = []
    for project in getCurrentProjects():
        if project_name in project:
            matching.append(project)
    if len(matching) == 0:
        return newNote(project_name, 'org') 
    if len(matching) == 1:
        return matching[0]
    else:
        return limitNotesInteractive(matching)

def getTaggedLines(tags, filename):
    f = open(filename)
    lines = f.readlines()
    f.close()
    result = []
    for line in lines:
        low_line = line
        for tag in tags:
            match = True
            if tag not in low_line:
                match = False
            if match:
                result.append(line)
    return result

def sampleTagged(tags):
    matching_files = getTaggedFiles(tags, full=False)
    non_cal_files = removeNotes(matching_files, ['calendar'])
    if len(non_cal_files) > 0:
        sample_file = random.choice(non_cal_files)
        sample_text = sample_file
        if isProject(sample_file):
            matching_lines = getTaggedLines(tags, sample_file)
            if len(matching_lines) > 0:
                sample_text += '\n' + random.choice(matching_lines)
        return [sample_text] 
    else:
        return [] 

def getTaggedFiles(tags, full=False):
    all_files = getAllFiles(archives=False)
    for tag in tags:
        all_files = limitNotes(tag, all_files, full)
    return all_files

def getCurrentProjects(): 
    current_projects = getTaggedFiles(['@project'])
    current_projects.extend(getTaggedFiles(['.org']))
    return current_projects
    
def isProject(filename):
    for tag in ['.org', 'project']:
        if tag in filename:
            return True
    return False

def limitNotes(choice, notes, full=False):
    new_array = []
    for note in notes:
        choice = choice.lower()
        low_note = note.lower()
        if choice in low_note:
            if 'swp' not in note:
                new_array.append(note)
        else:
            if full or isProject(low_note):
                content = ''
                try:
                    f = open(note, 'r')
                    content = f.readlines()
                # print content
                    f.close()
                except:
                    pass
                content = ' '.join(content)
                content = content.lower()
                if choice in content:
                    new_array.append(note)
    return new_array

def removeArchives(file_list):
    return removeNotes(file_list, ['archive'])

def removeNotes(file_list, terms):
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

def getAllFiles(archives=True, folder=None):
    if folder == None:
        folder = get_notes_home()
    files = find_files(folder)
    if not archives:
        return removeArchives(files) 
    else:
        return files

def clean_file_name(text):
    return text.replace(' ', '-').replace('/', '-')

def isValidTag(tag):
    if tag.isdigit():
        return False
    if tag in ['.txt', 'get', 'not', 'it', 'is', 'a', 'at', 'out', 'of', 'and', 'on', 'in', 'with', 'about', 'to', 'the', 'from', 'for', 'if']:
        return False
    return True

def chooseFileByTags(file_list, tags):
    new_array = []
    for note in file_list:
        match = True
        for tag in tags:
            if not tag in note:
                match = False
        if match:
            new_array.append(note)
    return new_array

def chooseFileByTagsInteractive(file_list, tags=[]):
    file_list = chooseFileByTags(file_list, tags)
    all_tags = tags
    while len(file_list) > 1:
        display_output('Matches', '\n'.join(file_list))
        more_tags = getTags(raw_input("More tags?"))
        all_tags.extend(more_tags)
        file_list = chooseFileByTags(file_list, more_tags)

    if len(file_list) < 1:
        new_file = '%s/%s.txt' % (get_inbox(),'-'.join(all_tags))
        open(new_file, 'w').close() 
        print "Created a new file in inbox called: %s" % new_file
        filename = new_file
    else:
        filename = file_list[0]    
    return filename    

def parseTags(input_string):
    input_string = input_string.replace('\n' ,' ')
    tags = input_string.split(' ')
    #proper_tags = []
    #for tag in tags:
    #    if 
    return tags

def open_file(filename, line=0, multiple=False, editor=None):
    print "Opening %s" % filename
    programs = {
        '.pdf':'evince',
        '.xls':'libreoffice',
        }
    extension = os.path.splitext(filename)[1]
    if programs.has_key(extension):
        program = programs[extension]
        subprocess.call([program, filename])
        # subprocess.Popen([program, filename])
    else:
        if editor == None:
            try:
                editor = os.environ['EDITOR']
            except:
                editor = 'vim'
        subprocess.call([editor, filename, "+%d" % (line + 2)])
        # subprocess.Popen([editor, filename, "+%d" % (line + 2)])

def previewFile(filename, lines):
    result = displayNice(filename)
    f = open(full_path, 'r')
    line_count = 0
    lines = f.readlines()
    lines = [line.replace('\t', ' ') for line in lines]
    if len(lines) > 2:
        for line in lines:
            if 'done' in line.lower() or 'waiting' in line.lower() or 'someday' in line.lower():
                pass
            else:
                if (line_count < lines) and (len(line) > 0):
                    result += '\n'
                    result += line.replace('\n', '')
                    line_count = line_count +1
        if line_count >= lines: result += "\n..."

    output = ''
    first_found = False
    end_of_first_found = False
    for line in result.split('\n'):
        if len(line) == 0:
            if first_found:
                end_of_first_found = True
        else:
            if not end_of_first_found:
                output += '%s\n' % line
                first_found = True
    # print result
    return output

def get_settings():
    minion_file = os.path.expanduser('~/.minion')

# Default settings
    settings = SafeConfigParser()
    settings.add_section('notes')
    settings.set('notes', 'home', '~/notes')

# Load if available, write defaults if not.
    if os.path.exists(minion_file):
        settings.read([minion_file])
    else:
        f = open(minion_file, 'w')
        settings.write(f)
        f.close()

    return settings

def get_notes_home():
    # if os.environ.has_key('NOTES_HOME'):
    #     notes_home = os.environ['NOTES_HOME']
    # else:
    #     notes_home = '~/notes'
    #     print "Notes home has been set to %s. Export the NOTES_HOME variable to suppress this message." % notes_home
    settings = get_settings()

    notes_home = settings.get('notes', 'home')
    
    notes_home = os.path.expanduser(notes_home)
    if not os.path.exists(notes_home):
        os.mkdir(notes_home)
    return notes_home




def get_inbox():
    inbox = "%s/inbox" % get_notes_home()
    if not os.path.exists(inbox):
        os.mkdir(inbox)
    return inbox

def chooseBox(choice):
    boxes = getBoxes()
    selected = []
    for box in boxes:
        if choice[0] == box[0]:
            selected.append(box)
    if len(selected) == 1:
        return boxes[selected[0]]
    else:
        selected2 = []
        for box in selected:
            if choice in box:
                selected2.append(box)
        if len(selected2) == 1:
            return boxes[selected2[0]]
        else:
            return None

def getDir(folder):
    '''If in invalid folder is passed, assume a relative path 
    within the Inbox directory.'''
    if os.path.exists(folder):
        return folder
    notes_home = get_notes_home()
    if folder == 'archive':
        year_month = datetime.datetime.today().strftime("%y.%m")
        directory = os.path.expanduser("%s/archive.%s" % (notes_home, year_month))
    directory = os.path.join(notes_home, folder)
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory

def newNote(name, ext='txt'):
    clean_name = createFileName(name, ext)
    inbox = get_inbox()
    full_name = "%s/%s" % (inbox, clean_name)
    return full_name    

def limitNotesInteractive(notes):
    while len(notes) > 1:
        display_output('Multiple Matches', notes)
        choice = raw_input('Choice? ')
        notes = limitNotes(choice, notes)
    return notes[0]

def getCurrentMonth():
    return getMonthName(datetime.datetime.today().month)
def getNextMonth():
    return getMonthName((datetime.datetime.today()+datetime.timedelta(weeks=4)).month)
def getMonthName(number):
    return datetime.date(1900,number,1).strftime('%B')

def getUpcoming(full=False):
    results = []

    project_calendar = []
    current_projects = getCurrentProjects()

    for project_file in current_projects:
        project_calendar.extend( getCalendarItems( project_file ) )

    # Get results for this month.
    current_month = getCurrentMonth()
    this_month = getTaggedFiles([current_month])
    results.extend(this_month)
    this_month_project_cal = limitNotes(choice=current_month, notes=project_calendar)
    results.extend(this_month_project_cal)
    
# Get results for next month.
    if len(results) < 5 or full:
        next_month_tag = getNextMonth()
        next_month = getTaggedFiles([next_month_tag])
        results.extend(next_month)
        next_month_project_cal = limitNotes(choice=next_month_tag, notes=project_calendar)
        results.extend(next_month_project_cal)
    if full:
        return results
    else:
        return results[:5]

def getCurrentProjects(): 
    current_projects = getTaggedFiles(['@project'])
    current_projects.extend(getTaggedFiles(['.org']))
    return current_projects
    

def limitNotes(choice, notes, full=False):
    new_array = []
    for note in notes:
        choice = choice.lower()
        low_note = note.lower()
        if choice in low_note:
            if 'swp' not in note:
                new_array.append(note)
        else:
            if full or isProject(low_note):
                content = ''
                try:
                    f = open(note, 'r')
                    content = f.readlines()
                # print content
                    f.close()
                except:
                    pass
                content = ' '.join(content)
                content = content.lower()
                if choice in content:
                    new_array.append(note)
    return new_array

def makeProject(filename):
    basename, extension = os.path.splitext(filename) 
    new_filename = "%s.org" % (basename)
    shutil.move(filename, new_filename)
    print "Renamed to %s" % new_filename
    return new_filename

def expand_short_command(command):
    commands = {
        'a':'>wiki/archive',
        'w':'>wiki',
        'wc':'>wiki/cites',
        'wp':'>wiki/personal',
        'd':'>archive',
        'r':'!rename',
        '#':'!review',
        'v':'!view',
    }
    if commands.has_key(command):
        return commands[command]
    return command

def applyCommandToLine(filename, line, command):
    command = expand_short_command(command)
    updates = {}
    if '!rename' in command:
        line = raw_input('Updated line?')
        command = command.replace('!rename', '')
    if ':' in line:
        line = '%s %s' % (line, command)
    if '>archive' in command:
        line = toggleDone(line)
        pass
    return line

def applyCommandToFile(filename, command):
    '''
    The core of the interactive file sorting system.
    '''
    command = expand_short_command(command)
    orig_filename = filename
    # Rename:
    if '!review' in command:
        reviewProjectInteractive(filename)
    if '!rename' in command:
        new_name = command.replace('!rename', '')
        if len(new_name) == 0:
            new_name = raw_input('New name? ')
        new_name = createFileName(new_name)
        new_file = "%s/%s" % (get_inbox(), new_name)
        new_file = move_file(filename, new_file)
        # shutil.move(filename, new_file)
        # print "Renamed to %s" % new_file
        return new_file

    # Add tags
    add_tags = getTags(command)
    basename, extension = os.path.splitext(filename) 
    new_tags = '-'.join(add_tags)    
    if len(new_tags) > 0:
        filename = "%s.%s.%s" % (basename, new_tags, extension)
        print "Added tags: %s" % add_tags
    
    # Remove tags
    remove_tags = getRemoveTags(command)
    for remove_tag in remove_tags:
        filename = filename.replace(remove_tag, '')
        print "Removed tags: %s" % remove_tags
    
    #    Move file
    if len(remove_tags) > 0 or len(add_tags) > 0:
        filename = move_file(orig_filename, filename)
        # shutil.move(orig_filename, filename)
        # print "Re-tagged to %s" % filename

    # If there's a calendar tag...move to the calendar folder.
    if hasCalendarTag(command):
        filename = move_file(filename, 'calendar')
    else:
        # Move elsehwere if requested.
        folder_re = re.compile('>\S*')
        folders = folder_re.findall(command)
        if len(folders) > 0:
                #print folders
            folder = folders[0]
            folder = folder.replace('>', '')
            folder = os.path.expanduser(folder)
            filename = move_file(filename, folder)
            print "Moved to %s" % folder

    if '!view' in command:
            os.system('cat %s | less' % filename)
            doInboxInteractive(filename)

    return filename

# TODO: Remove references to handling files in 'project' mode?
# It was not working out well. Better to encourage users 
# to use one file per task.
def reviewProjectInteractive(filename):
    f = open(filename, 'r')
    content = f.readlines()
    f.close()
    total_lines = len(content)
    current_line = 0
    for line in content:
        current_line +=1
        if 'TODO' in line: 
            percentage = '%d/%d' % (current_line, total_lines)
            display_output(percentage, line, by_tag=False)
            choice = raw_input('Action? ')
            if len(choice) > 0:
                applyCommandToLine(filename, current_line, choice)

def doInboxInteractive(item):
    to_open = []
    # print get_inbox_menu()
    display_output('Selected', item, by_tag=False)
    choice = raw_input('Action? ')
    if len(choice) > 0:
        applyCommandToFile(item, choice)
        if choice == 'o':
            to_open.append(item)
    return to_open

def getCalendarTags():
    return ['@Jan', '@Feb', '@Mar', '@Apr', '@May', '@Jun', '@Jul', '@Aug', '@Sep', '@Oct', '@Nov', '@Dec', ':Jan', ':Feb', ':Mar', ':Apr', ':May', ':Jun', ':Jul', ':Aug', ':Sep', ':Oct', ':Nov', ':Dec']    

def hasCalendarTag(text):
    month_tags = getCalendarTags()
    for tag in month_tags:
        if tag in text:
            return True
    return False

def find_files(directory=None, archives=True, filter=[], full_text=False, weekend=None):
    if directory == None:
        directory = get_notes_home()

    files = []
    dirList = os.listdir(directory)
    # dirList.sort()
    for item in dirList:
        dirName = os.path.join(directory, item)
        if os.path.isdir(dirName):
            files.extend(find_files(dirName))
        else:
            if not item.endswith('~'):
                files.append("%s/%s" % (directory, item))
    
    if not archives:
        files = removeArchives(files)

    for tag in filter:
        files = limitNotes(tag, files, full=full_text)

    if weekend is not None:
        ignore_tags = get_ignore_tags(worktime=not weekend)
        files = ignoreTags(files, ignore_tags)

    return files

def getIgnoreString(worktime=False):
    return "-i %s" % ' -i '.join(get_ignore_tags(worktime))

def addUpdatedLine(filename):
    f = open(filename, 'r+')
    # Get the file length.
    line = sum(1 for line in f)
    # Append a timestamp to the file.
    if not '.pdf' in filename:
        timestamp = getUpdatedString()
        f.write(timestamp)
    f.close()
    return line


def chooseBox(choice):
    boxes = getBoxes()
    selected = []
    for box in boxes:
        if choice[0] == box[0]:
            selected.append(box)
    if len(selected) == 1:
        return boxes[selected[0]]
    else:
        selected2 = []
        for box in selected:
            if choice in box:
                selected2.append(box)
        if len(selected2) == 1:
            return boxes[selected2[0]]
        else:
            return None

def createFileName(text, ext='.txt'):
    new_name = text.replace(' ', '-').replace('/', '-')
    # if not (new_name.endswith('.txt') or new_name.endswith('.pdf')):
    if not new_name.endswith(ext):
        new_name = '%s%s' % (new_name, ext)
    return new_name

def move_file(filename, folder):
    try:
        destination = getDir(folder)
        print destination
        final_name = "%s/%s" % (destination, os.path.basename(filename))
        while os.path.exists(final_name):
            import uuid
            uid = str(uuid.uuid1())
            final_name = final_name.replace('.', \
                    '.' + uid + '.', 1)
        shutil.move(filename, final_name)
        print "Moved %s to %s" % (filename, final_name)
        return final_name 
    except Exception as ex:
        raise ex
        destination = get_inbox()
        new_file_name = "%s/%s" % (destination, os.path.basename(filename))
        print "Error: Moved %s to inbox." % filname
        shutil.move(filename, destination)

def archive(filename):
    archive_dir = getDir('archive') 
    cleaned_name = filename.replace('urgent', 'complete')
    if filename != cleaned_name:
        shutil.move(filename, cleaned_name)
        print "Renamed to %s" % cleaned_name
    final_name = '%s/%s' % (archive_dir, os.path.basename(cleaned_name))
    while os.path.exists(final_name):
        final_name = final_name.replace('.', '.duplicate.', 1)
    shutil.move(cleaned_name, final_name)
    print "Moved to %s" % final_name
    recordDone(filename)

def recordDone(item):
    clean_item = cleanOutput(item)
    done_file = "%s/done.txt" % (get_notes_home())
    appendToFile(done_file, clean_item)

def getCalendarItems(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    results = []
    for line in lines:
        low_line = line.lower()
        for cal_tag in getCalendarTags():
            if cal_tag in line:
                results.append(line)
    return results

if __name__ == '__main__':
    import bottle
    bottle.debug(True)
    run(host='localhost', port=8080)
import subprocess
import os

def get_inbox_menu():
        display_options = "Actions:\nrename tag email archive done"
        return display_options

def cleanOutput(output):
        notes_folder = os.path.expanduser('~/Dropbox/notes/')
        no_folder = output.replace(notes_folder, '')
        no_dashes = no_folder.replace('-', ' ')
        no_extensions = no_dashes.replace('.txt', '')
        return no_extensions

def previewFile(filename, lines):
    result = displayNice(filename)
    f = open(full_path, 'r')
    line_count = 0
    lines = f.readlines()
    lines = [line.replace('\t', ' ') for line in lines]
    if len(lines) > 2:
        for line in lines:
            if 'done' in line.lower() or 'waiting' in line.lower() or 'someday' in line.lower():
                pass
            else:
                if (line_count < lines) and (len(line) > 0):
                    result += '\n'
                    result += line.replace('\n', '')
                    line_count = line_count +1
        if line_count >= lines: result += "\n..."

    output = ''
    first_found = False
    end_of_first_found = False
    for line in result.split('\n'):
        if len(line) == 0:
            if first_found:
                end_of_first_found = True
        else:
            if not end_of_first_found:
                output += '%s\n' % line
                first_found = True
    # print result
    return output

#def getOutput(command):
#        # print command
        #command = command.replace('(', '\(').replace(')', '\)')
        #p1 = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        #output = p1.communicate()[0]
        #return output

def getOutput(command):
        p1 = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE)
        output = p1.communicate()[0]
        return output

def appendToFile(filename, content, timestamp=True):
        f = open(filename, 'a')
        if timestamp:
                f.write(getUpdatedString())
                f.write('\n')
        f.write(content)
        f.write('\n')
        f.close()
        print "%s updated." % filename


DONE = 'DONE:'
TODO = 'TODO:'
WAITING = ':WAITING:'

def toggleTodo(line):
        if DONE.lower() in line.lower():
                return line.replace(DONE, TODO).replace(DONE.lower(), TODO).replace('Done:', TODO)
        if TODO.lower() in line.lower():
                return line.replace(TODO, DONE).replace(TODO.lower(), DONE).replace('Todo:', DONE)
        return TODO + ' ' + line

def toggleWaiting(line):
        if WAITING.lower() in line.lower():
                return line.replace(WAITING, '').replace('@waiting', '')
        return WAITING + ' ' + line

def getDateString():
        return datetime.datetime.today().strftime("%a, %x %H:%M %p")

def getUpdatedString():
        return "\nUpdated: %s" % datetime.datetime.today().strftime("%H:%M %p, %a, %x")

def new_note(args, quick):
    notes_dir = get_inbox()

    if not os.path.exists(notes_dir):
        os.mkdir(notes_dir)

    topic = ' '.join(args)
    if len(topic) == 0:
        print getOutput('cal')
        topic = raw_input("Topic? ")

    topic_filename = createFileName(topic)
    print topic_filename

    today = datetime.date.today()
    filename = "%s/%s" %(notes_dir, topic_filename)
    underline = '=' * len(topic)
    summary = "%s\n%s\nCreated %s" % (topic, underline, today)

    f = open(filename, 'a')
    f.write(summary)
    f.close()

    if not quick:
        open_file(filename)
    print summary

def to_bar(number, total=10):
    pct_complete = number * 1.0 / total 
    print pct_complete
    result ='%s/%s [' % (number, total)

    FULL = '#'
    EMPTY = ' '
    for i in range(1, 10):
        if (i * .1)<=pct_complete:
            result+=FULL
        else:
            result+=EMPTY
    result+= ']'
    return result
    
def numbers_to_bars(text):
    output = ''
    args = text.split(' ')
    for arg in args:
        x = None
        try:
            x = int(arg)
        except:
            output += arg + ' '	
        if x != None:
            output += to_bar(x) + ' '
    return output
