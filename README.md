Minion
======

Personal command line assistant. Takes notes, tags notes, finds notes, gets things done.

Setup
-----
Copy the example .minion file to your home directory, and edit it as needed.
Edit your bash/zsh/sh profile to add `source ~/Minion/add_to_your_profile`.

Usage
-----

minion --new-note Meet with Mr. Gordon.
will create a new note file in your inbox (as set by your .minion file, or the `$NOTES_HOME` environment variable.) This file will be fetched by minion in various useful ways.

Calling minion with a command line argument will search for that term (or terms):

`minion urgent` will list anything in the notes directory (outside of the archive folders) with 'urgent' in the file name or text body.

`minion --open cave security plan`
will search for all files with all three search terms, regardless of their order or location. If there are multiple matches, the matches will be displayed, and you will be prompted for additional search terms. Once enough terms have been added to find a unique match, the file will be opened in your preferred editor as set by your ~/.minion configuration file or your $EDITOR environment variable. You may override by calling minion with the --editor= flag. Minion has some experimental code for matching binay formats with appropriate viewers (pdf, etc), but it is not yet full featured.

This command will step you through your inbox:
minion inbox

Here are some handy things you can do when stepping through results:

a - archive - Move the file into the 'Archive.YYYY.MM' folder.
d - done - Move the file into the 'Archive.YYYY.MM' folder.
r - rename - Lets you type in a new name. Renaming resets all tags, so retype any tags that you want to keep.
v - view the file inline
>later - Move the file into a folder next to the inbox called 'later'
@email - Add an @email tag to the file name, to assist with searching later.
You can combine any number of tags with a single folder move, so this command is valid:
@email @alfred >later

This creates a file in your notes folder.

Get some things done
--------------------
Use tags and categories as recommended in your favorite organizational book.
I recommend symlinking ~/inbox to your actual inbox location, for those rare occassions when you need to create a file from some source other than minion.
Anything in a title starting with @ is a tag.
The name of a folder can act like a category.

Some tags or categories that might get you started on the right foot:
@monday, @tuesday, etc.
@today, @tomorrow
@soon, @someday
@alfred, @email, @calendar, @online, @quick

Tips
----
The file system can be a decent way to stay organized. You may decide to open your favorite file manager once in awhile to take stock or move things quickly. minion is named minion because it serves without question. It won't mind.

Minion will create new folders dynamically as you work, and never loses track of anything. Experiment with your categories and tags until you find what works for you. 

Use minion with Dropbox or a similar service to keep all of your reminders in sync.

If you use mutt for your email, remember that you can save messages or entire message chains into one of your minion managed directories, and minion will treat them just like any other full text reminder. 

When downloading instructions that you want to follow later, remember that minion does not mind an occasional pdf file dropped into a minion managed directory, so long as all the description you need is contained in the file name (since minion can only read the file names of, not the contents of binary files such as pdf files).

HTML files are text inside, so minion can search them. Sometimes saving an entire webpage's raw HTML into a minion directory is a good way to set a reminder.
