
import os
import atexit
import praw
import re
import time
from spells import spell_list

try:
    import cPickle as pickle
except:
    import pickle

pkl_file = "seen.pkl"
seen_posts = set()

# Load the seen posts
# if os.path.isfile(pkl_file):
#     with open(pkl_file, 'rb') as fp:
#         seen_posts = pickle.load(fp)
# Write out seen comments
@atexit.register
def write_seen_posts():
    with open(pkl_file, 'wb') as fp:
        pickle.dump(seen_posts, fp)


reddit = praw.Reddit('spellbot-script')
subreddit = reddit.subreddit('DnD')
test_subreddit = reddit.subreddit('pythonforengineers')


comment_pre = "I noticed some spells in your post!\n\n"
comment_post = "^(I am a bot, still in very early testing)"
url_prefix = "http://forgottenrealms.wikia.com/wiki/"



for post in subreddit.new(limit=10):
    # Don't operate on the same post twice
    if post.id not in seen_posts:
        # Add to the list of posts to ignore
        seen_posts.add(post.id)

        reply_list = []
        comment_links = ''

        # Scan for spell names
        # TODO - better way to do this?
        for spell in spell_list:
            if re.search(spell, post.selftext, re.IGNORECASE):
                # Got a hit, add to the list of things to link to
                reply_list.append(spell)

        if len(reply_list) > 0:
            for spell in reply_list:
                comment_links = comment_links + "["+ spell +"]("+ url_prefix + spell +")\n\n"
            comment = comment_pre + comment_links + comment_post

            print("About to reply to post " + post.id  + ": "+ post.title + "\n" + post.selftext)
            print("Comment: " + comment)
            print("----------------------------------------------------------")
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("----------------------------------------------------------")

            for test_post in test_subreddit.new(limit=1):
                test_post.reply(post.selftext +"\n\n\n"+ comment)
                time.sleep(5)


write_seen_posts()
