" ---------------------------------------------------------
"
"	Vim Bindings for the Minion command line file organizer.
"
" ---------------------------------------------------------

" Archive the current file and close it.
:map <Leader>ma :!~/.vim/bundle/Minion/bin/minion --action=archive --filename=%<Cr>:q<Cr>

" Organizer help
:map <Leader>mh :!~/.vim/bundle/Minion/bin/minion --help<Cr>$

" New Note
:map <Leader>mn :!~/.vim/bundle/Minion/bin/minion --new-note

" Review this file
:map <Leader>mr :!~/.vim/bundle/Minion/bin/minion --filename %<Cr>:q<Cr>


