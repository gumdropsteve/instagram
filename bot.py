from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import sys

# plugins, base urls, and paths
instagram = 'https://www.instagram.com/'
ig_login_button = '//a[@href="/accounts/login/?source=auth_switcher"]'
username_box = '//input[@name="username"]'
password_box = '//input[@name="password"]'
instagram_tags_url = 'https://www.instagram.com/explore/tags/'
scroll = "window.scrollTo(0, document.body.scrollHeight);"
like = '//span[@aria-label="Like"]'
tags = ['pleasanton', 'californialife', 'californiaadventure', 'homesforsale', 'fsbo', 'californiarealestate', 'pleasantonhomesforsale', 'bayarearealestate', 'forsalebyowner']


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username, password):
        options = webdriver.FirefoxOptions()  
        options.set_preference("dom.push.enabled", False)  
        '''
        options allows the blocking of popups 
        this is not required for this script as it is currently written
        may become necessary in future editions
        to disable, change (options=options) to ()
        '''
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox(options=options)

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get(instagram)
        sleep(2)
        login_button = driver.find_element_by_xpath(ig_login_button)
        login_button.click()
        sleep(2)
        user_name_elem = driver.find_element_by_xpath(username_box)
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath(password_box)
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        sleep(2)

    def like_photo(self, hashtag):
        driver = self.driver
        driver.get(instagram_tags_url + hashtag + '/')
        sleep(2)

        # gathering photos
        pic_hrefs = []
        for _ in range(7):
            try:
                driver.execute_script(scroll)
                sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except:
                print('except Exception: # gathering photos')
                continue

        # liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            sleep(2)
            driver.execute_script(scroll)
            try:
                sleep(random.randint(2, 4))
                like_button = lambda: driver.find_element_by_xpath(like).click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    sleep(1)
            except:
                sleep(2)
            unique_photos -= 1
            print(unique_photos)

if __name__ == "__main__":

    user_id = ''  # your username 
    pword = ''  # your password

    ig = InstagramBot(user_id, pword)
    ig.login()

    # insert your desired hashtags here (list)
    hashtags = tags

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            ig.like_photo(tag)
        except Exception:
            ig.closeBrowser()
            sleep(61)
            ig = InstagramBot(user_id, pword)
ig.login()
