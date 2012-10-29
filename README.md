Minion
======

Personal command line assistant. Takes notes, tags notes, finds notes, gets things done.

Examples
--------

minion --new-note Meet with Mr. Gordon.

Calling minion with a command line argument will search for that term (or terms):

'minion urgent' will list anything in the notes directory (outside of the archive folders) with 'urgent' in the file name or text body.

minion --open cave security plan
will search for all files with all three search terms, regardless of their order or location. If there are multiple matches, the matches will be displayed, and you will be prompted for additional search terms. Once enough terms have been added to find a unique match, the file will be opened in your preferred editor as set by your ~/.minion configuration file or your $EDITOR environment variable. You may override by calling minion with the --editor= flag. Minion has some experimental code for matching binay formats with appropriate viewers (pdf, etc), but it is not yet full featured.

This command will step you through your inbox:
minion inbox

Here are some handy things you can do when stepping through results:
v - view the file inline

a - archive - Move the file into the 'Archive.YYYY.MM' folder.
d - done - Move the file into the 'Archive.YYYY.MM' folder.
>later - Move the file into a folder called 'later'
@email - Add an @email tag to the file name, to assist with searching later.
You can combine any number of tags with a single folder move, so this command is valid:
@email @alfred >later

This creates a file in your notes folder.

Tips
----
Use it with Dropbox or a similar service to keep all of your reminders in sync.


