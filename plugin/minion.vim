" ---------------------------------------------------------
"
"	Vim Bindings for the Minion command line file organizer.
"
" ---------------------------------------------------------

if !has('python')
	echo "Error: Minion requires vim compiled with +python"
		finish
	endif

" =================
" Minion Functions
" =================

let s:path = expand('<sfile>:p:h')

" " Open all Inbox files in buffers.
" -----------------------------------
function! MinionInbox()
python << EOF
import sys
import os
script_path = vim.eval('s:path')
lib_path = os.path.join(script_path, '..')
print lib_path 
sys.path.insert(0, lib_path)

import vim
import brain_of_minion as brain
match_files = brain.get_inbox_files()
for item in match_files:
	# Add everything to buffers.
	vim.command("badd %(item)s" % {'item':item})
	# Switch to the next buffer, in case we ran from an empty Vim window.
	vim.command("bn")
	# Show the list of open buffers.
	vim.command("buffers")
EOF
endfunction

" Archive the current open file.
" -------------------------------
function! MinionArchive()
	let s:current_file = expand('%')
python << EOF
import sys
import os
script_path = vim.eval('s:path')
lib_path = os.path.join(script_path, '..')
print lib_path 
sys.path.insert(0, lib_path)

import vim
import brain_of_minion as brain

current_file = vim.eval("s:current_file")

# This call will nicely display message on success, already.
brain.archive(current_file)
EOF
" Delete the buffer, since we moved the file.
bd
" echom "Archived " 

endfunction

" Sort the current file into a folder.
" -------------------------------------
function! MinionSort(command)
	let s:current_file = expand('%')
python << EOF
import sys
import os
script_path = vim.eval('s:path')
lib_path = os.path.join(script_path, '..')
print lib_path 
sys.path.insert(0, lib_path)

import vim
import brain_of_minion as brain

current_file = vim.eval("s:current_file")
current_command = vim.eval("a:command")
# TODO: Debug this call...
brain.apply_command_to_file(current_command, current_file)

EOF
endfunction

" ================
" Minion Commands
" ================

command! -nargs=0 MinionInbox call MinionInbox()
command! -nargs=0 MinionArchive call MinionArchive()
" TODO: Shorthand for Minion Sort...?
" command! -nargs=1 MinionArchive call MinionSort(foo?)

" ==========================
" Minion Keyboard Shortcuts
" ==========================

" Archive the current file and close it.
:map <Leader>ma :MinionArchive<Cr>

" Open all items in the Minion Inbox
:map <Leader>mi :MinionInbox<Cr>

" Apply a sort command to the current file.
" Allows arbitrary text to allow for folder names...
:map <Leader>ms :MinionSort


" Organizer help
:map <Leader>mh :!~/.vim/bundle/Minion/bin/minion --help<Cr>$

" New Note
:map <Leader>mn :!~/.vim/bundle/Minion/bin/minion --new-note

" Review this file
:map <Leader>mr :!~/.vim/bundle/Minion/bin/minion --filename %<Cr>:q<Cr>

