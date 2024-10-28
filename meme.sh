#! /bin/bash

PS1='$(
    echo "`hostname`: $(tput sgr0)\n  "
    `whoami | lolcat -f -p 0.5`
)\$ '

"$(hostname): $(tput sgr0)\n"
$(whoami | lolcat -f -p 0.5)

# CORRECT OLD VERSION
PS1='$(echo "`hostname`:\w $(tput sgr0)\n "$(echo "`whoami`" | lolcat -f -p 0.5))\$ '

PS1='\[$(echo "\]\h \t \w \n  \u\[" | lolcat -f -p 0.5)$(tput sgr0)\] > '

PS1='\h \t \w \n  \u\[$(tput sgr0)\] > '
