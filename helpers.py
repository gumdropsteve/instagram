from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  


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
        # element was found, step 1 complete
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
    # if it didn't work
    except NoSuchElementException:
        print(f'NoSuchElementException : {xpath}')
    pass
