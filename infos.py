"""all / what future looks like"""
# xpath ; username input box
username_box = '//input[@name="username"]'
# xpath ; password input box
password_box = '//input[@name="password"]'

"""post_to_ig.py"""
# instagram login url (base)
ig_log_page = 'https://instagram.com/accounts/login/'
# xpath ; save info pupup (occours ~45% of time)
save_info_popup = '//*[contains(text(),"Save Info")]'
# xpath ; new post button
new_post_button = '//span[@aria-label="New Post"]'

"""bot.py"""
# plugins, base urls, and paths
instagram = 'https://www.instagram.com/'
ig_login_button = '//a[@href="/accounts/login/?source=auth_switcher"]'
instagram_tags_url = 'https://www.instagram.com/explore/tags/'
scroll = "window.scrollTo(0, document.body.scrollHeight);"
like = '//span[@aria-label="Like"]'
