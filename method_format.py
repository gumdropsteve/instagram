"""purpose: define standard format method (general; all) of class (InstagramBot) 
how: redefine specific method (.unfollow()) of class (InstagramBot)
specifics: break down current .unfollow() into its generalizable components; 
build generalized method of each generalizable component, 
replace current .unfollow() in InstagramBot with new methods
"""

def generate_actionable_uls(self, potential_accounts, n, white_list_accounts):
    """identify accounts elgible for action from pd dataframe via 
    compairson to dataframe of non/previously-actionable accounts

    inputs:
    > potential_accounts
        >> pandas dataframe of accounts up for action
            > with account urls in .user_profile column
    > n
        >> number of accounts on which action will be taken in this round
    > white_list_accounts
        >> pandas dataframe of accounts which have already been acted upon
            > with account urls in .user_profile column

    output:
    > list of urls belonging to potential_accounts not found in white_list_accounts
    """
    # pull/tag potential urls 
    potential_urls = [url for url in potential_accounts.user_profile]
    # pull/tag previously seen urls
    already_actioned = [url for url in white_list_accounts.user_profile]
    # forget already actioned urls
    elgible_urls = [url for url in potential_urls if url not in already_actioned]
    # range matters
    if n != False:
        # shrink numer of accounts to desired range
        elgible_urls = elgible_urls[:n]
    # output actionable accounts
    return elgible_urls

def unfollow(self, account_url):
    """unfollow given account 

    inputs:
    > account_url
        >> url of account to unfollow

    output:
    > list detailing transaction
        >> check/click 'following', check/click 'unfollowing', datetime
    """
    # load the account's profile
    self.driver.get(account_url) 
    # test for/find and click the 'following' button (0=success)
    ntract_following = check_xpath(webdriver=self.driver, 
                                xpath=following_button, 
                                click=True,
                                hedge_load=5)
    # following button went well
    if ntract_followng == 0:
        # wait a bit (hedge load)
        sleep(3)                    
        # test for/find and click the 'unfollow' button (0=success)
        ntract_unfollow = check_xpath(webdriver=self.driver, 
                                    xpath=unfollow_button, 
                                    click=True)
    # following buttion did not go well
    else:
        # unfollow no longer possible
        ntract_unfollow = 'nan'
    # output instance of unfollowing for log
    return list(ntract_following, ntract_unfollow, datetime.datetime.now())

def record_recents(self, recents, record_log):
    """record given info into csv log 

    inputs:
    > recents
        >> information (from recent transactions) to be recorded
    > record_log
        >> csv file where information is to be recorded
    """
    # open up that redo log 
    with open(record_log, 'a') as f:
        # fit the writer
        writer = csv.writer(f)
        # go though each information point 
        for transaction in recents:
            # document the information
            writer.writerow(transaction)



