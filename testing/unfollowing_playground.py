import time
import pandas as pd
from instapy import InstaPy, relationship_tools, smart_run, unfollow_util
from user import u, p
"""looking into unfollowing possibilities 

code
  > https://github.com/timgrossmann/InstaPy/blob/10f2171b9bee5a54b824710dde7878d142c193dc/instapy/instapy.py#L3757
docs
  > https://github.com/timgrossmann/InstaPy/blob/master/DOCUMENTATION.md#unfollowing
"""

# 3 - Unfollow the users WHO do not follow you back:
# session.unfollow_users(amount=126, nonFollowers=True, style="RANDOM", unfollow_after=42*60*60, sleep_delay=655)
'''
def unfollow_users(
    self,
    amount: int = 10,
    custom_list_enabled: bool = False,
    custom_list: list = [],
    custom_list_param: str = "all",
    instapy_followed_enabled: bool = False,
    instapy_followed_param: str = "all",
    nonFollowers: bool = False,
    allFollowing: bool = False,
    style: str = "FIFO",
    unfollow_after: int = None,
    delay_followbackers: int = 0,  # 864000 = 10 days, 0 = don't delay
    sleep_delay: int = 600,
):
    """Unfollows (default) 10 users from your following list"""
'''
ref = 't_data/followers_and_following20190821-213242.csv'
# check there's a file loaded
if len(ref) < 10:
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
print(f'{len(followers)} followers\n'
      f'{len(following)} following\n'
      f'{len(follow_backers)} follow backers\n'
      f'{len(non_follow_backers)} non-follow backers\n')

if len(non_follow_backers) > 0:
    to_unfollow = input('would you like to unfollow any non-follow backers (y/n)? ')
    if to_unfollow == 'y':
        # determine how many accounts to unfollow
        n_unfollow = int(input('how many would you like to unfollow (int)? '))
        # limit it (low)
        if n_unfollow > 10:
            n_unfollow = 10
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
