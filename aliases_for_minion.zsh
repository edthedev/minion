#!/bin/zsh

# For backwards compatability.
alias minion="python ~/.antigen/repos/https-COLON--SLASH--SLASH-github.com-SLASH-edthedev-SLASH-minion.git/bin/minion.py"

# Create default config if missing.
if [ ! -f ~/.minion ]; then
	minion make_config
fi

# Keystrokes have value.
alias mn="minion"

# Let's add content.
alias remind="minion remind $@"
alias rem="minion remind $@"

# Some templates
alias journal="minion template journal $@"
alias week="minion template week"
alias weekend="minion template weekend"

# Let's review content.
alias goals="minion open goals"
alias today="minion find urgent today `date +%Y-%m-%d` goal `date +%A`"
alias where_in_the_world_is="minion find --archives $@"

# For development under Zshell
# alias testminion="pushd ~/.vim/bundle/minion/tests; ./run_all_tests.sh; popd"
