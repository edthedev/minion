#!/bin/bash
# To add all of the Ed The Dev scripts to your path, 
# you can copy the bits below that you want to your profile...
#    ...or...
# Just add the following line in your profile (but remove the '#' from the begining):
# source ~/minion/add_to_your_profile
#    ...or... , if installed as a vim plugin, ...
# source ~/.vim/bundle/minion/add_to_your_profile
# 
# Your profile is typically at ~/.profile or ~/.zshrc or ~/.bashrc or ~/.bash_profile

# Variables for convenience. 
export MINION_INSTALL=$HOME/.vim/bundle/minion

# Include the scripts on your path.
if [ -d "$MINION_INSTALL" ] ; then
	export PATH="$MINION_INSTALL:$PATH"
fi
# Include some handy aliases in your profile.
if [ -f $MINION_INSTALL/profiles/alias.sh ]; then
	source $MINION_INSTALL/profiles/alias.sh
fi
