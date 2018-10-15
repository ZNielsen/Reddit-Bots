
import os
import atexit
import praw
import re
import time
import getpass
from collections import deque
import _spells

try:
    import cPickle as pickle
except:
    import pickle


username = getpass.getuser()
if username == 'z':
    # Mint
    path = "/home/z/Documents/reddit-bots/DnD_Spell_Bot"
elif username == 'pi1':
    # Pi
    path = "/home/pi1/Documents/reddit-bots/DnD_Spell_Bot"
elif username == 'cpzniels':
    # Windows
    pass

p_pkl_name = "/p_seen.pkl"
c_pkl_name = "/c_seen.pkl"
q_pkl_name = "/deque.pkl"
t_name     = "/time"
p_pkl_file = path + p_pkl_name
c_pkl_file = path + c_pkl_name
q_pkl_file = path + q_pkl_name
t_file     = path + t_name

seen_posts = set()
serviced_comments = set()
post_deque = deque()
tt_post = 1

class reply_object:
    to_id = 0
    text  = 0
reply_obj = reply_object()

# Load the persistent info
if os.path.isfile(p_pkl_file):
    with open(p_pkl_file, 'rb') as fp:
        seen_posts = pickle.load(fp)
if os.path.isfile(c_pkl_file):
    with open(c_pkl_file, 'rb') as fp:
        serviced_comments = pickle.load(fp)
if os.path.isfile(q_pkl_file):
    with open(q_pkl_file, 'rb') as fp:
        post_deque = pickle.load(fp)
if os.path.isfile(t_file):
    with open(t_file, 'r') as fp:
        tt_post = fp.readline()

# Write out seen comments
@atexit.register
def write_persistent_data():
    with open(p_pkl_file, 'wb') as fp:
        pickle.dump(seen_posts, fp)
    with open(c_pkl_file, 'wb') as fp:
        pickle.dump(serviced_comments, fp)
    with open(q_pkl_file, 'wb') as fp:
        pickle.dump(post_deque, fp)
    with open(t_file, 'w') as fp:
        fp.write(str(tt_post))


reddit = praw.Reddit('spellbot-script')
subreddit = reddit.subreddit('DnD')
test_subreddit = reddit.subreddit('pythonforengineers')

comment_pre = "Here are some links for you:\n\n"
comment_post = "^(I am a bot, still in very early testing.)"


def are_spells_in_comments(text):
    ret_val = []
    for spell in _spells.spell_list:
        # Word boundries -> Don't match the start of a word
        # ex. Halloween linking to the spell Hallow
        if re.search(r'\b'+ spell +r'\b', text):
            ret_val.append(spell)
    return ret_val

def make_bot_comment(list):
    comment_links = ''
    for spell in reply_list:
        comment_links = comment_links + "["+ spell +"]("+ _spells.spell_url + spell +")\n\n"
    comment = comment_pre + comment_links + comment_post
    return comment


def post_test_reply(post, bot_comment):
    # Print for debug
    print("About to reply to post " + post.id  + ": "+ post.title + "\n" + post.selftext)
    print("Comment: " + bot_comment)
    print("----------------------------------------------------------")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("----------------------------------------------------------")
    for test_post in test_subreddit.new(limit=1):
        x = post.title +"\n\n"+ post.selftext +"\n\n"
        x = x+ "----------------------------------------------------------\n\n"
        x = x+ "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n"
        x = x+ "----------------------------------------------------------\n\n"
        x = x+ bot_comment
        #test_post.reply(x)

def can_post_in():
    global tt_post
    return int(round(float(tt_post)))-int(round(time.time()))


def post_from_queue():
    global tt_post
    try:
        obj = post_deque.pop()
        if can_post_in() < 0:
            comment = reddit.comment(id=obj.to_id)
            # Post reply to calling comment
            print("Posting a reply comment: "+ obj.text)
            comment.reply(obj.text)
            comment.upvote()
            serviced_comments.add(obj.to_id)
            tt_post = (time.time() + 600)
        else:
            print("Too early to post.  Can post again in "+ str(can_post_in()) +" seconds.")
    except Exception as e:
        if e.__class__.__name__ == "IndexError":
            print("Deque is empty")
        elif re.match("RATELIMIT", str(e)):
            print("Reddit is saying you are posting too fast - did you manually post?")
            # Update the timer
            num = [int(s) for s in str(e.message).split() if s.isdigit()]
            tt_post = time.time() + (60* int(num[0]))
        else:
            print("[EXCEPTION]")
            print(str(e))




################################################################################
#print("[DEBUG] seen posts: "+ str(seen_posts))
#print("[DEBUG] total of "+ str(len(seen_posts)) +" posts.")
#print("[DEBUG] serviced comments: "+ str(serviced_comments))
#print("[DEBUG] total of "+ str(len(serviced_comments)) +" serviced comments.")
#print("[DEBUG] time to next post: "+ str(can_post_in()) +" seconds.")


# Comments - only post on request
call_token = "!DnD_spell_bot"
comment_counter = 0
post_counter    = 0
for post in subreddit.hot():
    post_counter += 1
    # Look for an explicit call in comments
    post.comments.replace_more()
    for comment in post.comments.list():
        comment_counter += 1
        # Make sure we havn't serviced this comment yet
        if comment.id not in serviced_comments:
            if re.search(call_token, comment.body, re.IGNORECASE):
                # Parse parent comment for spells
                parent_comment = comment.parent()
                reply_list = are_spells_in_comments(parent_comment.body)
                if len(reply_list) > 0:
                    bot_comment = make_bot_comment(reply_list)
                else:
                    bot_comment = "Hmm.. I don't see any spells.  Sorry about that.\n\n"+ comment_post
                # Place reply into queue
                reply_obj.to_id = comment.id
                reply_obj.text  = bot_comment
                post_deque.appendleft(reply_obj)
post_from_queue()
write_persistent_data()
print("Just parsed "+ str(comment_counter) +" comments and "+ str(post_counter) +" posts.")
print("Python Done!")
