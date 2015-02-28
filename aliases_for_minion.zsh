#!/bin/bash

# For backwards compatability.
alias minion="minion.py"

# Keystrokes have value.
alias mn="minion.py"

# Let's add content.
alias remind="minion.py remind $@"
alias rem="minion.py remind $@"

# Some templates
alias journal="minion.py template journal $@"
alias week="minion.py template week"
alias weekend="minion.py template weekend"

# Let's review content.
alias goals="minion.py open goals"
alias today="minion.py find urgent today `date +%Y-%m-%d` goal `date +%A`"
alias where_in_the_world_is="minion.py find --archives $@"

# For development under Zshell
# alias testminion="pushd ~/.vim/bundle/minion/tests; ./run_all_tests.sh; popd"
