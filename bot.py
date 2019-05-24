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

# .js help
from infos import scroll
# functions
from helpers import check_xpath
# urls
from infos import ig_log_page, ig_tags_url
# data (loaded here for future multitasking)
from infos import follows_users, by_users, unfollow_log
# paths
from infos import username_box, password_box, save_info_popup, like, following_button, unfollow_button
# misc
from infos import ig_tags_url


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
        # minimize browser window
        self.driver.minimize_window()

    def login(self):
        """
        loads and logs in to instagram
        """
        # load instagram login page
        self.driver.get(ig_log_page)
        # wait (hedge load time)
        sleep(2)

        # find user box, type in account id
        self.driver.find_element_by_xpath(username_box).send_keys(self.username)
        # find key box and call locksmith, he should be able to punch in
        self.driver.find_element_by_xpath(password_box).send_keys(self.password, Keys.RETURN)
        # hedge request/load time 
        sleep(3)
        
        # take care if "save info" pop-up page pops up
        check_xpath(webdriver=self.driver, xpath=save_info_popup, click=True)

    def like_photos(self, hashtag):
        """collects group of image urls by hashtag
        then loads & likes each individually 
        """
        # set driver
        driver = self.driver
        
        # load the webpage to which the image belongs 
        driver.get(ig_tags_url + hashtag + '/')
        # better safe than sorry
        sleep(2)

        '''gather a nice collection of posts
        '''
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
                print("Check: pic href length " + str(len(pic_hrefs)))
            # but just in case
            except:
                # let us know it didn't work, and which iteration 
                print(f"except Exception: #{_} gathering photos")
                # and keep moving
                continue

        '''actually liking the posts
        '''
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

    def closeBrowser(self):
        """closes webdriver
        """
        self.driver.close()  

    def analyze_following(self, followers=by_users, following=follows_users, 
                          to_unfollow=False, follow_backers=False, previous=False):
        """identifies users who you are following that do not follow you back
        and other stuff, we're not all negative, more to come
        """
        # url of each account following us
        by_usernames = np.array(followers.user_profile)
        # url of each account we follow
        follows_usernames = np.array(following.user_profile)
        
        # requested accounts to unfollow?
        if to_unfollow == True:
            # identify urls of profiles to unfollow 
            un = [user for user in follows_usernames if user not in by_usernames]
            # are we considering previous
            if previous == True:
                # so list out previous
                prev = [user for user in unfollow_log.user_profile]
                # and consider them
                return [user for user in un if user not in prev]
            # otherwise
            else:
                # gimme da loot
                return un

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
        # init & trim following
        self.follows = follows_users[start:end]
        # init & trim followers
        self.followers = by_users[start:end]

        # generate full list of urls qualified to unfollow (include previously seen urls)
        accounts_to_unfollow = InstagramBot.analyze_following(self, followers=self.follows, 
                                                              following=self.followers, 
                                                              to_unfollow=True, previous=True)
        print(len(accounts_to_unfollow))
        sleep(4)
        # retag driver
        driver = self.driver

        # within the number of loops equal to the number of urls
        for i in range(len(accounts_to_unfollow)):
            '''prime the mission'''
            # tag the url you encounter
            user_url = accounts_to_unfollow[i]
            # load that url
            driver.get(user_url)
            # wait for profile page to load
            sleep(3)
            # test for/find and click the 'following' button (0=success)
            ntract_following = check_xpath(webdriver=driver, xpath=following_button, click=True)
            # wait a bit (hedge load)
            sleep(2)
            
            '''set up recording of transaction'''
            # pull the account's record
            this_account = follows_users.loc[follows_users['user_profile'] == user_url]
            # account's id number
            account_id = this_account.id.values[0]
            # account's username
            username = list(this_account.username)[0]
            # account's url
            profile_url = user_url

            # set values to be recorded (to the ranch!)
            fields = [account_id, username, profile_url, datetime.datetime.now(), ntract_following]
            
            '''execute'''
            # test for/find and click 'unfollow' button in popup 
            ntract_unfollow = check_xpath(webdriver=driver, xpath=unfollow_button, 
                                          click=True, send_keys=False, keys=None)
            # note outcome for csv (0=success)
            fields.append(ntract_unfollow)

            '''record the transaction'''
            # open up the csv
            with open('accounts_ttvpa_used_to_follow.csv', 'a') as _f:
                # fit the writer
                writer = csv.writer(_f)
                # document the transaction
                writer.writerow(fields)
            
            # did we actually successfully unfollow
            if ntract_unfollow == 0:
                # pause so we can do this for a long time without breaching the unfollow limit 
                sleep(random.randint(7,12))

            # on first loop
            if i == 0:
                # lay out the situation 
                print(f'zeroth account has been unfollowed ; {len(accounts_to_unfollow)-1} to go ; {datetime.datetime.now()}')

            # every 25th loop
            if i % 25 == 0 and i != 0:
                # are we on a 50th
                if i % 50 == 0:
                    # display raw number completion
                    print(f'{i}/{len(accounts_to_unfollow[start:end])} complete ; {datetime.datetime.now()}')
                # or just a quarter
                else:
                    # display percentage completion
                    print(f'{int(100*(i/len(accounts_to_unfollow)))}% complete ; {datetime.datetime.now()}')
