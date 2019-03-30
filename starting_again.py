import pandas as pd
import numpy as np

#                  id  follows_count  ...  region_name  country_code
# count  8.104000e+03    2389.000000  ...          0.0           0.0
# mean   5.412701e+09     700.983257  ...          NaN           NaN
# std    3.152647e+09    1293.038622  ...          NaN           NaN
# min    9.280000e+04       0.000000  ...          NaN           NaN
# 25%    2.178089e+09      75.000000  ...          NaN           NaN
# 50%    6.328614e+09     242.000000  ...          NaN           NaN
# 75%    8.388525e+09     672.000000  ...          NaN           NaN
# max    1.140352e+10    7509.000000  ...          NaN           NaN
# [8 rows x 11 columns]
df = pd.read_csv( 'data/All_users_ttv.princearthur_20190303_0543.csv' )
# <class 'pandas.core.frame.DataFrame'>
# RangeIndex: 8104 entries, 0 to 8103
# Data columns (total 30 columns):
# id                        8104 non-null int64
# username                  8104 non-null object
# full_name                 7619 non-null object
# user_profile              8104 non-null object
# followed_by_viewer        8104 non-null bool
# requested_by_viewer       8104 non-null bool
# user_follows              8104 non-null bool
# user_followed_by          8104 non-null bool
# profile_pic_url           8104 non-null object
# profile_pic_url_hd        2389 non-null object
# is_private                2389 non-null object
# follows_count             2389 non-null float64
# followed_by_count         2389 non-null float64
# media_count               2389 non-null float64
# latestPostDate            2346 non-null object
# follows_viewer            2389 non-null object
# has_requested_viewer      2389 non-null object
# blocked_by_viewer         2389 non-null object
# has_blocked_viewer        2389 non-null object
# biography                 2206 non-null object
# is_verified               8104 non-null bool
# is_business_account       2389 non-null object
# business_category_name    1160 non-null object
# business_email            0 non-null float64
# business_phone_number     0 non-null float64
# street_address            0 non-null float64
# zip_code                  0 non-null float64
# city_name                 0 non-null float64
# region_name               0 non-null float64
# country_code              0 non-null float64
# dtypes: bool(5), float64(10), int64(1), object(14)
# memory usage: 1.6+ MB
# None

'''
notes
    df['user_follows'] == df['followed_by_viewer']
'''



# print(sum(df['follows_viewer'] == True) , sum(df['followed_by_viewer']==True))
# print(sum(df['user_follows']) , sum(df['followed_by_viewer']))
# qq = 0
# for _ in range(len(df['user_follows'])):
#     if df['user_follows'][_] == df['followed_by_viewer'][_]:
#         qq+=1
# guess = df['follows_viewer']==df['followed_by_viewer']
# sguess = sum(guess)
# print(sguess==len(df['follows_viewer']))
# print(sguess)

# for _ in df['id']:
#     print(_)

# for _ in range(len(df['follows_viewer'])):
#     if df['follows_viewer'][_] == True:
        # print(f"{df['username'][_]} {df['follows_viewer'][_]}")
    # print(df['follows_viewer'][_])
# print(df['follows_viewer'])
'''[x for b in a for x in b]'''
# f = [ user for _ in range(len(df['username'])) for user in df['username'][_] if df['follows_viewer'][_] == True ]  # if df['follows_viewer'][_] == True
followers = []
for _ in range(len(df['username'])):
    if df['follows_viewer'][_] == True:
        followers.append(df['username'][_])


# print(len(df['username']),len(df['follows_viewer']))
# davidarnett2004
# print(df['follows_viewer'].pop(0))
# for _ in range(1, len(df['follows_viewer'])):
#     if df['username'][_] == 'davidarnett2004':
#         print(_)
# print(df['username'].head())
# tup = tuple(followers)
# print(len(tup) , len(followers))
# double = []
# for _ in followers:
#     if _ not in double:
#         double.append(_)

# print(len(double) , len(followers))
# print(len(f))
# print(len(followers))
print(followers)
