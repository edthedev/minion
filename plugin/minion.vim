" ---------------------------------------------------------
"
"	Vim Bindings for the Minion command line file organizer.
"
" ---------------------------------------------------------

" Archive the current file and close it.
:map <Leader>ma :!minion --action=archive --filename=%<Cr>:q<Cr>

" Organizer help
:map <Leader>mh :!minion --help<Cr>$

" New Note
:map <Leader>mn :!minion --new-note

" Review this file
:map <Leader>mr :!minion --filename %<Cr>:q<Cr>


