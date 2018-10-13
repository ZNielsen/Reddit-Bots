#!/bin/bash

scriptdir=/home/pi1/Documents/reddit-bots/DnD_Spell_Bot
scriptname="cron_manager.sh"

# Check if a process by this name is running.  If not, go ahead and run the python script
if [ "$(ps | grep -c $scriptname)" -le "2" ]; then
	echo Running!
	python3 $scriptdir/spell_lookup.py 2>1 1>$scriptdir/debug.txt
fi

touch $scriptdir/CRON_RAN

exit

