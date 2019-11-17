from bot import InstagramBot
from helpers import record_followers_and_following, check_non_followbackers
from user import user, pwrd


def rec_n_check():
    """
    record followers and following then check for non-followbackers to unfollow
        > if there are accounts to follow a prompt (with details) will ask how many to unfollow 
            >> range: 0-24

    methods used:
        > record_followers_and_following (helpers.py)
        > check_non_followbackers (helpers.py)
    """
    # variable to make record
    record = record_followers_and_following(account=user)
    # variable to check that record
    run = check_non_followbackers(record)
    # record then check followbackers (display output)
    print(run)


def add_hashtags(post, comment):
    """
    add hashtags (as a comment) to a given post

    methods used:
        > login
        > comment
        > close_browser
    """
    # tag bot instance
    ig = InstagramBot(username=user)
    # log in
    ig.login(password=pwrd)
    # comment (display output)
    print(ig.comment(post, comment))
    # close up shop 
    ig.quit_driver()


def like_by_hashtag(hashtags, scroll_range=5, indicator_thresh=5, limit=50):
    """
    identify then like posts from given hashtags

    methods used:
        > login
        > gather_posts
        > like_posts
        > close_browser
    """
    # tag bot instance
    ig = InstagramBot(username=user)
    # log in
    ig.login(password=pwrd)
    # go through hashtags
    for tag in hashtags:
        # gather posts 
        to_like = ig.gather_posts(hashtag=tag, scroll_range=scroll_range, 
                                  limit=limit, certify=True, r_log_on=True)
        # like posts 
        ig.like_posts(hashtag=tag, hrefs=to_like, indicator_thresh=indicator_thresh)
    # close up shop
    ig.quit_driver()


# make this a runable script 
if __name__ == "__main__":
    # tbd
    # print('nothing here just yet.. ideas?')
    from infos import default
    print(like_by_hashtag(hashtags=default, 
                          scroll_range=5, 
                          indicator_thresh=5, 
                          limit=50))
