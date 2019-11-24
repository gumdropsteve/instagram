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
# .js help
from infos import scroll
# functions
from helpers import check_xpath
# urls
from infos import ig_log_page, ig_tags_url
# paths
from infos import username_box, password_box, save_info_popup
from infos import comment_button, comment_box, like
# misc
from infos import ig_tags_url


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
        # check username isn't blank
        if username == '':
            # let this person know they need to set their username
            raise Exception(f'username not found error\nusername = {username}\nplease set username in user.py')
        # set & greet user
        self.username = username
        print(f'\nhello, {self.username}.\n')
        # start up webdriver? (default = yes)
        if not cold_start:
            # tag the options field
            options = webdriver.FirefoxOptions()  
            # do we want to block pop-ups? (default = yes)
            if block:
                # disable push/popups 
                options.set_preference("dom.push.enabled", False)  
            # set driver with options 
            self.driver = webdriver.Firefox(options=options)
            # do we want to minimize the webdriver window? (default = yes)
            if mini:
                # minimize browser window
                self.driver.minimize_window()
        # start counters for # posts liked and # comments posted this sessison  
        self.n_posts_liked_this_session = 0
        self.n_comments_this_session = 0

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
        # let us know what's going on 
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
        """closes the current window
        """
        self.driver.close()

    def quit_driver(self):
        """quits webdriver and closes every associated window
        
        use this: at the end of your script
        """
        self.driver.quit() 

    def start_driver(self, block=True):
        """starts webdriver (gecko)
        
        inputs:
        > block (bool)
            > if True, blocks pop ups
            > default == True 
        """
        # do we want to block pop-ups? (default = yes)
        if block:
            # tag the options field
            options = webdriver.FirefoxOptions()  
            # disable push/popups 
            options.set_preference("dom.push.enabled", False)  
            # set driver with options 
            self.driver = webdriver.Firefox(options=options)
        # we do not want to block pop ups. 
        else:
            self.driver = webdriver.Firefox()

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
