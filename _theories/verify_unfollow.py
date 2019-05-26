
def verify_unfollow(self, log=unfollow_log, prior=verified_unfollow_log, 
                    start=0, end=250):
    """takes list of accounts that have been 'unfollowed' in unfollow_log
    visits each profile, checks for existance of 'Following' button
    if 'Following' button exists, account was obviously not unfollowed
    rewrites unfollow_log with new 'actually_unfollowed' and 'time_checked' columns
        to verified_accounts_ttvpa_used_to_follow.csv

    inputs)
        > webdirver
            >> driver in use
        > log 
            >> log of accounts which have been run through bot.py 
                > default = unfollow_log
        > prior 
            >> accounts which have gone through verification process
                > default = verified_unfollow_log
        > start
            >> first instance to consider
        > end
            >> last instance to consider
    """
    # set out route
    out = []
    # id urls verified
    verified_urls = [url for url in prior.user_profile]
    # focus & trim log urls
    url_log = [url for url in log.user_profile if url not in verified_urls]
    # go through each
    for _ in range(len(url_log)):
        # tag that url
        url = url_log[_]
        # pull that account's info in log & make into a list of unique values
        this_user = [datapoint for list in log.loc[log.user_profile == url].values 
                     for datapoint in list]
        # load the url in question
        self.driver.get(url)
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
        this_user.append(datetime.datetime.now())
        # to the ranch!
        out.append(this_user)
    '''record the transaction
    '''
    # open up the csv
    with open('data/made/verified_accounts_ttvpa_used_to_follow.csv', 'a') as _f:
        # fit the writer
        writer = csv.writer(_f)
        # each out is an account
        for user in out:
            # document the transaction
            writer.writerow(user)
