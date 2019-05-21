import numpy as np
import pandas as pd
df=pd.read_csv('accounts_ttvpa_used_to_follow.csv')
# a = np.empty(len(df))
# a.fill(np.nan)
# df['following_button']=pd.Series(a)
# df['unfollow_button']=pd.Series(a)
# df.to_csv('accounts_ttvpa_used_to_follow.csv')
# print(df[:790])
# print(df.columns)
lower_account_numbers = df['Unnamed: 0.1'][786:]
lower_account_usernames = df['account_id'][786:]
lower_account_urls = df['username'][786:]
lower_account_times = df['profile_url'][786:]
lower_account_fb = df['time_unfollowed'][786:]
lower_account_un = df['following_button'][786:]
# print(lower_account_numbers)
df = df[['account_id', 'username', 'profile_url',
       'time_unfollowed', 'following_button', 'unfollow_button']]
df['account_id'][786:] = lower_account_numbers
df['username'][786:]=lower_account_usernames
df['profile_url'][786:]=lower_account_urls
df['time_unfollowed'][786:]=lower_account_times
df['following_button'][786:]=lower_account_fb
df['unfollow_button'][786:]=lower_account_un
# print(df.head())
# print(df[780:].profile_url)
df.to_csv('accounts_ttvpa_used_to_follow.csv')
"""Index(['Unnamed: 0', 'Unnamed: 0.1', 'account_id', 'username', 'profile_url',
       'time_unfollowed', 'following_button', 'unfollow_button'],
      dtype='object')"""
