# for loading and sorting data regarding accounts of interest 
import csv
import numpy as np
import pandas as pd
# for taking action on accounts of interest
from time import sleep
from selenium import webdriver 

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
    
# GeckoDriver options setup
options = webdriver.FirefoxOptions()  
# block popups (set push notifications to False)
options.set_preference('dom.push.enabled', False) 
# 


