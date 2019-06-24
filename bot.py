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
from infos import follows_users, by_users, unfollow_log, verified_unfollow_log, redo_unfollow_log, re_verified_unfollow_log
# paths
from infos import username_box, password_box, save_info_popup, like, following_button, unfollow_button, follow_button
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
        # set ds
        # self.ds = self.DataScience()
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
        sleep(3)
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

    def close_browser(self):
        """closes webdriver
        """
        self.driver.close()  
        
    def generate_actionable_uls(self, potential_accounts, n, white_list_accounts):
        """identify accounts elgible for action from pd dataframe via 
        compairson to dataframe of non/previously-actionable accounts

        inputs:
        > potential_accounts
            >> pandas dataframe of accounts up for action
                > with account urls in .user_profile column
        > n
            >> number of accounts on which action will be taken in this round
        > white_list_accounts
            >> pandas dataframe of accounts which have already been acted upon
                > with account urls in .user_profile column

        output:
        > list of urls belonging to potential_accounts not found in white_list_accounts
        """
        # pull/tag potential urls 
        potential_urls = [url for url in potential_accounts.user_profile]
        # pull/tag previously seen urls
        already_actioned = [url for url in white_list_accounts.user_profile]
        # forget already actioned urls
        elgible_urls = [url for url in potential_urls if url not in already_actioned]
        # range matters
        if n != False:
            # shrink numer of accounts to desired range
            elgible_urls = elgible_urls[:n]
        # output actionable accounts
        return elgible_urls

    def unfollow(self, account_url):
        """unfollow given account 

        inputs:
        > account_url
            >> url of account to unfollow

        output:
        > list detailing transaction
            >> check/click 'following', check/click 'unfollowing', datetime
        """
        # load the account's profile
        self.driver.get(account_url) 
        # test for/find and click the 'following' button (0=success)
        ntract_following = check_xpath(webdriver=self.driver, 
                                    xpath=following_button, 
                                    click=True,
                                    hedge_load=5)
        # following button went well
        if ntract_following == 0:
            # wait a bit (hedge load)
            sleep(3)                    
            # test for/find and click the 'unfollow' button (0=success)
            ntract_unfollow = check_xpath(webdriver=self.driver, 
                                        xpath=unfollow_button, 
                                        click=True)
        # following buttion did not go well
        else:
            # unfollow no longer possible
            ntract_unfollow = 'nan'
        # output instance of unfollowing for log
        return list(ntract_following, ntract_unfollow, datetime.datetime.now())

    def record_recents(self, recents, record_log):
        """record given info into csv log 

        inputs:
        > recents
            >> information (from recent transactions) to be recorded
        > record_log
            >> csv file where information is to be recorded
        """
        # open up that redo log 
        with open(record_log, 'a') as f:
            # fit the writer
            writer = csv.writer(f)
            # go though each information point 
            for transaction in recents:
                # document the information
                writer.writerow(transaction)    

