import pandas as pd 

"""paths
"""
# xpath ; username input box
username_box = '//input[@name="username"]'
# xpath ; password input box
password_box = '//input[@name="password"]'
# xpath ; save info pupup (occours ~45% of time)
save_info_popup = '//*[contains(text(),"Save Info")]'
# xpath ; like button (heart)
like = '//span[@aria-label="Like"]'
# xpath ; new post button
new_post_button = '//span[@aria-label="New Post"]'
# xpath ; following button 
following_button = '//button[contains(text(),"Following")]'
# xpath ; unfollow button
unfollow_button = '//button[contains(text(),"Unfollow")]'
"""# xpath ; # posts by this account display
following_button = '//span[contains(text(),"posts")]'
# xpath ; # accounts following this account
following_button = '//button[contains(text(),"followers")]'
# xpath ; following button 
following_button = '//button[contains(text(),"following")]'""" # soon come
# xpath ; instagram 404 page text
# ig_not_available = '//[contains(text(),"The link you followed may be broken, or the page may have been removed.")]'

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
hashtags_2 = ['videogames', 'videogame', 'battleroyale', 'freeforall', 'codblackout', 'coptopplays',
            'codclipsdaily', 'codclips', 'proplayer', 'like4like', 'fazetesty', 'streamer']
hashtags = ['callofduty', 'codnation', 'blackops4', 'multiplayer', 'xbox', 'ps4', 'twitch', 'esports',
                'coderedtourneyment', 'popupcup', 'gamingmemes', 'memes', 'ninja', 'pogchamp', 'twitch',
            'likeback', 'cod', 'longshot', 'ttv', 'faze']






