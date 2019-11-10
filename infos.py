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






