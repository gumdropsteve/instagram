# general
import random
from time import sleep
# bot
from bot import InstagramBot
# hashtags
from infos import plsntn_re_tags

# determine mode
mode='unfollow'  # 'like'

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
    # get the party started 
    ig.login()

    if mode == 'like':
        # insert your desired hashtags here (list)
        hashtags = plsntn_re_tags

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
                ig.closeBrowser()
                # take a break 
                sleep(600)
                # retry the bot 
                ig = InstagramBot(username=u, password=p)

    elif mode == 'unfollow':
        ig.unfollow(start=1750,end=2000)
