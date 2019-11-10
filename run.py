from bot import InstagramBot
from helpers import record_followers_and_following, check_non_followbackers
# login info
from _pile import utv, ptv, u, p


def rec_n_check():
    """
    record followers and following then check for non-followbackers to unfollow

    methods used:
        > record_followers_and_following (helpers.py)
        > check_non_followbackers (helpers.py)
    """
    # variable to make record
    record = record_followers_and_following()
    # variable to check that record
    run = check_non_followbackers(record)
    # record then check followbackers (display output)
    print(run)


def comment(post, comment):
    """
    post a comment on a given post

    methods used:
        > login
        > comment
        > close_browser
    """
    # tag bot instance
    ig = InstagramBot(username=u)
    # log in
    ig.login(password=p)
    # comment (display output)
    print(ig.comment(post, comment))
    # close
    ig.close_browser()


def like_by_hashtag(hashtags, scroll_range=5, indicator_thresh=5, limit=False):
    """
    identify then like posts from given hashtags

    methods used:
        > login
        > gather_posts
        > like_posts
        > close_browser
    """
    # tag bot instance
    ig = InstagramBot(username=u)
    # log in
    ig.login(password=p)
    # go through hashtags
    for tag in hashtags:
        # gather posts 
        to_like = ig.gather_posts(hashtag=tag, scroll_range=scroll_range, 
                                  limit=limit, certify=True, r_log_on=True)
        # like posts 
        ig.like_posts(hashtag=tag, hrefs=to_like, indicator_thresh=indicator_thresh)
    # close up shop
    ig.close_browser()


# make this a runable script 
if __name__ == "__main__":
    # tbd
    print('nothing here just yet.. ideas?')
