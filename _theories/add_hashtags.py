from time import sleep
from selenium import webdriver

'''
log in
    load most recent post (of own account)
        add comment of hashtags
            close
                remove firefox thing from dock (annoying and needed across all)
'''

def add_hashtags(self, post, hashtags):
    # pull up post 
    self.driver.get(post)
    # locate & click comment button
    # self.driver.find_element_by_....click()
    # write out hashtags
    # self.driver.find_element_by_....send_keys(post)
    # find button & submit comment
    # self.driver.find_element_by_....click()
