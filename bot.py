# timing 
import time
# reading
import numpy as np
import pandas as pd
# recording
import csv
from datetime import datetime
# webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
# .js help
from infos import scroll
# urls
from infos import ig_log_page, ig_tags_url
# paths
from infos import username_box, password_box, save_info_popup
from infos import comment_button, comment_box, like
# misc
from infos import ig_tags_url
# instapy
from instapy import InstaPy, smart_run


class InstagramBot:

    def __init__(self, username, 
                 cold_start=False, block=True, mini=True):
        """set username and start up a webdriver session

        inputs:
        > username (str)
            >> username of the account being used
            >> tied to the instance (self.username)
        > cold_start (bool)
            >> if True, don't start up webdriver
            >> default == False
        > block (bool)
            >> if True, block pop ups, else don't 
            >> default == True 
        > mini (bool)
            >> if True, minimize the browser window
            >> default == True
        """
        # remember start time
        self.start_time = time.time()
        # check username isn't blank
        if username == '':
            # let this person know they need to set their username
            raise Exception(f'username not found error\nusername = {username}\nplease set username in user.py')
        # set & greet user
        self.username = username
        print(f'\nwelcome back, {self.username}.')
        # start up webdriver? (default = yes)
        if not cold_start:
            # do we want to block pop-ups? (default = yes)
            if block == True:
                # disable push/popups 
                self.start_driver() 
            # we specified to not block popups
            else:
                # so start webdriver & don't block them 
                self.start_driver(block=False)
            # do we want to minimize the webdriver window? (default = yes)
            if mini:
                # minimize browser window
                self.driver.minimize_window()
        # cold start
        else:
            # so note that driver is not on
            self.driver_on = False
        # count # posts liked and # comments posted this sessison  
        self.n_posts_liked_this_session = 0
        self.n_comments_this_session = 0
        # count # posts gathered, # new posts and # previously seen posts this session 
        self.n_posts_gathered = 0
        self.n_new_posts = 0
        self.n_repeat_posts = 0

    def login(self, password):
        """loads and logs in to instagram

        inputs:
        > password (str)
            >> password to the account logging in
        """
        # check password isn't blank
        if password == '':
            # let this person know they need to set their password
            raise Exception(f'password not found error\npassword = {password}\nplease set password in user.py')
        # load instagram login page
        self.driver.get(ig_log_page)
        # wait (hedge load time)
        time.sleep(3)
        # log in 
        try:
            # find user box, type in account id
            self.driver.find_element_by_xpath(username_box).send_keys(self.username)
            # find key box and call locksmith, he should be able to punch in
            self.driver.find_element_by_xpath(password_box).send_keys(password, Keys.RETURN)
        # error
        except:
            # this one is big, so let us know & stop the program
            raise Exception(f'LOG IN ERROR\nunable to log in')
        # hedge request/load time 
        time.sleep(3)
        # take care if "save info" pop-up page pops up
        check_xpath(webdriver=self.driver, xpath=save_info_popup, click=True)

    def gather_posts(self, hashtag, 
                     scroll_range=5, 
                     limit=False, certify=True, r_log_on=True, 
                     route='data/made/post_hrefs/log', r_route='data/made/post_hrefs/r_log'):
        """collects group of post urls by hashtag

        inputs:
        > hashtag (str)
            >> hashtag from which to gather posts
        > scroll_range (int)
            >> how many times to scroll the hashtag page
                > note: more scrolls = more posts
                > default is 5 scrolls (a lot of posts)
        > limit (bool (False) when no limit, int when limit)
            >> maximum number of posts to consider 
                > does not affect scroll_range
                    >> if you have a limit, you may lower scroll_range to save time
                > limit is applied before certification of new posts {certify}
        > certify (bool)
            >> compare the post_hrefs found to post hrefs you've seen before {log}
                > drops posts which have been seen before
                > adds new ones to log 
                    > default recording location: 'data/made/post_hrefs/log'
                    > record info: first sighting of pulled hrefs + some info on time & hashtag found under
                > adds repeats to r_log if r_log_on == True 
            >> default == True
                > suggusted: turn off if you have no interest in keeping record
        > r_log_on (bool)
            >> record href, day, key, and hashtag for pulled hrefs that were already in log
                > default recording location: 'data/made/post_hrefs/r_log'
                > record info: multi-sighting hrefs + some info on time & hashtag found under (each time)
            >> dependent on certify (does not work if certify=False)
            >> default == True 
                > suggusted: turn off if no interest in keeping record or only want unique record {log}
        > route (str)
            >> route to log file
            >> default == 'data/made/post_hrefs/log'
        > r_route (str)
            >> route to r_log file
            >> default == 'data/made/post_hrefs/r_log'

        outputs:
        > post_hrefs (list)
            >> collection of urls to posts form hashtag 
        """
        # let us know what's going on
        print(f'\ncollecting posts from #{hashtag}')
        # determine day of week and key strings
        day = time.strftime("%A").lower()
        key = time.strftime("%Y%m%d_%H%M%S")
        # load the webpage to which the image belongs 
        self.driver.get(ig_tags_url + hashtag + '/')
        # hedge load time
        time.sleep(3)
        # set base collection for hrefs 
        post_hrefs = []
        # load n (scroll_range) scrolls of pictures
        for n in range(scroll_range):
            # this should work
            try:
                # it's almost like we're human
                self.driver.execute_script(scroll)
                # so pause and maybe they won't catch on
                time.sleep(2)
                # get page tags
                hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                # find relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # build list of unique photos
                [post_hrefs.append(href) for href in hrefs_in_view if href not in post_hrefs]
            # but just in case
            except:
                # let us know it didn't work, and which iteration 
                print(f'ERROR gathering photos on scroll #{n}')
                # and keep moving
                continue
        # let us know how many posts were collected
        print(f'{len(post_hrefs)} posts collected')
        time.sleep(1)
        # check for limit
        if limit != False:
            # check if we are over the limit
            if len(post_hrefs) > limit:
                # apply the limit 
                post_hrefs = post_hrefs[:limit]
                # let us know
                print(f'limit applied, # posts == {len(post_hrefs)}')
                time.sleep(1)
        # update total number of posts that have been gathered this session 
        self.n_posts_gathered += len(post_hrefs)
        # are we making sure these are unique? (default : yes)
        if certify:
            # let us know
            print('checking posts collected vs previously seen')
            time.sleep(1)
            # dataframe this hashtag's existing csv file 
            log = pd.read_csv(route)     
            # tag previously seen hrefs
            repeats = [href for href in post_hrefs if href in list(log.href)]
            # remove previously seen hrefs 
            post_hrefs = [href for href in post_hrefs if href not in repeats]
            # update counts of total new and previously seen posts for this session 
            self.n_new_posts += len(post_hrefs)
            self.n_repeat_posts += len(repeats)
            # let us know how many new and how many repeats there are
            print(f'posts checked, # new == {len(post_hrefs)}, # repeats == {len(repeats)}')
            time.sleep(1)
            # are we recording repeats? (default : yes)
            if r_log_on:
                # check that there are repeats to add to r_log
                if len(repeats) > 0:
                    # let us know what's happening
                    print(f'adding repeat posts to {r_route}')
                    time.sleep(1)
                    # read in repeat log
                    repeat_log = pd.read_csv(r_route)
                    # build dataframe
                    r_df = pd.DataFrame(repeats, columns=['href'])
                    # make lists for day of week, key, and tag columns
                    r_df['dow'] = (  (  (day + ',') * (len(r_df)-1) ) + day).split(',')
                    r_df['key'] = (  (  (key + ',') * (len(r_df)-1) ) + key).split(',')
                    r_df['tag'] = (((hashtag + ',') * (len(r_df)-1) ) + hashtag).split(',')    
                    # join and write the new repeat log
                    pd.concat([repeat_log, r_df], axis=0).to_csv(r_route, index=False) 
                # there are no repeat posts to add to r_log
                else:
                    # so let us know
                    print(f'no repeat posts to add to r_log, len(repeats) == {len(repeats)}')
        # not checking if the posts have been seen before or not 
        else:
            # so update counts of new and repeat posts to indicate these were not counted
            self.n_new_posts = 'not counted'
            self.n_repeat_posts = 'not counted'
        # check that there are posts to add to log
        if len(post_hrefs) > 0:
            # define dataframe of hrefs
            df = pd.DataFrame(post_hrefs, columns=['href'])
            # make lists for day of week and key columns
            df['dow'] = (  (  (day + ',') * (len(df)-1) ) + day).split(',')
            df['key'] = (  (  (key + ',') * (len(df)-1) ) + key).split(',')
            df['tag'] = (((hashtag + ',') * (len(df)-1) ) + hashtag).split(',')
            # add new dataframe to existing 
            df = pd.concat([log, df], axis=0)
            # let us know that we're about to record 
            print(f'adding new posts to {route}')
            time.sleep(1)
            # write the new dataframe over the old dataframe in csv (w/o index)
            df.to_csv(route, index=False)
        # there are no new posts to add to log
        else:
            # so let us know
            print(f'no new posts to add to log, len(post_hrefs) == {len(post_hrefs)}')
        # output collection of hrefs
        return post_hrefs        

    def like_posts(self, hashtag, hrefs, 
                   indicator_thresh=5):
        """load and 'like' posts from given list

        inputs:
        > hashtag (str)
            >> hashtag from which the posts have been collected
        > hrefs (list)
            >> list of posts (by url) to be liked
        > indicator_thresh (int)
            >> how many posts to process between printing progress 
        """
        # remember starting time
        now = time.time()
        # note how many posts there are 
        n_posts = len(hrefs)
        # tag how many posts we've liked this session 
        session_like_count = self.n_posts_liked_this_session 
        # let us know what's going on & provide ETA for how long it will take
        print(f'\nliking {n_posts} posts from #{hashtag}, ETA = {int(n_posts * 15.51)} seconds')
        # make a lambda function for clicking the like button
        like_button = lambda: self.driver.find_element_by_xpath(like).click()
        # go through each one
        for post_href in hrefs:
            # load the post
            self.driver.get(post_href)
            # hedge for whatever
            time.sleep(4)
            # move around a bit, make sure we can see the heart (like button)
            self.driver.execute_script(scroll)
            # this should work
            try:
                # click the like button (using the lambda function)
                like_button()
                # update number of posts liked this session 
                self.n_posts_liked_this_session += 1
                # hedge over-liking
                time.sleep(10)
            # but if it doesn't work
            except:
                # let us know
                print(f'ERROR: unable to like post at {post_href}')
                # and we don't really have a backup plan.. so just take a break i guess..
                time.sleep(2)
            # update count of remaining posts
            n_posts -= 1
            # check for asked indication
            if n_posts % indicator_thresh == 0:
                # let us know how many remain
                print(f'#{hashtag} : remaining = {n_posts}')
        # note ending time
        then = time.time()
        # output what just happened 
        print(f'liked {self.n_posts_liked_this_session - session_like_count} posts from #{hashtag} in {int(then-now)} seconds')
        print(f'{self.n_posts_liked_this_session} total posts liked this session')

    def comment(self, post, comment):
        '''load given post then comment given comment

        inputs:
        > post (str) 
            >> url to the post being commented on 
        > comment (str)
            >> comment to comment
        '''
        # pull up post 
        self.driver.get(post)
        # comment on the post
        try:
            # locate & click comment button
            self.driver.find_element_by_xpath(comment_button).click()
            # write out hashtags
            self.driver.find_element_by_xpath(comment_box).send_keys(comment, Keys.RETURN)
            # update the number of comments we've posted this session 
            self.n_comments_this_session += 1
            # let us know what happened
            print(f'\ncomment added to post\npost: {post}\ncomment: {comment}\n')
        # error
        except:
            # so let us know
            print(f'\nERROR commenting on {post}\n')
        # let us know how many comments we've posted this session 
        print(f'{self.n_comments_this_session} total comments this session')

    def close_window(self):
        """close the current window
        """
        self.driver.close()

    def quit_driver(self):
        """quit webdriver and close every associated window        
        """
        # check that driver is on 
        if self.driver_on == True:
            # quit webdriver
            self.driver.quit() 
            # set driver status to off
            self.driver_on = False
        # driver is not on
        else:
            # driver is not on, let the user know 
            print(f'\nDRIVER STATUS ERROR\n'
                  f'trying to run ig.quit_driver() but driver is not running\n'
                  f'self.driver_on == {self.driver_on}\nDRIVER STATUS ERROR\n')
            time.sleep(1)

    def start_driver(self, block=True):
        """start webdriver (gecko)
        inputs:
        > block (bool)
            > if True, blocks pop ups
            > default == True 
        """
        # tag the options field
        options = webdriver.FirefoxOptions()
        # do we want to block pop-ups? (default = yes)
        if block:
            # adjust options to disable push/popups 
            options.set_preference("dom.push.enabled", False)
        # start up driver w/ options (options do nothing if block=False)
        self.driver = webdriver.Firefox(options=options)
        # set webdriver status to on
        self.driver_on = True

    def shutdown(self):
        """
        quit webdriver (unless already quit) then shuts down InstagramBot

        use this: to end your scritps

        note: it is ok to run this even if driver is not running 
        """
        # check webdriver status
        if self.driver_on == True:
            # shut down webdriver & close all windows
            self.quit_driver()
            # switch driver status to off
            self.driver_on = False
        # define username line for final output
        user_out = f'user: {self.username}'
        # tag ending time
        self.end_time = time.time()
        # calculate runtime in minutes + seconds + 3 decimals
        gross_runtime = self.end_time - self.start_time
        split_runtime = str(gross_runtime).split('.')
        minutes =     int(float(split_runtime[0]) // 60)
        seconds = str(int(float(split_runtime[0]) % 60))
        runtime = minutes + float(seconds + '.' + split_runtime[1][:3])
        # set runtime line for final output 
        runtime_out = f'runtime: {runtime} seconds'
        # compare runtime line to username line to see which is longer
        if len(user_out) > len(runtime_out):
            num_stars = len(user_out)
        else:
            num_stars = len(runtime_out)
        # make boarder trim for final output = to whichever was longer
        stars = '*' * num_stars
        # add int minute and second sub output to runtime_out
        runtime_out = runtime_out + f'\n  {minutes} minutes\n  {seconds} seconds'
        # format session output into one long string 
        output = (f'''
                   {stars}
                   {stars}
                   session stats
                   {stars}
                   {user_out}
                   posts gathered: {self.n_posts_gathered}
                     new: {self.n_new_posts}
                     repeat: {self.n_repeat_posts}
                   posts liked: {self.n_posts_liked_this_session}
                   comments shared: {self.n_comments_this_session}
                   {runtime_out}
                   {stars}
                   {stars}
                   ''')
        # set session overview {ig.final_output} to output
        self.final_output = output

    def record(self, record, log):
        """record given info into given csv 

        inputs:
        > record
            >> information to be recorded
        > log
            >> csv file where information is to be recorded
        """
        # open up that redo log 
        with open(log, 'a') as f:
            # fit the writer
            writer = csv.writer(f)
            # document the information
            writer.writerow(record)
        
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
        ntract_following = check_xpath(webdriver=self.driver, xpath=following_button, click=True, hedge_load=5)
        # following button went well
        if ntract_following == 0:
            # wait a bit (hedge load)
            time.sleep(3)                    
            # test for/find and click the 'unfollow' button (0=success)
            ntract_unfollow = check_xpath(webdriver=self.driver, xpath=unfollow_button, click=True)
        # following buttion did not go well
        else:
            # unfollow no longer possible
            ntract_unfollow = 'nan'
        # output instance of unfollowing for log
        return [ntract_following, ntract_unfollow, datetime.now()]


    def check_xpath(self, xpath, webdriver, hedge_load=2,
                    click=False, send_keys=False, keys=None):
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
        time.sleep(hedge_load)
        # test this 
        try:
            # find xpath in question
            find_element = webdriver.find_element_by_xpath(xpath)
            # are we clicking
            if click == True:
                # yes, so click
                find_element.click()
                # hedge time
                time.sleep(3)
            # are we sending keys
            if send_keys == True:
                # yes, so send them
                find_element.send_keys(keys)
                # hedge time
                time.sleep(3)
            # element exists and was successfull
            return 0
        # if it didn't work
        except NoSuchElementException:
            # indicate as such
            return 1

    def record_followers_and_following(self, user, pwrd, account, **output_df):
        """
        > pull up a given account and record it's followers and following to csv
            >> then return that file path 
            >> optional output_df param
                > print file name & return the pandas dataframe
        """
        # set InstaPy session
        session = InstaPy(username=user, password=pwrd, headless_browser=True)
        # start the session
        with smart_run(session):
            # grab followers (list)
            followers = session.grab_followers(username=account, amount="full", 
                                            live_match=True, store_locally=False)
            # grab following (list)
            following = session.grab_following(username=account, amount="full", 
                                            live_match=True, store_locally=False)
        # merge for single list of all unique accounts in following/followers
        unique_accounts = list(set(followers + following))
        # make dataframe of all (unique) accounts
        df = pd.DataFrame(data=unique_accounts, columns=['account'])
        # make bool list of followers (1 == True)
        bool_followers = []
        for account in df['account']:
            # is follower
            if account in followers:
                bool_followers.append(1)
            # not follower
            else:
                bool_followers.append(0)
        # make bool list of following (1 == True)
        bool_following = []
        for account in df['account']:
            # are following
            if account in following:
                bool_following.append(1)
            # not following
            else:
                bool_following.append(0)
        # add bool columns to dataframe
        df['follower'] = bool_followers
        df['following'] = bool_following
        # id day of week 
        dow = time.strftime("%A_").lower()
        # numerical year, month, day _ hour, minute, second
        ymdhms = time.strftime("%Y%m%d_%H%M%S")
        # generate file name
        file = 'data/made/followers_and_following/' + dow + ymdhms + '.csv'
        # record dataframe as csv
        df.to_csv(path_or_buf=file, index=False)
        # did we request the dataframe?
        if output_df:
            # display file name
            print(f'{file}')
            # output dataframe for further use
            return df
        # output file name
        return file

    def check_non_followbackers(self, ref='ask'):
        """
        > compare followers and following from given csv 
            >> to identify non-followbackers
        > print out findings
        > ask if the user would like to unfollow any found non-followbackers
            >> limit 24 per session (rec max 99 / day)
        """
        # check there's a file loaded
        if ref == 'ask':
            # ask for reference file
            ref = input('csv to run: ')
        # load data into frame
        df = pd.read_csv(ref)
        # tag followers & following 
        followers = df.account.loc[df.follower == 1]
        following = df.account.loc[df.following == 1]
        # identify accounts our account is following that are followers of our account
        follow_backers = df.account.loc[((df.follower == 1) & (df.following == 1))]
        # identify accounts our account is following that are NOT followers of our account
        non_follow_backers = df.account.loc[((df.follower == 0) & (df.following == 1))]
        # display number of follow backers and number of non follow backers
        print(f'\n{len(followers)} followers\n'
            f'{len(following)} following\n'
            f'{len(follow_backers)} follow backers\n'
            f'{len(non_follow_backers)} non-follow backers\n')
        time.sleep(2)
        # output non-followbackers
        return non_follow_backers

    def unfollow(self, pwrd, accounts_to_unfollow='live', ref='ask'):
        """
        still in experimental mode
        """
        # make sure there is not a session going
        if self.driver_on:
            raise Exception('WebDriver must be shutdown before using unfollow method.')
        # the only current option is to do this live
        accounts_to_unfollow='live'
        # so make sure to set a ref for checking for nonfollowbackers
        if accounts_to_unfollow == 'live':
            non_follow_backers = self.check_non_followbackers(ref=ref)
        # are there accounts worthy of unfollowing? 
        if len(non_follow_backers) > 0:
            # ask user opinion
            to_unfollow = input('would you like to unfollow any non-follow backers (y/n)? ')
            # proceed with unfollowing
            if to_unfollow == 'y':
                # determine how many accounts to unfollow
                n_unfollow = int(input('how many would you like to unfollow (int <= 24)? '))
                # set a cap (limit number of unfollows per session)
                cap = 24
                # is desired number of unfollow more than max amount allowed per session (cap)?
                if n_unfollow > cap:
                    # output warning, action and times to read 
                    print(f'\nWARNING: MAX UNFOLLOWS EXCEEDED\nmax n_unfollow = {cap}\n')
                    time.sleep(1)
                    print(f'resetting n_unfollow from {n_unfollow} to {cap}\n\n')
                    time.sleep(1)
                    # enforce cap
                    n_unfollow = cap
                # cut down to accounts to unfollow
                accounts_to_unfollow = list(non_follow_backers[:n_unfollow])
                # give us the accounts to unfollow
                return accounts_to_unfollow
            # not unfollowing anyone
            else:
                print('ok, cool.')
                # output non-followbackers
                return non_follow_backers
        # nobody to unfollow
        else:
            # indicate so 
            print(f'nobody to unfollow\nlen(non_follow_backers) == {len(non_follow_backers)}')
        # make a session 
        session = InstaPy(username=self.username, password=pwrd, headless_browser=True)
        # start the session 
        with smart_run(session):
            # unfollow those accounts
            session.unfollow_users(amount=n_unfollow, custom_list_enabled=True,
                                   custom_list=accounts_to_unfollow, custom_list_param="all",
                                   instapy_followed_enabled=False, instapy_followed_param="all",
                                   nonFollowers=False, allFollowing=False,
                                   style="FIFO", unfollow_after=None,
                                   sleep_delay=600, delay_followbackers=0) # 864000 = 10 days, 0 = don't delay
        # indicate completion
        print(f'session complete\n {len(non_follow_backers)-n_unfollow} non-followbackers remain')
        # output accounts we unfollowed
        return accounts_to_unfollow
