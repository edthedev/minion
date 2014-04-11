" ---------------------------------------------------------
"
"	Vim Bindings for the Minion command line file organizer.
"
" ---------------------------------------------------------

if !has('python')
	echo "Error: Minion requires vim compiled with +python"
		finish
	endif

let s:path = expand('<sfile>:p:h')

" Setup for Python library imports.
python << endpython
import sys
import os
import vim
script_path = vim.eval('s:path')
lib_path = os.path.join(script_path, '..')
sys.path.insert(0, lib_path)

import brain_of_minion as brain
endpython

" =================
" Minion Functions
" =================

let s:path = expand('<sfile>:p:h')

" " Open all Inbox files in buffers.
" -----------------------------------

function! MinionOpen(keywords, archives)
python << endpython
do_not_open = ['.jpg', '.jpeg', '.pdf', '.png', '.rtf', '.xls']
args = {
	'keyword_string':vim.eval("a:keywords"),
	'archives':(vim.eval("a:archives")=="true"),
}
match_files = brain.get_keyword_files(**args)
if not match_files:
	vim.command('echom "No matching results."')

# Add almost everything to buffers.
for item in match_files:
	item_lower = item.lower()

	# Do not open non-text files.
	skip = False
	for ext in do_not_open:
		if ext in item_lower:
			skip = True	

	if skip:
		vim.command(
			'echom "Skipping non-text file %(item)s."' % {
				'item': item})
		
		continue

	# Escape spaces in file names.
	item = item.replace(' ', '\ ')

	# Open the item in a new buffer.
	vim.command("badd %(item)s" % {'item':item})

	# Switch to the next buffer, in case we ran from an empty Vim window.
	vim.command("bn")
	# Show the list of open buffers.
	vim.command("buffers")
endpython
endfunction

" Archive the current open file.
" -------------------------------
function! MinionArchive()
	let s:current_file = expand('%')
python << endpython
current_file = vim.eval("s:current_file")

# This call will nicely display message on success, already.
brain.archive(current_file)
endpython
" Delete the buffer, since we moved the file.
bd
" echom "Archived " 
endfunction

" Sort the current file into a folder.
" -------------------------------------
function! MinionMove(folder)
	let s:current_file = expand('%')
python << endpython
args = {
	'folder':vim.eval("a:folder"),
	'filename':vim.eval("s:current_file"),
}
brain.move_to_folder(**args)
endpython
bd
endfunction


" Output a summary of Minion folders.
" -------------------------------------
function! MinionSummary()
	let s:current_file = expand('%')
python << EOF
print brain.folder_summary(limit=20)
EOF
bd
endfunction

function! MinionFavorites()
	let s:current_file = expand('%')
python << EOF
print brain.print_favorites_summary()
EOF
bd
endfunction

function! MinionHelp()
	help minion.txt
endfunction

" Rename the current file.
" -------------------------------------
function! MinionRename(new_name)
	let s:current_file = expand('%')
python << EOF
new_name = vim.eval("a:new_name")
new_name = brain.string_to_file_name(new_name)
args = {
	'filename':vim.eval("s:current_file"),
	'new_name': new_name,
}

# Close current buffer.
# vim.command('bdelete')
# Move the file.
new_filename = brain.rename_file(**args)
# Open it in the new location.
vim.command("badd %(item)s" % {'item':new_filename})
vim.command("echom 'Your buffer may have moved in the list.'")
EOF
bd
endfunction

" Create a new note file in the inbox
" -------------------------------------
function! MinionNote(keywords)
	let s:current_file = expand('%')
python << EOF
# Create the file
new_name = vim.eval("a:keywords")
args = {
	'topic':vim.eval("a:keywords"),
}
(filename, last_line) = brain.create_new_note(**args)

# Open it in the new location.
vim.command("e %(item)s" % {'item':filename})
vim.command("call cursor(%d, 0)" % (last_line + 1))
EOF
endfunction

" ================
" Minion Commands
" ================

command! -nargs=0 MinionArchive call MinionArchive()
command! -nargs=0 MinionFavorites call MinionFavorites()
command! -nargs=0 MinionHelp call MinionHelp()
command! -nargs=0 MinionInbox call MinionInbox('inbox')
command! -nargs=1 MinionMove call MinionMove(<f-args>)
command! -nargs=1 MinionNote call MinionNote(<f-args>)
command! -nargs=1 MinionOpen call MinionOpen(<f-args>, "false")
command! -nargs=1 MinionRename call MinionRename(<f-args>)
command! -nargs=1 MinionSearch call MinionOpen(<f-args>, "true")
command! -nargs=0 MinionSummary call MinionSummary()

" ==========================
" Minion Keyboard Shortcuts
" ==========================

" Map keyboard shortcuts by default.
if !exists('g:minion_map_keys')
	let g:minion_map_keys = 1
endif

if g:minion_map_keys
	" ":nnoremap <leader>d :call <sid>minionDelete()<CR>

	" Create a new item in the Inbox, and open it immediately.
	:nnoremap <leader>mn :MinionNote 

	" Minion help
	:nnoremap <leader>mh :MinionHelp<Cr>

	" Open files from a Minion sub-folder.
	:nnoremap <leader>mo :MinionOpen 
	
	" Open all items in the Minion Inbox
	:nnoremap <Leader>mi :MinionOpen inbox<Cr>

	" Archive the current file and close it.
	:nnoremap <Leader>ma :MinionArchive<Cr>

	" Display a summary of favorite Minion managed folders.
	:nnoremap <Leader>mf :MinionFavorites<Cr>

	" Move the current file to a new folder.
	:nnoremap <Leader>mm :MinionMove 

	" Rename the current file in place.
	:nnoremap <leader>mr :MinionRename

	" Display a summary of Minion managed folders.
	:nnoremap <Leader>ms :MinionSummary<Cr>

	" New Note
	" :nnoremap <Leader>mn :!~/.vim/bundle/Minion/bin/minion --new-note

	" Review this file
	" ":nnoremap <Leader>mr :!~/.vim/bundle/Minion/bin/minion --filename %<Cr>:q<Cr>
endif
