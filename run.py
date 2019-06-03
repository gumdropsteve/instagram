# general
import random
from time import sleep
# bot
from bot import InstagramBot
# hashtags
from infos import pleasanton_tags

# determine mode
mode='redo unfollow'  # 'verify unfollowing' 'unfollow' 'like' 'analyze unfollow'

# determine start point in data
genesis = 0
# determine end point in data
exodus = 500

# make this a runable script 
if __name__ == "__main__":
    """
       ***adjust lines 13-21 to fit your style***
    """
    # login info 
    from _pile import utv, ptv
    # your username 
    u = utv 
    # your password
    p = ptv  

    # label the bot
    ig = InstagramBot(username=u, password=p)
    
    if mode == 'analyze unfollow':
        # import data
        from infos import by_users, follows_users
        # analyze current selection of unfollowability
        au = ig.analyze_following(followers=by_users[genesis:exodus], 
                                  following=follows_users[genesis:exodus],
                                  to_unfollow=True, previous=True)
        # display number of subject accounts in selection 
        print(len(au))
        # quit driver
        ig.close_browser()

    elif mode == 'like':
        # get the party started 
        ig.login()
        # insert your desired hashtags here (list)
        hashtags = pleasanton_tags

        while True:
            # this should work until all tags have been used
            try:
                # choose a random tag from the list of tags
                tag = random.choice(hashtags)
                # like the posts under that tag
                ig.like_photos(tag)
            # if it doesn't, or (hopefully) we're done
            except Exception:
                # close her down
                ig.close_browser()
                # take a break 
                sleep(600)
                # retry the bot 
                ig = InstagramBot(username=u, password=p)

    elif mode == 'unfollow':
        # get the party started 
        ig.login()
        # unfollow these people
        ig.unfollow(start=genesis,end=exodus)
        # close her down
        ig.close_browser()

    elif mode == 'verify unfollowing':
        # kickoff (this can be more efficient; fix when making analysis class)
        ig.login()
        # verify some unfollowings 
        ig.verify_unfollow(start=genesis, end=exodus)
        # wrap it up (run.py needs to be rewritten)
        ig.close_browser()

    elif mode == 'redo unfollow':
        # kickoff (this can be more efficient; fix when making analysis class)
        ig.login()
        # verify some unfollowings 
        ig.redo_unfollow(start=genesis, end=exodus)
        # wrap it up (run.py needs to be rewritten)
        ig.close_browser()

    else:
        print(f'mode == {mode}')
