import time
import random
import pandas as pd
from instapy import InstaPy, relationship_tools, smart_run, unfollow_util
from user import u, p


def record_followers_and_following(account="ttv.princearthur"):
    # set InstaPy session
    session = InstaPy(username=u, password=p, headless_browser=True)

    # start the session
    with smart_run(session):
        # grab followers (list)
        followers = session.grab_followers(username=account, 
                                        amount="full", 
                                        live_match=True, 
                                        store_locally=False)
        # grab following (list)
        following = session.grab_following(username=account, 
                                        amount="full", 
                                        live_match=True, 
                                        store_locally=False)

    # merge for single list of all unique accounts in following/followers
    unique_accounts = list(set(followers + following))

    # make dataframe of all (unique) accounts
    df = pd.DataFrame(columns=['account'], data=unique_accounts)

    # make bool list of followers (1 == True)
    bool_followers = []
    for account in df['account']:
        if account in followers:
            bool_followers.append(1)
        else:
            bool_followers.append(0)
    # make bool list of following (1 == True)
    bool_following = []
    for account in df['account']:
        if account in following:
            bool_following.append(1)
        else:
            bool_following.append(0)

    # add bool columns to dataframe
    df['follower'] = bool_followers
    df['following'] = bool_following

    # record dataframe as csv
    file = 't_data/followers_and_following/'+ time.strftime("%A_").lower() + time.strftime("%Y%m%d_%H%M%S") + '.csv'
    df.to_csv(path_or_buf=file, index=False)
    # output file name
    return file


def check_unfollowable(ref='ask'):
    # check there's a file loaded
    if ref == 'ask':
        # ask for reference file
        ref = input('csv to run: ')
    # load data into frame
    df = pd.read_csv(ref)

    # tag the followers
    followers = df.account.loc[df.follower == 1]
    # tag the following
    following = df.account.loc[df.following == 1]
    # identify accounts our account is following that are followers of our account
    follow_backers = df.account.loc[((df.follower == 1) & (df.following == 1))]
    # identify accounts our account is following that are NOT followers of our account
    non_follow_backers = df.account.loc[((df.follower == 0) & (df.following == 1))]

    # display number of follow backers and number of non follow backers
    print(f'\n{len(followers)} followers\n'
        f'{len(following)} following\n'
        f'{len(follow_backers)} follow backers\n'
        f'{len(non_follow_backers)} non-follow backers\n')

    if len(non_follow_backers) > 0:
        to_unfollow = input('would you like to unfollow any non-follow backers (y/n)? ')
        if to_unfollow == 'y':
            # determine how many accounts to unfollow
            n_unfollow = int(input('how many would you like to unfollow (int <= 24)? '))
            # limit it (low)
            if n_unfollow > 24:
                print(f'\nWARNING: MAX UNFOLLOWS EXCEEDED\nmax n_unfollow = {24}\n'
                      f'resetting n_unfollow from {n_unfollow} to {24}\n\n')
                n_unfollow = 24
            # cut down to accounts to unfollow
            accounts_to_unfollow = list(non_follow_backers[:n_unfollow])
            # start a session
            session = InstaPy(username=u, password=p, headless_browser=True)
            with smart_run(session):
                # unfollow those accounts
                followers = session.unfollow_users(amount = n_unfollow,
                                                custom_list_enabled = True,
                                                custom_list = accounts_to_unfollow,
                                                custom_list_param = "all",
                                                instapy_followed_enabled = False,
                                                instapy_followed_param = "all",
                                                nonFollowers = False,
                                                allFollowing = False,
                                                style = "FIFO",
                                                unfollow_after = None,
                                                delay_followbackers = 0,  # 864000 = 10 days, 0 = don't delay
                                                sleep_delay = 600)


# default run
if __name__=='__main__':
    # login credentials
    from user import u, p

    # get an InstaPy session!
    # set headless_browser=True to run InstaPy in the background
    session = InstaPy(username=u,
                    password=p,
                    use_firefox=True,
                    headless_browser=True)

    # set call of duty hashtags
    cod_tags = ["codnation","callofduty","codblackout","blackout","blackops4","bo4",
                "modernwarfare","codtoplays","callofdutymodernwarfare","bo4clips",
                "callofdutybo4","codclips","blackops4clips","bo4multiplayer","codbo4",
                "callofdutyclips","treyarch","activision"]

    with smart_run(session):
        """ Activity flow """		
        # general settings		
        # session.set_dont_include(["friend1", "friend2", "friend3"])		

        # track number of tags
        n_tags = 0
        # collect tags to like in groups of 3
        bag_tags = []
        # looping to add sleep between tags
        for tag in cod_tags:	
            # update tag bag
            bag_tags.append(tag)
            # update tag count
            n_tags += 1
            # every 3rd tag
            if n_tags == 3:
                # display bag
                print(f'\nthis bag = {bag_tags}\n')
                # execute likes on tags in this bag
                session.like_by_tags(tags=bag_tags, amount=21)
                # add random rest (hedge like only engagement ban)
                rest = random.randint(a=60, b=120)
                time.sleep(rest)
                # reset tag bag & count
                bag_tags = []
                n_tags = 0 

        # Joining Engagement Pods
        session.join_pods()
