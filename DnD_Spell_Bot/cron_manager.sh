#!/bin/bash

#scriptdir=/home/pi1/Documents/reddit-bots/DnD_Spell_Bot
scriptdir=/home/z/Documents/reddit-bots/DnD_Spell_Bot
scriptname="cron_manager.sh"

debug_file=$scriptdir/debug.out


# Check if a process by this name is running.  If not, go ahead and run the python script
# Not sure why this says 2 processes are running.. is it the ps itself that gets counted?
if [ "$(ps -A | grep -c $scriptname)" -le "2" ]; then
	echo Running, pid=$$ >> $debug_file
	# cd for ini file
	cd $scriptdir
	python3 $scriptdir/spell_lookup.py &>> $debug_file
else
	echo Script already running: $(ps -A | grep -c $scriptname) >> $debug_file
fi

echo Bash Done. >> $debug_file

exit
