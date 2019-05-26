import pandas as pd
from time import sleep
from datetime import datetime
# selenium 2.0
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
# data
from infos import unfollow_log, following_button, verified_unfollow_log
# helper functions (possibly where this will end up)
from helpers import check_xpath


def verify_unfollow(webdriver, log=unfollow_log, prior=verified_unfollow_log):
    """takes list of accounts that have been 'unfollowed' in unfollow_log
    visits each profile, checks for existance of 'Following' button
    if 'Following' button exists, account was obviously not unfollowed
    rewrites unfollow_log with new 'actually_unfollowed' and 'time_checked' columns

    inputs)
        > webdirver
            >> driver in use
        > log 
            >> log of accounts which have been run through bot.py 
                > default = unfollow_log
        > prior 
            >> accounts which have gone through verification process
                > default = verified_unfollow_log
    """
    # set out route
    out = []
    # id urls verified
    verified_urls = [url for url in prior.user_profile]
    # focus & trim log urls
    url_log = [url for url in log.user_profile if url not in verified_urls]
    # go through each
    for _ in range(len(url_log[:5])):
        # tag that url
        url = url_log[_]
        # pull that account's info in log & make into a list of unique values
        this_user = [datapoint for list in log.loc[log.user_profile == url].values 
                     for datapoint in list]
        # load the url in question
        webdriver.get(url)
        sleep(2)
        # check for 'Following' button
        check = check_xpath(webdriver, xpath=following_button, 
                            click=False, send_keys=False, keys=None)
        # does it exist?
        if check == 0:
            # never actually unfollowed 
            this_user.append(1)
        # does it not exist?
        elif check == 1:
            # ok, so we unfollowed
            this_user.append(0)
        # and note the time
        this_user.append(datetime.now())
        # to the ranch!
        out.append(this_user)
    # that's a wrap
    webdriver.close()
    # tag columns
    cols = [column for column in log.columns.values]
    # add column for if the account is still followed
    cols.append('actually_unfollowed')
    # add column for time 
    cols.append('time_checked_au')
    # make dataframe
    df=pd.DataFrame(data=out,columns=cols)
    df.to_csv('test.csv',index=False)
    # output dataframe
    return df

# lets do it
if __name__=='__main__':
    # imports
    from selenium import webdriver
    # tag the options field
    options = webdriver.FirefoxOptions()  
    # disable push/popups 
    options.set_preference("dom.push.enabled", False) 
    # set driver 
    driver=webdriver.Firefox(options=options)
    # test method
    print(verify_unfollow(webdriver=driver))
