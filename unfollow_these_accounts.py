# for loading and sorting data regarding accounts of interest 
import numpy as np
import pandas as pd
# for taking action on accounts of interest
from time import sleep
from selenium import webdriver 
# for documentation
import csv
import datetime

# load accounts & info on followed
follows_users = pd.read_csv('data/follows_users_ttv_princearthur_20190421_2205.csv')
# load accounts & info on following
by_users = pd.read_csv('data/followed_by_users_ttv_princearthru_20190421_1846.csv')

# url of each account following us
by_usernames = np.array(by_users.user_profile)
# url of each account we follow
follows_usernames = np.array(follows_users.user_profile)

# collect urls of profiles to unfollow 
unfollow_these = [user for user in follows_usernames if user not in by_usernames]
# collect urls of profiles we do NOT want to unfollow (double check overlap)
keep_these = [user for user in follows_usernames if user in by_usernames]

# set count for safety check (make sure we don't unfollow anyone we don't want to)
safe_check = 0
# check overlap
for user in keep_these:
    # does user coexist?
    if user in unfollow_these:
        # display it
        raise Exception(f'if user in unfollow_these : {user}')
    # otherwise
    else:
        # add to count of non coexisting
        safe_check += 1
# double check overlap via count
if safe_check != len(keep_these):
    # display unequal counts
    raise Exception(f'safe_check != len(keep_these) : {safe_check} != {len(keep_these)}')
    
# create csv to store accounts we have unfollowed (so do not re-follow in future)
with open('accounts_ttvpa_used_to_follow.csv', 'w', newline='') as file:
    # set writer to this file
    the_writer = csv.writer(file)
    # write column names
    the_writer.writerow(['account_id','username','profile_url','time_unfollowed'])
    
# geckodriver options setup
options = webdriver.FirefoxOptions()  
# block popups (set push notifications to False)
options.set_preference('dom.push.enabled', False) 

# id css selector for 'following' button
following_button = '.vBF20'
# id css selector for 'unfollow' button
unfollow_button = 'button.aOOlW:nth-child(1)'

# set webdriver w/ options
driver = webdriver.Firefox(options=options) 

# go through first 100 urls
for user_url in unfollow_these[:100]:
    """
    prime the mission
    """
    # load the url
    driver.get(user_url)
    # wait for profile page to load
    sleep(3)
    # find and click the 'following' button 
    driver.find_element_by_css_selector(following_button).click()
    # wait a bit (to seem human, for web loading, and not unfollow too quickly)
    sleep(2)
    """
    set up recording of transaction
    """
    # pull the account's record
    this_account = follows_usernames.loc[follows_users.user_profile == user_url]
    # account's id number
    account_id = this_account.id
    # account's username
    username = this_account.username
    # account's url
    profile_url = this_account.user_profile
    # double check
    if profile_url != user_url:
        # let us know if it's not adding up 
        raise Exception(f'profile_url != user_url : {profile_url} != {user_url}')
    # set values to be recorded 
    fields = [account_id, username, profile_url, datetime.datetime.now()]
    """
    execute
    """
    # find and click 'unfollow' button in popup 
    driver.find_element_by_css_selector(unfollow_button).click()
    """
    record the transaction
    """
    # open up the csv
    with open('accounts_ttvpa_used_to_follow.csv', 'a') as _f:
        # fit the writer
        writer = csv.writer(_f)
        # document the transaction
        writer.writerow(fields)
    


