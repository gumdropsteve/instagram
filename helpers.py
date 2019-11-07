import time
import random
import pandas as pd
# selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
# instapy
from instapy import InstaPy, relationship_tools, smart_run, unfollow_util
from _pile import u, p

'''
to add
detect if page is 404
    by text? 
recording info on the visuals
    what is the account broadcasting?
        rip sullivan --classic
    this may be better in bot?
        no? what is point of helpers?
            maybe.
'''


def check_xpath(webdriver, xpath, click=False, send_keys=False, keys=None, hedge_load=1):
    """checks if an xpath exists on the current page

    inputs)
        > webdriver
            >> driver being used
        > xpath
            >> xpath in question
        > click
            >> if clicking the element once/if found
        > send_keys
            >> if sending keys to element once/if found
        > keys
            >> keys being sent if sending keys (i.e. send_keys=True)

    output)
        > if successful
            >> 0
        > if unsuccessful
            >> 1
    """
    # hedge laod time
    time.sleep(hedge_load)
    # test this 
    try:
        # find xpath in question
        find_element = webdriver.find_element_by_xpath(xpath)
        # are we clicking
        if click == True:
            # yes, so click
            find_element.click()
            # hedge time
            time.sleep(3)
        # are we sending keys
        if send_keys == True:
            # yes, so send them
            find_element.send_keys(keys)
            # hedge time
            time.sleep(3)
        # element exists and was successfull
        return 0
    # if it didn't work
    except NoSuchElementException:
        # indicate as such
        return 1


def record_followers_and_following(account="ttv.princearthur", **output_df):
    """
    > pull up a given account and record it's followers and following to csv
        >> then return that file path 
        >> optional output_df param
            > print file name & return the pandas dataframe
    """
    # set InstaPy session
    session = InstaPy(username=u, password=p, headless_browser=True)

    # start the session
    with smart_run(session):
        # grab followers (list)
        followers = session.grab_followers(username=account, amount="full", 
                                           live_match=True, store_locally=False)
        # grab following (list)
        following = session.grab_following(username=account, amount="full", 
                                           live_match=True, store_locally=False)

    # merge for single list of all unique accounts in following/followers
    unique_accounts = list(set(followers + following))

    # make dataframe of all (unique) accounts
    df = pd.DataFrame(data=unique_accounts, columns=['account'])

    # make bool list of followers (1 == True)
    bool_followers = []
    for account in df['account']:
        # is follower
        if account in followers:
            bool_followers.append(1)
        # not follower
        else:
            bool_followers.append(0)
    
    # make bool list of following (1 == True)
    bool_following = []
    for account in df['account']:
        # are following
        if account in following:
            bool_following.append(1)
        # not following
        else:
            bool_following.append(0)

    # add bool columns to dataframe
    df['follower'] = bool_followers
    df['following'] = bool_following

    # id day of week 
    dow = time.strftime("%A_").lower()
    # numerical year, month, day _ hour, minute, second
    ymdhms = time.strftime("%Y%m%d_%H%M%S")
    # generate file name
    file = 'data/made/followers_and_following/' + dow + ymdhms + '.csv'
    
    # record dataframe as csv
    df.to_csv(path_or_buf=file, index=False)
    
    # did we request the dataframe?
    if output_df:
        # display file name
        print(f'{file}')
        # output dataframe for further use
        return df

    # output file name
    return file


def check_non_followbackers(ref='ask'):
    """
    > compare followers and following from given csv 
        >> to identify non-followbackers
    > print out findings
    > ask if the user would like to unfollow any found non-followbackers
        >> limit 24 per session (rec max 99 / day)
    """
    # check there's a file loaded
    if ref == 'ask':
        # ask for reference file
        ref = input('csv to run: ')
    
    # load data into frame
    df = pd.read_csv(ref)

    # tag followers & following 
    followers = df.account.loc[df.follower == 1]
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

    # are there accounts worthy of unfollowing? 
    if len(non_follow_backers) > 0:
        # ask user opinion
        to_unfollow = input('would you like to unfollow any non-follow backers (y/n)? ')
        
        # proceed with unfollowing
        if to_unfollow == 'y':
            # determine how many accounts to unfollow
            n_unfollow = int(input('how many would you like to unfollow (int <= 24)? '))
            
            # set a cap (limit number of unfollows per session)
            cap = 24
            # is desired number of unfollow more than max amount allowed per session (cap)?
            if n_unfollow > cap:
                # output warning, action and times to read 
                print(f'\nWARNING: MAX UNFOLLOWS EXCEEDED\nmax n_unfollow = {cap}\n')
                time.sleep(1)
                print(f'resetting n_unfollow from {n_unfollow} to {cap}\n\n')
                time.sleep(1)
                # enforce cap
                n_unfollow = cap
            
            # cut down to accounts to unfollow
            accounts_to_unfollow = list(non_follow_backers[:n_unfollow])
            
            # make a session 
            session = InstaPy(username=u, password=p, headless_browser=True)
            
            # start the session 
            with smart_run(session):
                # unfollow those accounts
                followers = session.unfollow_users(amount=n_unfollow, custom_list_enabled=True,
                                                   custom_list=accounts_to_unfollow, custom_list_param="all",
                                                   instapy_followed_enabled=False, instapy_followed_param="all",
                                                   nonFollowers=False, allFollowing=False,
                                                   style="FIFO", unfollow_after=None,
                                                   sleep_delay=600, delay_followbackers=0) # 864000 = 10 days, 0 = don't delay
            
            # indicate completion
            print(f'session complete\n {len(non_follow_backers)-n_unfollow} non-followbackers remain')
            # output accounts we unfollowed
            return accounts_to_unfollow

        # not unfollowing anyone
        else:
            print('ok, cool.')
            # output non-followbackers
            return non_follow_backers

    # nobody to unfollow
    else:
        # indicate so 
        print(f'len(non_follow_backers) == {len(non_follow_backers)}')
