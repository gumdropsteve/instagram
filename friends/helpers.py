from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
# from infos import ig_not_available

"""to add
detect if page is 404
    by text? 
recording info on the visuals
    what is the account broadcasting?
        rip sullivan --classic
    this may be better in bot?
        no? what is point of helpers?
            maybe.
"""

def check_xpath(webdriver, xpath, click=False, send_keys=False, keys=None):
    """
    checks if an xpath exists on the current page

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
    """
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
        # run 404 test
        # test_404 = ig_broken_page(webdriver=webdriver)
        # return 404 if 404 or 1 if not 404
        # return test_404
        return 1


# def ig_broken_page(webdriver, xpath=ig_not_available):
#     """
#     determines if the current page is an instagram 404 or not

#     inputs)
#     > webdriver
#         >> driver being used
#     > xpath
#         >> xpath in question
#             > default is to text on Instagram's 404 page
#     """
#     # test this 
#     try:
#         # find xpath in question
#         driver.find_element_by_xpath(xpath)
#         # indicate successful find
#         return 404
#     # if it didn't work
#     except:
#         # indicate failure to find
#         return 1


# if __name__ == '__main__':
#     from selenium import webdriver
#     # tag the options field
#     options = webdriver.FirefoxOptions()  
#     # disable push/popups 
#     options.set_preference("dom.push.enabled", False)  
#     # set driver
#     driver=webdriver.Firefox(options=options)
#     # get 404 page
#     driver.get('https://www.instagram.com/nolegacyyyleft/')
#     from time import sleep
#     sleep(3)
#     # test check 404 (should be 404)
#     a=ig_broken_page(webdriver=driver)
#     # test check 404 in check_xpath (should be 404)
#     b=check_xpath(webdriver=driver, xpath='nonsense', click=False, send_keys=False, keys=None)
#     # get non-404 page
#     driver.get('https://www.instagram.com/nolegacyleft/')
#     sleep(3)
#     # test 404 check (should be 1)
#     c=ig_broken_page(webdriver=driver)
#     # check test 404 check in check_xpath (should be 1)
#     d=check_xpath(webdriver=driver, xpath='nonsense', click=False, send_keys=False, keys=None)
#     # close
#     driver.quit()
#     # expect: 404,404,1,1
#     print(a,b,c,d)


