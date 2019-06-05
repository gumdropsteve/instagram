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
from infos import follows_users, by_users, unfollow_log, verified_unfollow_log, redo_unfollow_log
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
        # generate full list of urls qualified to unfollow
        urls_to_unfollow = InstagramBot.analyze_following(self, followers=by_users, 
                                                          following=follows_users, to_unfollow=True)
        # trim list to urls in start/end range
        accounts_in_range = urls_to_unfollow[start:end]

        # call up the lady at the county recorders office (previously visited urls)
        previously_seen_ulrs = InstagramBot.analyze_following(self, followers=by_users.iloc[0],
                                                              following=unfollow_log, to_unfollow=True)
        # forget urls which are in the start/end range but have been visited before
        accounts_to_unfollow = [url for url in accounts_in_range if url not in previously_seen_ulrs]
        
        # within the number of loops equal to the number of urls
        for i in range(len(accounts_to_unfollow)):
            '''prime the mission'''
            # tag the url you encounter
            user_url = accounts_to_unfollow[i]
            # load that url
            self.driver.get(user_url)
            # wait for profile page to load
            sleep(3)
            
            # test for/find and click the 'following' button (0=success)
            ntract_following = check_xpath(webdriver=self.driver, xpath=following_button, click=True)
            
            """# was the button found & clicked
            if ntract_following ==  0:"""  # to be added after data for 6,12 test has been collected
            # wait a bit (hedge load)
            sleep(2)
            
            '''set up recording of transaction'''
            # pull the account's record
            this_account = follows_users.loc[follows_users.user_profile == user_url]

            # account's id number
            account_id = int(this_account.id)
            # account's username
            username = list(this_account.username)[0]
            # account's url
            profile_url = user_url

            # set values to be recorded (to the ranch!)
            fields = [account_id, username, profile_url, datetime.datetime.now(), ntract_following]
            
            '''execute'''
            # test for/find and click 'unfollow' button in popup 
            ntract_unfollow = check_xpath(webdriver=self.driver, xpath=unfollow_button, 
                                          click=True, send_keys=False, keys=None)
            
            """start temp fix of 1,1 logic issue"""  # adjust time measures (very slightly) to reflect
            # 'Following' was never found/clicked
            if ntract_following == 1:
                # double check "impossible" case
                if ntract_unfollow != 0:
                    # so 'Unfollow' button was not expected
                    ntract_unfollow = 'N/a' 
                # double check "impossible" case
                elif ntract_unfollow == 1:
                    raise Exception(f'"IMPOSSIBLE" CASE : ntract_unfollow == 1')
            """end temp fix of 1,1 logic issue"""  # adjust time measures (very slightly) to reflect

            # note outcome for csv (0=success)
            fields.append(ntract_unfollow)
            """# was 'Following' button found and clicked
            if ntract_following == 0:
                # test for/find and click 'unfollow' button in popup 
                ntract_unfollow = check_xpath(webdriver=self.driver, xpath=unfollow_button, 
                                              click=True, send_keys=False, keys=None)
            else:
                ntract_unfollow = 'N/a'
            # set values to be recorded (to the ranch!)
            fields = [account_id, username, profile_url, datetime.datetime.now(), 
                      ntract_following, ntract_unfollow]"""  # to be added after data for 6,12 test has been collected

            '''record the transaction'''
            # open up the csv
            with open('data/made/accounts_ttvpa_used_to_follow.csv', 'a') as _f:
                # fit the writer
                writer = csv.writer(_f)
                # document the transaction
                writer.writerow(fields)
            
            # did we actually successfully unfollow
            if ntract_unfollow == 0:
                # pause so we can do this for a long time without breaching the unfollow limit 
                sleep(random.randint(6,12))

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

    def redo_unfollow(self, start=0, end=250, verification=True, record_thresh=10):
        # pull urls 
        potential_urls = [url for url in verified_unfollow_log.user_profile]
        # pull previously redone 
        already_redone = redo_unfollow_log
        # tag previously redone urls
        redone_urls = [url for url in already_redone.user_profile]
        # forget redone urls
        urls_not_redone = [url for url in potential_urls if url not in redone_urls]
        # shrink to range
        urls_to_redo = urls_not_redone[start:end]
        # start log for multi account writing
        log = []
        # start count of number of accounts unfollowed
        redone_count = 0
        # start log for re-unfollowed check
        re_unfollowed = []
        # go through each url to redo
        for n in range(len(urls_to_redo)):
            # focus this url
            url = urls_to_redo[n]
            # locate account
            account = verified_unfollow_log.loc[verified_unfollow_log.user_profile == url]
            # label account info 
            info = [i for column in account.values for i in column]
            # account was actually unfollowed
            if info[6] == 0:
                # make n/a values
                na = ['n/a','n/a',datetime.datetime.now()]
                # go through na values
                for _ in na:
                    # add n/a values
                    info.append(_)
                # add the account to temp log
                log.append(info)
                # did not unfollow or load page, minimal time off 
                sleep(1)
            # account was not actually unfollowed
            elif info[6] == 1:
                # load that url
                self.driver.get(url)      
                # wait for profile to load
                sleep(5)
                # test for/find and click the 'following' button (0=success)
                ntract_following = check_xpath(webdriver=self.driver, xpath=following_button, click=True)
                # add to account log
                info.append(ntract_following)
                # wait a bit (hedge load)
                sleep(3)                    
                # test for/find and click the 'unfollow' button (0=success)
                ntract_unfollow = check_xpath(webdriver=self.driver, xpath=unfollow_button, 
                                              click=True, send_keys=False, keys=None)
                # add to account log
                info.append(ntract_unfollow)
                # note time
                time_redone = datetime.datetime.now()
                # add to unfollow count
                redone_count += 1
                # add time account log
                info.append(time_redone)
                # add this account to log
                log.append(info)
                # note instance 
                re_unfollowed.append(url)
                
                # this isn't a 5th unfollow
                if redone_count % 5 != 0:
                    # take some time off so we hopefully don't get blocked 
                    sleep(30)
                
                # unfollow verification (for nth unfollowing) 
                elif redone_count % 5 == 0:
                    # hyper verification?
                    if verification == 'hyper':
                        # tag 1st from this set of 5
                        first = re_unfollowed[0]
                        # load first unfollow
                        self.driver.get(first)
                        # wait for load
                        sleep(5)
                        # check for 'Following' button 
                        fing_button = check_xpath(webdriver=self.driver, xpath=following_button, click=True)
                        # it exists; we did not unfollow 
                        if fing_button == 0:
                            # halt progress; we are probably blocked
                            raise Exception(f"fing_button == {fing_button} ;\naccount == {middle}\n\nrecent unfollows == {re_unfollowed}")
                        # it does not exist; we unfollowed
                        else:
                            # some sort of glitch
                            if fing_button != 1:
                                # so that's noteworthy
                                raise Exception(f'fing_button != 1 ;\nfing_button == {fing_button} ;\naccount == {middle}')
                            # otherwise, good; so let us know
                            print(f'5th test == pass')
                            # reset temp unfollowed log
                            re_unfollowed = []
                        # and break normally
                        sleep(30)
                    # the (defined) usual
                    elif verification == True:
                        # normal verification
                        if redone_count % 25 == 0:
                            # tag middle unfollow for this set
                            middle = re_unfollowed[12]
                            # load middle unfollow 
                            self.driver.get(middle) 
                            # wait for load
                            sleep(5)
                            # check for 'Following' button 
                            fing_button = check_xpath(webdriver=self.driver, xpath=following_button, click=True)
                            # it exists; we did not unfollow 
                            if fing_button == 0:
                                # halt progress; we are probably blocked
                                raise Exception(f"fing_button == {fing_button} ;\naccount == {middle}\n\nrecent unfollows == {re_unfollowed}")
                            # it does not exist; we unfollowed
                            else:
                                # some sort of glitch
                                if fing_button != 1:
                                    # so that's noteworthy
                                    raise Exception(f'fing_button != 1 ;\nfing_button == {fing_button} ;\naccount == {middle}')
                                # otherwise, good; so let us know
                                print(f'25th test == pass')
                                # reset temp unfollowed log
                                re_unfollowed = []
                        # break normally
                        sleep(30)
                    # no verification 
                    elif verification == False:
                        # ok, but every once in a while
                        if redone_count % 25 == 0:
                            # remind us
                            print(f"verification == {verification}")
                        # and don't forget break
                        sleep(30)
                    # unknown verification
                    else:
                        # let us know
                        print(f"\nERROR ; non-fatal ERROR ; verification method unknown ; verification == {verification}\n")
                    # it's a 500th
                    if redone_count % 500 == 0:
                        # let us know
                        print(f'\nredone_count == {redone_count}   >> taking an extra 10 minutes\n')
                        # take extra break 
                        sleep(60*10)
                    # it's a 100th 
                    elif redone_count % 100 == 0:
                        # let us know
                        print(f'\nredone_count == {redone_count}   >> taking an extra 5 minutes\n')
                        # take extra break 
                        sleep(60*5)
                    # it's a 50th
                    elif redone_count % 50 == 0:
                        # let us know
                        print(f'\nredone_count == {redone_count}   >> taking an extra minute\n')
                        # take extra break 
                        sleep(60)
                # idk (would be unexpected)
                else:
                    # so indicate
                    raise Exception(f"redone_count == {redone_count}")
            # this would be unexpected
            else:
                # so make it known
                raise Exception(f'info[6] == {info[6]}')

            # this is a nth iteration (or we're almost done)
            if n % record_thresh == 0 or len(urls_to_redo) - n < 2:
                # open up that redo log 
                with open('data/made/redone_accounts_ttvpa_used_to_follow.csv', 'a') as _f:
                    # fit the writer
                    writer = csv.writer(_f)
                    # go though each account 
                    for info in log:
                        # document the transaction
                        writer.writerow(info)
                    # reset temp log
                    log = []
                    
            # on first loop
            if n == 0:
                # lay out the situation 
                print(f'up and running ; {len(urls_to_redo)-1} to go ; {datetime.datetime.now()}')

            # every 25th loop
            if n % 25 == 0 and n != 0:
                # are we on a 50th
                if n % 50 == 0:
                    # display raw number completion
                    print(f'{n}/{len(urls_to_redo)} complete ; {datetime.datetime.now()}')
                # or just a quarter
                else:
                    # display percentage completion
                    print(f'{int(100*(n/len(urls_to_redo)))}% complete ; {datetime.datetime.now()}')        



    """# class DataScience:

    #     def __init__(self):
    #         # account followers
    #         self.followers = by_users
    #         # account following
    #         self.following = follows_users
    #         # accounts which have been unfollowed
    #         self.unfollowed = unfollow_log
    #         # accounts which have been unfollow verified
    #         self.verified = verified_unfollow_log
    #         # set user
    #         self.user = InstagramBot.username
    #         # set driver
    #         self.driver = InstagramBot(self.username, self.password).driver"""  # coming; eventually 
    # ALL BELOW ARE METHODS OF DataScience SUB-class

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

    def check_counts(self, uncounted_log=verified_unfollow_log, s=0, e=250):
        """
        takes list of accounts that have been through .verify_unfollow()
        visits each profile, checks counts for posts, followers, following
        if the user is still followed, unfollows them
        documents all times 
        """
        pass

    def verify_unfollow(self, log=unfollow_log, prior=verified_unfollow_log, 
                        start=0, end=250):
        """takes list of accounts that have been 'unfollowed' in unfollow_log
        visits each profile, checks for existance of 'Following' button
        if 'Following' button exists, account was obviously not unfollowed
        rewrites unfollow_log with new 'actually_unfollowed' and 'time_checked' columns
            to verified_accounts_ttvpa_used_to_follow.csv

        inputs)
            > webdirver
                >> driver in use
            > log 
                >> log of accounts which have been run through bot.py 
                    > default = unfollow_log
            > prior 
                >> accounts which have gone through verification process
                    > default = verified_unfollow_log
            > start
                >> first instance to consider
            > end
                >> last instance to consider
        """
        # set out route
        out = []
        # id urls verified
        verified_urls = [url for url in prior.user_profile]
        # focus & trim log urls
        url_log = [url for url in log.user_profile[start:end] if url not in verified_urls]
        # determine # of accounts to be verified
        num_to_verify = len(url_log)
        # assuming it's not 0
        if num_to_verify != 0:
            # go through each
            for _ in range():
                # tag that url
                url = url_log[_]
                # pull that account's info in log & make into a list of unique values
                this_user = [datapoint for list in log.loc[log.user_profile == url].values 
                            for datapoint in list]
                # load the url in question
                self.driver.get(url)
                # hold up
                sleep(random.randint(2,3))
                # check for 'Following' button
                check = check_xpath(webdriver=self.driver, xpath=following_button, 
                                    click=False, send_keys=False, keys=None)
                # does it exist?
                if check == 0:
                    # never actually unfollowed 
                    this_user.append(1)
                # does it not exist?
                elif check == 1:
                    # ok, so we unfollowed (unless it's 404)
                    this_user.append(0)
                # check for 'Follow' button
                check_404 = check_xpath(webdriver=self.driver, xpath=follow_button, 
                                        click=False, send_keys=False, keys=None)
                # does it exist?
                if check_404 == 0:
                    # this is not a 404
                    this_user.append(0)
                # does it not exist?
                elif check_404 == 1:
                    # this is a possible 404
                    this_user.append(1)
                # and note the time
                this_user.append(datetime.datetime.now())
                # to the ranch!
                out.append(this_user)
                '''record the transaction
                '''  # moved & staggered to allow ctrl + c at minimal cost
                # every 5th we will record (and each remainder at end)
                if _ % 10 == 0 or num_to_verify - _ < 1:
                    # open up the csv
                    with open('data/made/verified_accounts_ttvpa_used_to_follow.csv', 'a') as file:
                        # fit the writer
                        writer = csv.writer(file)
                        # each out is an account
                        for user in out:
                            # document the transaction
                            writer.writerow(user)
                        # reset temp log
                        out = []

                # on first loop
                if _ == 0:
                    # lay out the situation 
                    print(f'zeroth account has been verified ; {len(url_log)-1} to go ; {datetime.datetime.now()}')
                # every 25th loop
                if _ % 25 == 0 and _ != 0:
                    # are we on a 50th
                    if _ % 50 == 0:
                        # display raw number completion
                        print(f'{_}/{len(url_log[start:end])} complete ; {datetime.datetime.now()}')
                    # or just a quarter
                    else:
                        # display percentage completion
                        print(f'{int(100*(_/len(url_log)))}% complete ; {datetime.datetime.now()}')
        # but if it is
        else:
            # let us know
            print(f'{num_to_verify} accounts need verification')

