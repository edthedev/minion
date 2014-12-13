## Minion

[![Build Status](https://travis-ci.org/edthedev/minion.svg?branch=develop)](https://travis-ci.org/edthedev/minion)

Minion is a digital assitant that runs on the command line and stores everything in text files. Minion takes notes, tags notes, finds notes, and gets things done.

Minion is compatible with other systems. Minion creates, finds, sorts and archives files in a folder using subfolders on the filesystem. Because Minion uses plain text files, it is already compatible with other software.

In particular, Minion is well complimented by the following:
 
1. A great text editor. The best editors can be configured to run Minion commands as shortcuts without leaving the editor.
2. A file folder synchronizer. Minion stores everything in files, so  synchronization software can make Minion content available from any location.

## Latest Thoughts

Minion is a great tool for 'being caught up', but I would like it to grow toward being a great tool for being effective. As part of this, I hope to soon be able to provide built-in functionality, or suggested use cases for using Minion to track goals as well as tasks. At the moment, I'm experimenting with just adding a tag called 'goal' to some files, and making command line aliases treat that tag in ways that increase visibility of goal items.

## What Minon Does

In Vernor Vinge's novel, 'The Peace War', chess players can instantly upload thoughts from their minds into a computer for storage, and then recover and act on those thoughts later. Minion is meant to be a first step on that path. Minion takes care of storing, tagging, and retrieving ideas, freeing it's user to focus on thinking.

1. Capture thoughts. The note function gets an editor open to capture thoughts quickly.
2. Take next steps. Convert captured ideas into actions and artifacts. The sort function makes it simple to review files and take next steps related to them.
3. Never lose anything. The find, open and archive commands make sure that files are only a few keypresses away.
4. (beta) Keep track of upcoming dates. The dates function displays recent and upcoming date strings that appear in files.

## Installation

See either [Command Line Install](https://github.com/edthedev/minion/wiki/Install) or [Vim Plugin Install](https://github.com/edthedev/minion/wiki/Install_Vim_Plugin).

## Usage

See [Command Line Use](https://github.com/edthedev/minion/wiki/Command_Line_Use) or [Vim Plugin Use](https://github.com/edthedev/minion/wiki/Vim_Plugin_Use).

## Tips

1. Since Minion uses the existing file system to organize your notes, it is compatible with other systems that do the same. Minion accepts all incoming changes, so it is perfectly acceptable to use alternate tools to move files around under Minions nose. Minion will adapt and continue to help you create and find files located under the Minion 'NOTES_HOME' directory.

2. The file system can be a decent way to stay organized. You may decide to open your favorite file manager once in awhile to take stock or move things quickly. minion is named minion because it serves without question. It won't mind.

3. Minion will create new folders dynamically as you work, and never loses track of anything. Experiment with your categories and tags until you find what works for you. 

4. Use minion with [Dropbox](http://dropbox.com), [Copy.com](http://copy.com) or a similar service to keep all of your reminders in sync.

5. If you use **mutt** for your email, remember that you can save messages or entire message chains into one of your minion managed directories, and minion will treat them just like any other full text reminder. 

6. When downloading instructions that you want to follow later, remember that minion does not mind an occasional pdf file dropped into a minion managed directory, so long as all the description you need is contained in the file name (since minion can only read the file names of, not the contents of binary files such as pdf files).

7. HTML files are text inside, so minion can search them. Sometimes saving an entire webpage's raw HTML into a minion directory is a good way to set a reminder.
