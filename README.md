## Minion

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

## Installation for command line

Minion requires [Python2](http://python.org).

1. Clone the source code from GitHub:

	```
	git clone https://github.com/edthedev/minion
	```

2. Configure your shell:
	* `bash`/`zsh`/`sh`:
		
		Add the following to your profile (e.g. `~/.bashrc`):
		
		```sh
		source ~/minion/add_to_your_profile
		```
	* `fish`:
		
		Add the following to your `~/.config/fish/config.fish`
		
		```sh
		set -x MINION_INSTALL $HOME/minion
		
		if [ -d "$MINION_INSTALL" ]
			set -x PATH $MINION_INSTALL $PATH
		end
		
		# Some optional aliases, to get started.
		# Uncomment the ones you want.
		alias mn="minion"
		# alias icannotfind="minion open --archive --full"
		# alias newnote="minion note"
		# alias open="minion open"
		# alias remind="minion remind"
		# alias summary="minion summary" 
		# alias favorites="minion favorites"
		```

3. Run Minion once to ensure that a default `~/.minion` file gets created.

	```
	minion dates .
	```

4. Edit `~/.minion` to set your notes directory.

	```
	[notes]
	home = ~/Documents
	```

5. Optionally, edit `~/.minion` to modify the default editor, templates, and text file extension.

	```
	[compose]
	templates = /Users/edward/.vim/bundle/minion/plugin/../templates
	extension = .md
	editor = vim
	```

#### Or: Installation as a Vim plugin
*You can use minion in the command line as well as in VIM, just be sure to keep
your configuration files set to one method!*

This plugin is packaged for use with
[Vundle](https://github.com/gmarik/vundle/blob/master/README.md). This plugin requires [Vim](http://vim.org/about.php) to be compiled with [Python]( http://python.org) support.

1. Install Vundle and then add `edthedev/minion` to your .vimrc:

	```
	Bundle 'edthedev/minion'
	```

2. Then, from within Vim, run BundleInstall:

	```
	:BundleInstall
	```

3. Copy and set .minion file accordingly:

	```
	mv ~/.vim/bundle/minion/DOTminion ~/.minion
	```

4. Edit `~/.minion` to set your notes directory.

	```
	[notes]
	home = ~/Documents
	```

5. Optionally, edit `~/.minion` to modify the default editor, templates, and text file extension.

	```
	[compose]
	templates = /Users/edward/.vim/bundle/minion/plugin/../templates
	extension = .md
	editor = vim
	```

6. Change the `MINION_INSTALL` variable to `$HOME/.vim/bundle/minion` in
`~/.vim/bundle/minion/add_to_your_profile`.

7. Configure your shell:
	* `bash`/`zsh`/`sh`:
		
		Add the following to your profile (e.g. `~/.bashrc`):
		
		```sh
		source ~/.vim/bundle/minion/add_to_your_profile
		```
	* `fish`:
		
		Add the following to your `~/.config/fish/config.fish`
		
		```sh
		set -x MINION_INSTALL $HOME/.vim/bundle/minion
		
		if [ -d "$MINION_INSTALL" ]
			set -x PATH $MINION_INSTALL $PATH
		end
		
		# Some optional aliases, to get started.
		# Uncomment the ones you want.
		alias mn="minion"
		# alias icannotfind="minion open --archive --full"
		# alias newnote="minion note"
		# alias open="minion open"
		# alias remind="minion remind"
		# alias summary="minion summary" 
		# alias favorites="minion favorites"
		```

## Usage

Create a new note in your inbox folder:

```
minion remind Need to Meet with Mr. Gordon on Monday
```

Your inbox folder is a subfolder of your `$NOTES_HOME` folder, which is determined by your .minion file, or the `$NOTES_HOME` environment variable. The default value is `~/Notes`, but I typically change it to `$NOTES_HOME` to `~/Dropbox/notes`, since I am a Dropbox user.

Because it is inside a subfolder of the notes folder, the file you just created can now be instantly recalled by minion in various useful ways.

Calling minion with a command line argument will search for that term (or terms):

To list every file that mentions `gordon`:

```
minion list gordon
```

This will list anything in the notes directory (outside of the archive folders) with `gordon` (case insensitive) in the file name or text body.

To immediately open a note after creating it, use the `note` command instead of `remind`:

```
minion note cave security plan
```

To open a specific file, use the 'open' command with enough keywords to uniquely match a file you have already created:

```
minion open cave security plan
```

This will search for all files with all three search terms, regardless of their order or location. If there are multiple matches, the matches will be displayed, and you will be prompted for additional search terms. Once enough terms have been added to find a unique match, the file will be opened in your preferred editor.

Configure your preferred editor in either your ~/.minion configuration file or your $EDITOR environment variable. You may also override your setting by calling minion with the --editor= flag. Minion will also detect some binary files and open them with an appropriate viewer on Linux, but this feature is still in Beta.

To see a summary of everything you have stored in Minion folders:

```
minion summary
```

```
164 - someday
51 - journal
44 - wiki 
28 - pics 
23 - soon 
22 - teddy
16 - blog 
13 - next 
4 - waiting
4 - today
```

This command will step you through your inbox:

```
minion sort inbox
```

Here are some handy things you can do when stepping through results:

```
a - archive - Move the file into the 'Archive.YYYY.MM' folder.
d - done - Delete the file (after confirmation).
r - rename - Lets you type in a new name. Renaming resets all tags, so retype any tags that you want to keep.
v - view the file inline
>later - Move the file into a folder next to the inbox called 'later'. If the folder does not exist yet, it will be created.
@email - Add an @email keyword to the file name, to assist with searching later.
```

You can combine any number of additional keywords with a single folder move, so this command is valid:

```
@email @alfred >later
```

### Setting and using `dates`

1. Create a note:

	```
	minion note NOTENAME
	```

2. This opens the file NOTENAME.txt which shoud look like this:

	```
	NOTENAME
	====
	:date: 2014-03-04
	```


3. Change the date accordingly. 

4. List all notes with their according dates:

	```
	minion dates txt
	```

### Print the contents of all files matching 'foo' to standard output.

```
minion view foo | more
minion view foo --max=1 | more
```

## Tips

1. Since Minion uses the existing file system to organize your notes, it is compatible with other systems that do the same. Minion accepts all incoming changes, so it is perfectly acceptable to use alternate tools to move files around under Minions nose. Minion will adapt and continue to help you create and find files located under the Minion 'NOTES_HOME' directory.

2. The file system can be a decent way to stay organized. You may decide to open your favorite file manager once in awhile to take stock or move things quickly. minion is named minion because it serves without question. It won't mind.

3. Minion will create new folders dynamically as you work, and never loses track of anything. Experiment with your categories and tags until you find what works for you. 

4. Use minion with [Dropbox](http://dropbox.com), [Copy.com](http://copy.com) or a similar service to keep all of your reminders in sync.

5. If you use **mutt** for your email, remember that you can save messages or entire message chains into one of your minion managed directories, and minion will treat them just like any other full text reminder. 

6. When downloading instructions that you want to follow later, remember that minion does not mind an occasional pdf file dropped into a minion managed directory, so long as all the description you need is contained in the file name (since minion can only read the file names of, not the contents of binary files such as pdf files).

7. HTML files are text inside, so minion can search them. Sometimes saving an entire webpage's raw HTML into a minion directory is a good way to set a reminder.
