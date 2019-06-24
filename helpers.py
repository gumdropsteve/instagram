from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  

'''
to add
detect if page is 404
    by text? 
recording info on the visuals
    what is the account broadcasting?
        rip sullivan --classic
    this may be better in bot?
        no? what is point of helpers?
            maybe.
'''


def check_xpath(webdriver, xpath, click=False, send_keys=False, keys=None, hedge_load=1):
    """checks if an xpath exists on the current page

    inputs)
        > webdriver
            >> driver being used
        > xpath
            >> xpath in question
        > click
            >> if clicking the element once/if found
        > send_keys
            >> if sending keys to element once/if found
        > keys
            >> keys being sent if sending keys (i.e. send_keys=True)

    output)
        > if successful
            >> 0
        > if unsuccessful
            >> 1
    """
    # hedge laod time
    sleep(hedge_load)
    # test this 
    try:
        # find xpath in question
        find_element = webdriver.find_element_by_xpath(xpath)
        # are we clicking
        if click == True:
            # yes, so click
            find_element.click()
            # hedge time
            sleep(3)
        # are we sending keys
        if send_keys == True:
            # yes, so send them
            find_element.send_keys(keys)
            # hedge time
            sleep(3)
        # element exists and was successfull
        return 0
    # if it didn't work
    except NoSuchElementException:
        # indicate as such
        return 1



# below is pending rewrite & approval
'''
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

    def analyze_following(self, 
                          followers=by_users, 
                          following=follows_users,
                          to_unfollow=False, 
                          follow_backers=False, 
                          previous=False):
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
                record the transaction
                # moved & staggered to allow ctrl + c at minimal cost
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

    def re_verify_unfollow(self, log=redo_unfollow_log, prior=re_verified_unfollow_log, 
                           start=0, end=250, out_log='data/made/re_verified_accounts_ttvpa_used_to_follow.csv'):
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
        # focus log urls
        url_focus = [url for url in log.user_profile if url not in verified_urls]
        # trim list to range
        url_log = url_focus[start:end]
        # determine # of accounts to be verified
        num_to_verify = len(url_log)
        # assuming it's not 0
        if num_to_verify != 0:
            # go through each
            for _ in range(num_to_verify):
                # tag that url
                url = url_log[_]
                # pull that account's info in log & make into a list of unique values
                this_user = [datapoint for list in log.loc[log.user_profile == url].values 
                            for datapoint in list]
                # not the first time
                if _ != 0:
                    # extra hold for night run
                    if _ % 10 == 0:
                        # rarely
                        if _ % 500 == 0:
                            # take a snooze
                            sleep(500)
                        # once in a while
                        elif _ % 50 == 0:
                            # less short
                            sleep(50)
                        # but normally
                        else:
                            # short
                            sleep(3)
                # load the url in question
                self.driver.get(url)
                # hold up
                sleep(3)
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
                # # record the transaction
                # moved & staggered to allow ctrl + c at minimal cost
                # every 5th we will record (and each remainder at end)
                if _ % 10 == 0 or num_to_verify - _ <= 1:
                    # open up the csv
                    with open(out_log, 'a') as file:
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
'''


