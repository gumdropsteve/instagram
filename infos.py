import pandas as pd 

"""xpaths
"""
# username input box
username_box = '//input[@name="username"]'
# password input box
password_box = '//input[@name="password"]'
# save info pupup (occours ~45% of time)
save_info_popup = '//*[contains(text(),"Save Info")]'
# like button (heart)
like = '//span[@aria-label="Like"]'
# comment button 
comment_button = '//span[@aria-label="Comment"]'
# comment box
comment_box = '//*[@aria-label="Add a comment…"]'
# new post button
new_post_button = '//span[@aria-label="New Post"]'
# following button 
following_button = '//button[contains(text(),"Following")]'
# unfollow button
unfollow_button = '//button[contains(text(),"Unfollow")]'
# follow button
follow_button = '//button[contains(text(),"Follow")]'

"""urls
"""
# instagram login url (base)
ig_log_page = 'https://instagram.com/accounts/login/'
# base url for tags
ig_tags_url = 'https://www.instagram.com/explore/tags/'

"""webdriver focused
"""
# js scroll to bottom of page
scroll = "window.scrollTo(0, document.body.scrollHeight);"
# for the profile necessary to enable mobile view
user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) \
              AppleWebKit/528.18 (KHTML,like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"

"""data
"""
# load accounts & info on followed
follows_users = pd.read_csv('data/scraped/follows_users_ttv_princearthur_20190421_2205.csv')
# load accounts & info on following
by_users = pd.read_csv('data/scraped/followed_by_users_ttv_princearthru_20190421_1846.csv')
# load .unfollow() log
unfollow_log = pd.read_csv('data/made/accounts_ttvpa_used_to_follow.csv')
# load verified .unfollow() log
verified_unfollow_log = pd.read_csv('data/made/verified_accounts_ttvpa_used_to_follow.csv')
# load redo.unfollow() log
redo_unfollow_log = pd.read_csv('data/made/redone_accounts_ttvpa_used_to_follow.csv')
# load re-revified .unfollow() log
re_verified_unfollow_log = pd.read_csv('data/made/re_verified_accounts_ttvpa_used_to_follow.csv')
# load mass log from 2nd scrape
second_round_all=pd.read_csv('data/scraped/All_users_ttv.princearthur_20190613_2119.csv')
# followers from 2nd round (len = 1458)
s2_follows_princearthur=[url for url in second_round_all.loc[second_round_all.user_followed_by==True].user_profile]
# following from 2nd round (len = 1080)
s2_princearthur_follows=[url for url in second_round_all.loc[second_round_all.user_follows==True].user_profile]
# 2nd round accounts following that are not followers (len = 441)
s2_eligible_for_unfollowing=[url for url in s2_princearthur_follows if url not in s2_follows_princearthur]
# draft final database layout
draft_log = pd.read_csv('data/made/unfollow_log.csv')

"""hashtags
"""
# general real estate
gen_real_estate_tags = ['homesforsale', 'fsbo', 'forsalebyowner', 'realestate', 'realty', 'realtor', 'nar']
# california real estate
ca_real_estate_tags = ['californiarealestate']
# bay area real estate
bay_real_estate_tags =['bayarearealestate', 'bayareahomes']
# general california
gen_california_tags = ['californialife', 'californiaadventure']
# east bay real estate
pleasanton_tags = ['pleasanton', 'pleasantonhomesforsale']
# gaming tags
hashtags_2 = ['videogames', 'videogame', 'battleroyale', 'freeforall', 'codblackout', 'coptopplays',
            'codclipsdaily', 'codclips', 'proplayer', 'like4like', 'fazetesty', 'streamer']
# gaming tags
hashtags = ['callofduty', 'codnation', 'blackops4', 'multiplayer', 'xbox', 'ps4', 'twitch', 'esports',
                'coderedtourneyment', 'popupcup', 'gamingmemes', 'memes', 'ninja', 'pogchamp', 'twitch',
            'likeback', 'cod', 'longshot', 'ttv', 'faze']






