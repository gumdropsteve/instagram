# timing 
import random
from time import sleep
# reading
import numpy as np
import pandas as pd
# recording
import csv
import datetime
# webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException 
# outside functions
from helpers import check_xpath
# misc
from infos import scroll, plsntn_re_tags
# data
from infos import follows_users, by_users
# urls
from infos import ig_log_page, ig_tags_url
# paths
from infos import username_box, password_box, save_info_popup, like, following_button, unfollow_button

class InstagramBot:

    def __init__(self, username, password):
        # tag the options field
        options = webdriver.FirefoxOptions()  
        # disable push/popups 
        options.set_preference("dom.push.enabled", False)  
        '''
        options allows the blocking of popups 
        this is not required for this script as it is currently written
        may become necessary in future editions
        to disable, change (options=options) to ()
        '''
        # set user
        self.username = username
        # set pwrd
        self.password = password
        # set driver with options 
        self.driver = webdriver.Firefox(options=options)

    def closeBrowser(self):
        """
        closes webdriver
        """
        self.driver.close()

    def login(self):
        """
        loads and logs in to instagram
        """
        # set driver
        driver = self.driver
        # load instagram login page
        driver.get(ig_log_page)
        # wait (hedge load time)
        sleep(2)
        # find user box, type in account id
        driver.find_element_by_xpath(username_box).send_keys(self.username)
        # find key box and call locksmith, he should be able to punch in
        driver.find_element_by_xpath(password_box).send_keys(self.password, Keys.RETURN)
        # hedge request/load time 
        sleep(3)
        # take care if "save info" pop-up page pops up
        check_xpath(webdriver=driver, xpath=save_info_popup, click=True)

    def like_photos(self, hashtag):
        from infos import ig_tags_url
        # set driver
        driver = self.driver
        # load the webpage to which the image belongs 
        driver.get(ig_tags_url + hashtag + '/')
        # better safe than sorry
        sleep(2)

        """gather a nice collection of posts
        """
        # set base collection for hrefs 
        pic_hrefs = []
        # next step will be repeated 7 times to load 7 scrolls of pictures (adjustable)
        for _ in range(7):
            # this should work
            try:
                # it's almost like we're human
                driver.execute_script(scroll)
                # so pause and maybe they won't catch on
                sleep(2)
                # get page tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            # but just in case
            except:
                # let us know it didn't work, and which iteration 
                print(f'except Exception: #{_} gathering photos')
                # and keep moving
                continue

        """actually liking the posts
        """
        # note how many posts there are 
        unique_photos = len(pic_hrefs)
        # go through each one
        for pic_href in pic_hrefs:
            # load the post
            driver.get(pic_href)
            # hedge for whatever
            sleep(2)
            # move around a bit, make sure we can see the heart (like button)
            driver.execute_script(scroll)
            # this should work
            try:
                # hesitate a bit; you're human, right?
                sleep(random.randint(2, 4))
                # find the like button 
                like_button = lambda: driver.find_element_by_xpath(like).click()
                # click the like button
                like_button().click()
                
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    # take a minimal break 
                    sleep(1)
            # if it doesn't work
            except:
                # we don't really have a backup plan.. so take a break ig..
                sleep(2)
            # update count of remaining posts
            unique_photos -= 1
            # let us know how many remain
            print(unique_photos)
    
    def analyze_following(self, followers=by_users, following=follows_users, to_unfollow=False, follow_backers=False):
        """identifies users who you are following that do not follow you back
        and other stuff, we're not all negative, more to come
        """
        # url of each account following us
        by_usernames = np.array(followers.user_profile)
        # url of each account we follow
        follows_usernames = np.array(following.user_profile)
        
        # requested accounts to unfollow?
        if to_unfollow == True:
            # output urls of profiles to unfollow 
            return [user for user in follows_usernames if user not in by_usernames]

        # requested accounts to never unfollow?
        if follow_backers == True:
            # output urls of profiles to keep following
            return [user for user in follows_usernames if user in by_usernames]

        #otherwise
        else:
            # not much
            pass
        
    
    def unfollow(self, start=0, end=250):
        """
        NEEDS: more tuned outcomes

        goes through list of accounts
            loads the current account's profile url
                makes sure that account is cleared for unfollowing
                    unfollows the account 
        inputs)
            >> accounts
                > list of accounts eligible for unfollowing
            >> n
                > number of those accounts we're going to unfollow right now
                    >> rec: n < 250 , due to mass unfollowing (usually) being prohibited 
                    >> default: 1 (i.e. two (2) accounts)
        """
        # create csv to store accounts we have unfollowed (so do not re-follow in future)
        with open('accounts_ttvpa_used_to_follow.csv', 'a', newline='') as file:
            # set writer to this file
            the_writer = csv.writer(file)
            # write column names
            the_writer.writerow(['account_id','username','profile_url','time_unfollowed'])
        
        # generate list of accounts qualified to unfollow
        accounts_to_unfollow = InstagramBot.analyze_following(self, to_unfollow=True)

        # retag driver
        driver = self.driver
        
        # go through first n urls
        for user_url in accounts_to_unfollow[start:end]:
            '''prime the mission'''
            # load the url
            driver.get(user_url)
            # wait for profile page to load
            sleep(3)
            # test for/find and click the 'following' button  
            check_xpath(webdriver=driver, xpath=following_button, click=True)
            # wait a bit (hedge load)
            sleep(2)
            
            '''set up recording of transaction'''
            # pull the account's record
            this_account = follows_users.loc[follows_users.user_profile == user_url]

            # account's id number
            account_id = int(this_account.id)
            # account's username
            username = str(this_account.username)
            # account's url
            profile_url = user_url

            # set values to be recorded (to the ranch!)
            fields = [account_id, username, profile_url, datetime.datetime.now()]
            
            '''execute'''
            # test for/find and click 'unfollow' button in popup 
            check_xpath(webdriver=driver, xpath=unfollow_button, click=True, send_keys=False, keys=None)
            
            '''record the transaction'''
            # open up the csv
            with open('accounts_ttvpa_used_to_follow.csv', 'a') as _f:
                # fit the writer
                writer = csv.writer(_f)
                # document the transaction
                writer.writerow(fields)
            # pause so we can do this for a long time without breaching the unfollow limit 
            sleep(10)


# determine mode
mode='unfollow'  # 'like'
# make this a runable script 
if __name__ == "__main__":
    """
       ***adjust lines 135-143 to fit your style***
    """
    # loading login info 
    from _pile import utv, ptv
    # your username 
    u = utv 
    # your password
    p = ptv  

    # label the bot
    ig = InstagramBot(username=u, password=p)
    # get the party started 
    ig.login()

    if mode == 'like':
        # insert your desired hashtags here (list)
        hashtags = plsntn_re_tags

        while True:
            # this should work until all tags have been used
            try:
                # choose a random tag from the list of tags
                tag = random.choice(hashtags)
                # like the posts under that tag
                ig.like_photos(tag)
            # if it doesn't, or (hopefully) we're done
            except Exception:
                # close her down
                ig.closeBrowser()
                # take a break 
                sleep(600)
                # retry the bot 
                ig = InstagramBot(username=u, password=p)

    elif mode == 'unfollow':
        ig.unfollow(start=1500,end=1750)
