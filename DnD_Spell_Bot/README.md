## D&D Spell Lookup ##

DnD Spell Bot will link to spells when called with `!DnD_Spell_Bot` (case insensitive).  It will search the parent comment for spells, then post a reply to the comment that invoked the bot. Unfortunately, spells that are also common words (like
[Slow](http://forgottenrealms.wikia.com/wiki/Slow)
) will have a link provided, even when the poster is clearly not referring to the spell.  The spell search is case sensitive (spells must be capitalized to register a match) which helps a bit, but there are still a lot of false positives.  

DnD Spell Bot currently uses the
[Official D&D Beyond website](https://www.dndbeyond.com/spells)
as its link target.

Dnd Spell Bot is set up to run periodically via cron.  At the interval specified, it will scrape for new invocations, put any it finds on in the queue, then attempt to post the next message out of the queue.

I am considering adding Feats and other more class specific keywords to the search compendium.  If this bot takes off, I'll continue supporting it, but for now it was just a fun little weekend project.

### Possible Expansion ###
- Purge the pickle files every so often so they don't grow forever - probably a job for the cron_manager
    - Need to ensure clearing the pickle files doesn't result in the bot replying to comments it has already serviced.
- Add support for Feats
- Add support for other class specific keywords
- May want to change 'serviced_comments' to 'seen_comments'.
    - Currently, the bot can catch edits, which it wouldn't be able to do with a 'seen' list.  Not sure if pouring over comments that we have already parsed is worth catching an edit though.
- Include the text of the spell along with the link
