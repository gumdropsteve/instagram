import time
import pandas as pd
from instapy import InstaPy, relationship_tools, smart_run, unfollow_util
from user import u, p

# set InstaPy session
session = InstaPy(username=u, password=p, headless_browser=True)

# start the session
with smart_run(session):
    # grab followers (list)
    followers = session.grab_followers(username="ttv.princearthur", 
                                       amount="full", 
                                       live_match=True, 
                                       store_locally=False)
    # grab following (list)
    following = session.grab_following(username="ttv.princearthur", 
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
file = 't_data/followers_and_following' + time.strftime("%Y%m%d-%H%M%S") + '.csv'
df.to_csv(path_or_buf=file, index=False)
