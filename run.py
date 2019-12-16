from bot import InstagramBot
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
    ig = InstagramBot(username=user)
    # make record & return file path 
    record = ig.record_followers_and_following(user=user, pwrd=pwrd, account=user)
    # check that record (file path) & return list of non-followbackers
    check = ig.check_non_followbackers(ref=record)
    # unfollow given accounts from that list
    run = ig.unfollow(pwrd=pwrd, accounts_to_unfollow=check)
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
    ig.shutdown()
    # give us the final status 
    return ig.final_output


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
        # gather posts (apply inputs to corresponding method params)
        to_like = ig.gather_posts(hashtag=tag, scroll_range=scroll_range, limit=limit)
        # like posts 
        ig.like_posts(hashtag=tag, hrefs=to_like, indicator_thresh=indicator_thresh)
    # close up shop
    ig.shutdown()
    # give us the final status 
    return ig.final_output


# make this a runable script 
if __name__ == "__main__":
    # tbd
    print('nothing here just yet.. ideas?')
