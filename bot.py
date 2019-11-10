# timing 
import time
from time import sleep
# reading
import numpy as np
import pandas as pd
# recording
import csv
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

    def __init__(self, username, block=True):
        # set & greet user
        self.username = username
        print(f'hello, {self.username}.')
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
        # minimize browser window
        self.driver.minimize_window()

    def login(self, password):
        """loads and logs in to instagram
        """
        # load instagram login page
        self.driver.get(ig_log_page)
        # wait (hedge load time)
        sleep(3)
        # find user box, type in account id
        self.driver.find_element_by_xpath(username_box).send_keys(self.username)
        # find key box and call locksmith, he should be able to punch in
        self.driver.find_element_by_xpath(password_box).send_keys(password, Keys.RETURN)
        # hedge request/load time 
        sleep(3)
        # take care if "save info" pop-up page pops up
        check_xpath(webdriver=self.driver, xpath=save_info_popup, click=True)

    def gather_posts(self, hashtag, scroll_range=5, 
                     limit=False, certify=True, r_log_on=True):
        """collects group of post urls by hashtag

        inputs) 
        > hashtag 
            >> hashtag from which to gather posts
        > scroll_range
            >> how many times to scroll the hashtag page
                > note: more scrolls = more posts
                > default is 5 scrolls (a lot of posts)
        > limit
            >> maximum number of posts to consider 
                > does not affect scroll_range
                    >> if you have a limit, you may lower scroll_range to save time
                > limit is applied before certification of new posts {certify}
        > certify
            >> compare the post_hrefs found to post hrefs you've seen before {log}
                > drops posts which have been seen before
                > adds new ones to log (r_log_on option)
        > r_log_on
            >> record href, day, key, and hashtag for pulled hrefs that were already in log
            >> dependent on certify (does not work if certify=False)

        output)
        > post_hrefs
            >> collection of urls to posts form hashtag 
        > log (optional)
            >> record of seen hrefs and some info on time & hashtag found under
            >> default: it's on, suggusted: turn off if you have no interest in keeping record
        > r_log (optional)
                > "repeat log"
            >> record of multi-sighting hrefs and some info on time & hashtag found under (each time)
            >> default: it's on, suggusted: turn off if no interest in keeping record or only want unique record {log}
        """
        # determine day of week and key strings
        day = time.strftime("%A").lower()
        key = time.strftime("%Y%m%d_%H%M%S")
        # load the webpage to which the image belongs 
        self.driver.get(ig_tags_url + hashtag + '/')
        # hedge load time
        sleep(3)
        # set base collection for hrefs 
        post_hrefs = []
        # load n (scroll_range) scrolls of pictures
        for n in range(scroll_range):
            # this should work
            try:
                # it's almost like we're human
                self.driver.execute_script(scroll)
                # so pause and maybe they won't catch on
                sleep(2)
                # get page tags
                hrefs_in_view = self.driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [post_hrefs.append(href) for href in hrefs_in_view if href not in post_hrefs]
                # so as not to spam
                if n % 2 != 0:
                    # display length of list to user
                    print("Check: pic href length " + str(len(post_hrefs)))
            # but just in case
            except:
                # let us know it didn't work, and which iteration 
                print(f"except Exception: #{n} gathering photos")
                # and keep moving
                continue
        # check for limit
        if limit != False:
            # check if we are over the limit
            if len(post_hrefs) > limit:
                # apply the limit 
                post_hrefs = post_hrefs[:limit]
        # identify log route
        route = 'data/made/post_hrefs/log'
        # dataframe this hashtag's existing csv file 
        log = pd.read_csv(route)     
        # are we making sure these are unique? (default : yes)
        if certify:
            # tag previously seen hrefs
            repeats = [href for href in post_hrefs if href in list(log.href)]
            # remove previously seen hrefs 
            post_hrefs = [href for href in post_hrefs if href not in repeats]
            # are we recording repeats? (default : yes)
            if r_log_on:
                # tag repeat log route
                r_route = 'data/made/post_hrefs/r_log'
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
        # define dataframe of hrefs
        df = pd.DataFrame(post_hrefs, columns=['href'])
        # make lists for day of week and key columns
        df['dow'] = (  (  (day + ',') * (len(df)-1) ) + day).split(',')
        df['key'] = (  (  (key + ',') * (len(df)-1) ) + key).split(',')
        df['tag'] = (((hashtag + ',') * (len(df)-1) ) + hashtag).split(',')
        # add new dataframe to existing 
        df = pd.concat([log, df], axis=0)
        # write the new dataframe over the old dataframe in csv (w/o index)
        df.to_csv(route, index=False)
        # output collection of hrefs
        return post_hrefs        

    def like_posts(self, hashtag, hrefs, indicator_thresh=5):
        """load and 'like' posts from given list

        input)
        > hashtag
            >> hashtag from which the posts have been collected
        > hrefs
            >> list of posts (by url) to be liked
        > indicator_thresh
            >> how many posts to process between printing progress 
        """
        # note how many posts there are 
        n_unique_posts = len(hrefs)
        # go through each one
        for post_href in hrefs:
            # load the post
            self.driver.get(post_href)
            # hedge for whatever
            sleep(5)
            # move around a bit, make sure we can see the heart (like button)
            self.driver.execute_script(scroll)
            # this should work
            try:
                # find the like button 
                like_button = lambda: self.driver.find_element_by_xpath(like).click()
                # click the like button
                like_button().click()
                # hedge over-liking
                sleep(10)
            # if it doesn't work
            except:
                # don't really have a backup plan.. so take a break ig..
                sleep(2)
            # update count of remaining posts
            n_unique_posts -= 1
            # check for asked indication
            if n_unique_posts % indicator_thresh == 0:
                # let us know how many remain
                print(f'#{hashtag} : remaining = {n_unique_posts}')

    def comment(self, post, comment):
        '''load given post then comment given comment
        '''
        # pull up post 
        self.driver.get(post)
        # locate & click comment button
        self.driver.find_element_by_xpath(comment_button).click()
        # write out hashtags
        self.driver.find_element_by_xpath(comment_box).send_keys(comment, Keys.RETURN)
        # let us know what happened
        print(f'\ncomment added to post\npost: {post}\ncomment: {comment}\n')

    def close_browser(self):
        """closes webdriver
        """
        self.driver.close()  
 
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
