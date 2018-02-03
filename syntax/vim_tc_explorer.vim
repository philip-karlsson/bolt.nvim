if exists("b:current_syntax")
  finish
endif

syntax match _comment "\".*$"
syntax match path "$>.*$"
syntax match folder "TC Explorer (alpha)"
syntax match folder "+.*/"

syntax match commands "<Ret>"
syntax match commands "<C-q>"
syntax match commands "<C-s>"
syntax match commands "<C-f>"
syntax match commands "<F2>"
syntax match commands "<F5>"
syntax match commands "<F6>"
syntax match commands "<F7>"
syntax match commands "<F8>"
syntax match commands "<C-p>"

" Match file types | FIXME: Add more
syntax match editable ".*\.py$"
syntax match editable ".*\.txt$"
syntax match editable ".*\.xml$"
syntax match editable ".*\.c$"
syntax match editable ".*\.cpp$"
syntax match editable ".*\.h$"
syntax match editable ".*\.hpp$"
syntax match editable ".*\.xsl$"
syntax match editable ".*\.mk$"
syntax match editable "Makefile"

syntax match commands "-->.*"
highlight link commands Statement
highlight link folder Keyword
highlight link marker Number
highlight link path Debug
highlight link editable Debug
highlight link _comment comment

let b:current_syntax = "vim_tc_explorer"
