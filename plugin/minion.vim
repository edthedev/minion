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

function! MinionOpen(keywords)
python << EOF

import sys
import os
import vim
script_path = vim.eval('s:path')
lib_path = os.path.join(script_path, '..')
sys.path.insert(0, lib_path)

import brain_of_minion as brain
args = {
	'keyword_string':vim.eval("a:keywords"),
}
match_files = brain.get_keyword_files(**args)
if not match_files:
	vim.command('echom "No matching results."')
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
function! MinionMove(folder)
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

args = {
	'folder':vim.eval("a:folder"),
	'filename':vim.eval("s:current_file"),
}
brain.move_to_folder(**args)

EOF
bd
endfunction


" Output a summary of Minion folders.
" -------------------------------------
function! MinionSummary()
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

print brain.folder_summary()
EOF
bd
endfunction

function! MinionHelp()
python << EOF
import sys
import os
script_path = vim.eval('s:path')
lib_path = os.path.join(script_path, '..')
sys.path.insert(0, lib_path)

e eval('s:path')/help.txt
EOF
endfunction

" ================
" Minion Commands
" ================

command! -nargs=0 MinionArchive call MinionArchive()
command! -nargs=0 MinionHelp call MinionHelp()
" command! -nargs=0 MinionInbox call MinionInbox('inbox')
command! -nargs=1 MinionMove call MinionMove(<f-args>)
command! -nargs=1 MinionOpen call MinionOpen(<f-args>)
command! -nargs=0 MinionSummary call MinionSummary()

" ==========================
" Minion Keyboard Shortcuts
" ==========================

" Get some help.

"TODO: ":map <Leader>mh :MinionHelp<Cr>

" TODO: Create a global variable to control assignment of default key
" mappings.
" http://getpocket.com/a/read/102013317 - search yourplugin_map_keys
"
" Display a summary of Minion managed folders.
:map <Leader>ms :MinionSummary<Cr>

" Create a new item in the Inbox, and open it immediately.
" TODO:

" Open files from a Minion sub-folder.
:map <leader>mo :MinionOpen 

" Open all items in the Minion Inbox
:map <Leader>mi :MinionOpen inbox<Cr>

" Archive the current file and close it.
:map <Leader>ma :MinionArchive<Cr>

" Move the current file...
:map <Leader>mm :MinionMove 




" Organizer help
" ":map <Leader>mh :!~/.vim/bundle/Minion/bin/minion --help<Cr>$

" New Note
" :map <Leader>mn :!~/.vim/bundle/Minion/bin/minion --new-note

" Review this file
" ":map <Leader>mr :!~/.vim/bundle/Minion/bin/minion --filename %<Cr>:q<Cr>

