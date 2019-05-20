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
follows_users = pd.read_csv('data/follows_users_ttv_princearthur_20190421_2205.csv')
# load accounts & info on following
by_users = pd.read_csv('data/followed_by_users_ttv_princearthru_20190421_1846.csv')

"""misc.
"""
# pleasanton real estate tags
plsntn_re_tags = ['pleasanton', 'californialife', 'californiaadventure', 'homesforsale', 'fsbo', 'californiarealestate', 'pleasantonhomesforsale', 'bayarearealestate', 'forsalebyowner']







