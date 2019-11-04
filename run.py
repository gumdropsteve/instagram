# general
import random
from time import sleep
from datetime import datetime
# bot
from bot import InstagramBot
# hashtags
from infos import pleasanton_tags, s2_eligible_for_unfollowing, second_round_all, draft_log

def rec_n_check():
    from helpers import record_followers_and_following, check_non_followbackers
    """
    record followers and following then check for non-followbackers to unfollow
    """
    # variable to make record
    record = record_followers_and_following()
    # variable to check that record
    run = check_non_followbackers(record)
    # record then check followbackers (display output)
    print(run)


def comment(post, comment):
    # tag bot instance
    ig = InstagramBot(username=u)
    # log in
    ig.login(password=p)
    # comment (display output)
    print(ig.comment(post, comment))
    # close
    ig.close_browser()


"""
BELOW NEEDS TO BE REFORMATTED LIKE ABOVE
NEW STRAT IS QUASI-API OF SPECIFIC USES
"""

# determine mode
mode= 'like'  #'unfollow' #'re_verify unfollowing' 'redo unfollow' 'verify unfollowing' 'unfollow' 'like' 'analyze unfollow'

# determine start point in data
genesis = 0
# determine end point in data
exodus = 100
# make this a runable script 
if __name__ == "__main__":
    # login info
    from _pile import utv
    # your username 
    u = utv 
    # your password
    p = ptv  

    # label the bot
    ig = InstagramBot(username=u)

    # in testing mode
    if mode == 'like':
        # log in
        ig.login(password=p)
        # set hashtags
        hashtags = ['codnation', 'callofdutymodernwarfare', 'modernwarfare', 'callofduty', 'blackops4']
        for hashtag in hashtags:
            # gather posts
            to_like = ig.gather_posts(hashtag=hashtag)
            # like posts 
            ig.like_posts(hashtag=hashtag, hrefs=to_like)
        # close up shop
        ig.close_browser()

    # in testing mode
    if mode == 'unfollow':
        # log in
        ig.login(password=p)
        # tag database 
        db = second_round_all
        # pull unfollowed urls
        inelgible = [url for url in draft_log.user_profile]
        # adjust elgible
        elgible = [url for url in s2_eligible_for_unfollowing if url not in inelgible][genesis:exodus]
        # set record log
        log = []
        # start interations
        for i in range(len(elgible)):
            # tag url
            url = elgible[i]
            # pull account id and username 
            account = [_ for __ in db.loc[db.user_profile == url].values for _ in __][:2]
            # tack on url
            account.append(url)
            # tag unfollowing of account
            unfollow = ig.unfollow(url)
            # add unfollow info to account info
            for p in unfollow:
                account.append(p)
            # record transaction
            ig.record(record=account, log='data/made/unfollow_log.csv')
            # every 25 accounts
            if i % 25 == 0 and i != 0:
                # update user as to progress
                print(f"{int((i/len(elgible))*100)}% complete ; {datetime.now()}")
                # take an extended break
                sleep(75)
            #otherwise
            else:
                # take regular break
                sleep(15)
        # close up shop
        ig.close_browser()

    # if mode == 'analyze unfollow':
    #     # import data
    #     from infos import by_users, follows_users
    #     # analyze current selection of unfollowability
    #     au = ig.analyze_following(followers=by_users[genesis:exodus], 
    #                               following=follows_users[genesis:exodus],
    #                               to_unfollow=True, previous=True)
    #     # display number of subject accounts in selection 
    #     print(len(au))
    #     # quit driver
    #     ig.close_browser()

    # elif mode == 'like':
    #     # get the party started 
    #     ig.login()
    #     # insert your desired hashtags here (list)
    #     hashtags = pleasanton_tags

    #     while True:
    #         # this should work until all tags have been used
    #         try:
    #             # choose a random tag from the list of tags
    #             tag = random.choice(hashtags)
    #             # like the posts under that tag
    #             ig.like_photos(tag)
    #         # if it doesn't, or (hopefully) we're done
    #         except Exception:
    #             # close her down
    #             ig.close_browser()
    #             # take a break 
    #             sleep(600)
    #             # retry the bot 
    #             ig = InstagramBot(username=u, password=p)

    # elif mode == 'unfollow':
    #     # get the party started 
    #     ig.login()
    #     # unfollow these people
    #     ig.unfollow(start=genesis,end=exodus)
    #     # close her down
    #     ig.close_browser()

    # elif mode == 'verify unfollowing':
    #     # kickoff (this can be more efficient; fix when making analysis class)
    #     ig.login()
    #     # verify some unfollowings 
    #     ig.verify_unfollow(start=genesis, end=exodus)
    #     # wrap it up (run.py needs to be rewritten)
    #     ig.close_browser()

    # elif mode == 'redo unfollow':
    #     # kickoff (this can be more efficient; fix when making analysis class)
    #     ig.login()
    #     # verify some unfollowings 
    #     ig.redo_unfollow(start=genesis, end=exodus, verification=True, record_thresh=5, speed=0.5)
    #     # wrap it up (run.py needs to be rewritten)
    #     ig.close_browser()

    # elif mode == 're_verify unfollowing':
    #     # kickoff (this can be more efficient; fix when making analysis class)
    #     ig.login()
    #     # verify some unfollowings 
    #     ig.re_verify_unfollow(start=genesis, end=exodus)
    #     # wrap it up (run.py needs to be rewritten)
    #     ig.close_browser()

    else:
        print(f'mode == {mode}')
