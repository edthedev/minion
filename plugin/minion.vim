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
	vim.command("badd %(item)s" % {'item':item})
	vim.command("buffers")
EOF
endfunction



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

brain.archive(current_file)
EOF
bd
echom "Archived " 
echom s:current_file

endfunction

" ================
" Minion Commands
" ================

command! -nargs=0 MinionInbox call MinionInbox()
command! -nargs=0 MinionArchive call MinionArchive()

" ==========================
" Minion Keyboard Shortcuts
" ==========================

" Archive the current file and close it.
:map <Leader>ma :!~/.vim/bundle/Minion/bin/minion --action=archive --filename=%<Cr>:q<Cr>

" Organizer help
:map <Leader>mh :!~/.vim/bundle/Minion/bin/minion --help<Cr>$

" New Note
:map <Leader>mn :!~/.vim/bundle/Minion/bin/minion --new-note

" Review this file
:map <Leader>mr :!~/.vim/bundle/Minion/bin/minion --filename %<Cr>:q<Cr>

