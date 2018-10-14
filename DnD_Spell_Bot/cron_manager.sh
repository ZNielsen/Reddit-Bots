#!/bin/bash

#scriptdir=/home/pi1/Documents/reddit-bots/DnD_Spell_Bot
scriptdir=/home/z/Documents/reddit-bots/DnD_Spell_Bot
scriptname="python3"

debug_file=$scriptdir/debug.out


# Check if a process by this name is running.  If not, go ahead and run the python script
if [ "$(ps -a | grep -c $scriptname)" -lt "1" ]; then
	echo Running! >> $debug_file
	# cd for ini file
	cd $scriptdir
	python3 $scriptdir/spell_lookup.py &>> $debug_file
fi

echo Bash Done! >> $debug_file

exit
