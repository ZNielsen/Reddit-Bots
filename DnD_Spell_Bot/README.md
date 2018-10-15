## DnD Spell Lookup ##

DnD Spell Bot will link to spells when called with `!DnD_Spell_Bot` (case insensitive).  It will search the parent comment for spells, then post a reply to the comment that invoked the bot. Unfortunately, spells that are also common words (like
[Slow](http://forgottenrealms.wikia.com/wiki/Slow)
) will have a link provided, even when the poster is clearly not referring to the spell.  The spell search is case sensitive (spells must be capitalized to register a match) which helps a bit, but there are still a lot of false positives.  

DnD Spell Bot currently uses the
[D&D 5th Edition Wikia](http://dnd5e.wikia.com/wiki/D%26D_5th_Edition_Wikia)
as its link target.

I am considering adding Feats and other more class specific keywords to the search compendium.  If this bot takes off, I'll continue supporting it, but for now it was just a fun little weekend project.
