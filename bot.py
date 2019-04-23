from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import sys
# loading login info (adjust to import yours or take this line out and input near bottom)
from _pile import utv, ptv

# plugins, base urls, and paths
instagram = 'https://www.instagram.com/'
ig_login_button = '//a[@href="/accounts/login/?source=auth_switcher"]'
username_box = '//input[@name="username"]'
password_box = '//input[@name="password"]'
instagram_tags_url = 'https://www.instagram.com/explore/tags/'
scroll = "window.scrollTo(0, document.body.scrollHeight);"
like = '//span[@aria-label="Like"]'
tags = ['pleasanton', 'californialife', 'californiaadventure', 'homesforsale', 'fsbo', 'californiarealestate', 'pleasantonhomesforsale', 'bayarearealestate', 'forsalebyowner']


'''def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()'''  # concept 


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
        # driver load instagram.com
        driver.get(instagram)
        # wait (hedge load time)
        sleep(2)
        # find and tag the login button
        login_button = driver.find_element_by_xpath(ig_login_button)
        # click to login
        login_button.click()
        # wait (hedge load time)
        sleep(2)
        # find and tag user box
        user_name_elem = driver.find_element_by_xpath(username_box)
        # get rid of anything that for whatever reason may be in there
        user_name_elem.clear()
        # input email, ussername, or phone
        user_name_elem.send_keys(self.username)
        # find and tag pwrd box
        passworword_elem = driver.find_element_by_xpath(password_box)
        # get rid of anything that for whatever reason may be in there
        passworword_elem.clear()
        # input pwrd
        passworword_elem.send_keys(self.password)
        # enter it (log in)
        passworword_elem.send_keys(Keys.RETURN)
        # and wait a bit for safety 
        sleep(2)

    def like_photo(self, hashtag):
        # set driver
        driver = self.driver
        # load the webpage to which the image belongs 
        driver.get(instagram_tags_url + hashtag + '/')
        # better safe than sorry
        sleep(2)

        '''gather a nice collection of posts'''
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

        '''actually liking the posts'''
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
            
#     def unfollow(self, profile_url):
        

# make this a runable script 
if __name__ == "__main__":
    '''
    change user_id and pword to strings reflecting your login info
    current seen here are stored in a seperate file to hedge uploading 
    '''
    
    # your username 
    user_id = utv  # ''  
    # your password
    pword = ptv  # ''  

    # label the bot
    ig = InstagramBot(user_id, pword)
    # get the party started 
    ig.login()

    # insert your desired hashtags here (list)
    hashtags = tags

    while True:
        # this should work until all tags have been used
        try:
            # choose a random tag from the list of tags
            tag = random.choice(hashtags)
            # like the posts under that tag
            ig.like_photo(tag)
        # if it doesn't, or (hopefully) we're done
        except Exception:
            # close her down
            ig.closeBrowser()
            # take a break 
            sleep(61)
            # retry the bot 
            ig = InstagramBot(user_id, pword)
ig.login()
