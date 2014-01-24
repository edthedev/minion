" ---------------------------------------------------------
"
"	Vim Bindings for the Minion command line file organizer.
"
" ---------------------------------------------------------


if !has('python')
	echo "Error: Minion requires vim compiled with +python"
		finish
	endif

" Archive the current file and close it.
:map <Leader>ma :!~/.vim/bundle/Minion/bin/minion --action=archive --filename=%<Cr>:q<Cr>

" Organizer help
:map <Leader>mh :!~/.vim/bundle/Minion/bin/minion --help<Cr>$

" New Note
:map <Leader>mn :!~/.vim/bundle/Minion/bin/minion --new-note

" Review this file
:map <Leader>mr :!~/.vim/bundle/Minion/bin/minion --filename %<Cr>:q<Cr>

let s:path = expand('<sfile>:p:h')

function! MinionInbox() 
python << EOF
print "Hello World!"
import sys
import os
# sys.path.insert(0, os.path.realpath(os.path.join(__file__, '..')))
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

command! -nargs=0 MinionInbox call MinionInbox()
