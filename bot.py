from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
import sys


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username, password):
        options = webdriver.FirefoxOptions()  # (seems to) initiate(s) webdriver.Firefox() once referenced 
        options.set_preference("dom.push.enabled", False)  # blocks popups 
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox(options=options)

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        sleep(2)
        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        sleep(2)

    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        sleep(2)

        # gathering photos
        pic_hrefs = []
        for _ in range(7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                sleep(random.randint(2, 4))
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    sleep(1)
            except:
                sleep(2)
            unique_photos -= 1

if __name__ == "__main__":

    username = ''  # your username 
    password = ''  # your password

    ig = InstagramBot(username, password)
    ig.login()

    # insert your desired hashtags here (list)
    hashtags = ['codnation', 'callofduty', 'cwl', 'twitch', 'blackout', 'killcam', 'codclips', 
                'blackops', 'freeforall', 'twitchclips', 'blackoutgame', 'xbox', 'ps4',
                'battleroyale', 'gamingmemes', 'bo4', 'blackops4', 'callofdutyblackops4']

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            ig.like_photo(tag)
        except Exception:
            ig.closeBrowser()
            sleep(61)
            ig = InstagramBot(username, password)
ig.login()