"""origional method
"""
def unfollow(self, start=0, end=250, verification=True, record_thresh=10, speed=1):
    '''start generating actionable accounts'''
    # pull urls 
    potential_urls = [url for url in verified_unfollow_log.user_profile]
    # pull previously redone 
    already_redone = unfollow_log
    # tag previously redone urls
    redone_urls = [url for url in already_redone.user_profile]
    # forget redone urls
    urls_not_redone = [url for url in potential_urls if url not in redone_urls]
    # shrink to range
    urls_to_redo = urls_not_redone[start:end]
    # start log for multi account writing
    log = []
    # start count of number of accounts unfollowed
    redone_count = 0
    # start log for re-unfollowed check
    re_unfollowed = []
    '''end generating actionable accounts'''
    '''start going through actionable accounts'''
    # go through each url to redo
    for n in range(len(urls_to_redo)):
        '''start specific account'''
        # focus this url
        url = urls_to_redo[n]
        # locate account
        account = verified_unfollow_log.loc[verified_unfollow_log.user_profile == url]
        # label account info 
        info = [i for column in account.values for i in column]
        # account was actually unfollowed
        if info[6] == 0:
            # make n/a values
            na = ['n/a','n/a',datetime.datetime.now()]
            # go through na values
            for _ in na:
                # add n/a values
                info.append(_)
            # add the account to temp log
            log.append(info)
            # did not unfollow or load page, minimal time off 
            sleep(1 * (1/speed))
        # account was not actually unfollowed
        elif info[6] == 1:
            # load that url
            self.driver.get(url)      
            # wait for profile to load
            sleep(5)
            # test for/find and click the 'following' button (0=success)
            ntract_following = check_xpath(webdriver=self.driver, xpath=following_button, click=True)
            # add to account log
            info.append(ntract_following)
            # wait a bit (hedge load)
            sleep(3)                    
            # test for/find and click the 'unfollow' button (0=success)
            ntract_unfollow = check_xpath(webdriver=self.driver, xpath=unfollow_button, 
                                            click=True, send_keys=False, keys=None)
            # add to account log
            info.append(ntract_unfollow)
            # note time
            time_redone = datetime.datetime.now()
            # add to unfollow count
            redone_count += 1
            # add time account log
            info.append(time_redone)
            # add this account to log
            log.append(info)
            # note instance 
            re_unfollowed.append(url)
            '''end specific account'''
            '''start wait times / verification of recent unfollowing'''
            # this isn't a 5th unfollow
            if redone_count % 5 != 0:
                # take some time off so we hopefully don't get blocked 
                sleep(30 * (1/speed))
            
            # unfollow verification (for nth unfollowing) 
            elif redone_count % 5 == 0:
                # hyper verification?
                if verification == 'hyper':
                    # tag 1st from this set of 5
                    first = re_unfollowed[0]
                    # load first unfollow
                    self.driver.get(first)
                    # wait for load
                    sleep(5)
                    # check for 'Following' button 
                    fing_button = check_xpath(webdriver=self.driver, xpath=following_button, click=True)
                    # it exists; we did not unfollow 
                    if fing_button == 0:
                        # halt progress; we are probably blocked
                        raise Exception(f"fing_button == {fing_button} ;\naccount == {middle}\n\nrecent unfollows == {re_unfollowed}")
                    # it does not exist; we unfollowed
                    else:
                        # some sort of glitch
                        if fing_button != 1:
                            # so that's noteworthy
                            raise Exception(f'fing_button != 1 ;\nfing_button == {fing_button} ;\naccount == {middle}')
                        # otherwise, good; so let us know
                        print(f'5th test == pass')
                        # reset temp unfollowed log
                        re_unfollowed = []
                    # and break normally
                    sleep(30 * (1/speed))
                # the (defined) usual
                elif verification == True:
                    # normal verification
                    if redone_count % 25 == 0:
                        # tag middle unfollow for this set
                        middle = re_unfollowed[12]
                        # load middle unfollow 
                        self.driver.get(middle) 
                        # wait for load
                        sleep(5)
                        # check for 'Following' button 
                        fing_button = check_xpath(webdriver=self.driver, xpath=following_button, click=True)
                        # it exists; we did not unfollow 
                        if fing_button == 0:
                            # halt progress; we are probably blocked
                            raise Exception(f"fing_button == {fing_button} ;\naccount == {middle}\n\nrecent unfollows == {re_unfollowed}")
                        # it does not exist; we unfollowed
                        else:
                            # some sort of glitch
                            if fing_button != 1:
                                # so that's noteworthy
                                raise Exception(f'fing_button != 1 ;\nfing_button == {fing_button} ;\naccount == {middle}')
                            # otherwise, good; so let us know
                            print(f'25th test == pass')
                            # reset temp unfollowed log
                            re_unfollowed = []
                    # break normally
                    sleep(30 * (1/speed))
                # no verification 
                elif verification == False:
                    # ok, but every once in a while
                    if redone_count % 25 == 0:
                        # remind us
                        print(f"verification == {verification}")
                    # and don't forget break
                    sleep(30 * (1/speed))
                # unknown verification
                else:
                    # let us know
                    print(f"\nERROR ; non-fatal ERROR ; verification method unknown ; verification == {verification}\n")
                # it's a 500th
                if redone_count % 500 == 0:
                    # let us know
                    print(f'\nredone_count == {redone_count}   >> taking an extra 10 minutes\n')
                    # take extra break 
                    sleep(60*10)
                # it's a 100th 
                elif redone_count % 100 == 0:
                    # let us know
                    print(f'\nredone_count == {redone_count}   >> taking an extra 5 minutes\n')
                    # take extra break 
                    sleep(60*5)
                # it's a 50th
                elif redone_count % 50 == 0:
                    # let us know
                    print(f'\nredone_count == {redone_count}   >> taking an extra minute\n')
                    # take extra break 
                    sleep(60)
                '''end wait times / verification of recent unfollowing'''
            # idk (would be unexpected)
            else:
                # so indicate
                raise Exception(f"redone_count == {redone_count}")
        # this would be unexpected
        else:
            # so make it known
            raise Exception(f'info[6] == {info[6]}')
        '''start recording to csv'''
        # this is a nth iteration (or we're almost done)
        if n % record_thresh == 0 or len(urls_to_redo) - n < 2:
            # open up that redo log 
            with open('data/made/redone_accounts_ttvpa_used_to_follow.csv', 'a') as _f:
                # fit the writer
                writer = csv.writer(_f)
                # go though each account 
                for info in log:
                    # document the transaction
                    writer.writerow(info)
                # reset temp log
                log = []
        '''end recording to csv'''
        '''start user display'''
        # on first loop
        if n == 0:
            # lay out the situation 
            print(f'up and running ; {len(urls_to_redo)-1} to go ; {datetime.datetime.now()}')

        # every 25th loop
        elif n % 25 == 0:
            # are we on a 50th
            if n % 50 == 0:
                # display raw number completion
                print(f'{n}/{len(urls_to_redo)} complete ; {datetime.datetime.now()}')
            # or just a quarter
            else:
                # display percentage completion
                print(f'{int(100*(n/len(urls_to_redo)))}% complete ; {datetime.datetime.now()}')     
        '''end user display'''
