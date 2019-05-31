#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urllib.request
import urllib.parse
import urllib.error
from bs4 import BeautifulSoup
import ssl
import json
from time import sleep
import pandas as pd
import csv
from datetime import datetime


class Insta_Info_Scraper:

    def getinfo(self, url):
        html = urllib.request.urlopen(url, context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('meta', attrs={'property': 'og:description'
                             })
        # identify and tag text 
        text = data[0].get('content').split()
        # user name as account calls itself
        user = '%s %s' % (text[-3], text[-2])
        # number of followers
        followers = int(text[0].replace(',','').replace('k','000'))
        # number of accounts followed
        following = int(text[2].replace(',',''))
        # number of posts
        posts = int(text[4].replace(',',''))
        # output user/username with #posts, #followers, and #accounts that user is following 
        return user, posts, followers, following

    def main(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        # load the record log
        df=pd.read_csv('data/made/verified_accounts_ttvpa_used_to_follow.csv')
        # # extract urls to each 
        # urls=[i for i in df.user_profile]
        # que through each account in records
        for _ in range(len(df[:5])):
            # focus whichever account is up
            account = df.loc[_]
            # list out it's datapoints
            datas = [i for i in account]
            # pull metrics on that account via url
            metrics = list(self.getinfo(account.user_profile))
            # note the time these metrics were recorded
            metrics.append(datetime.now()) 
            # go through each metric
            for metric in metrics:
                # add it to the account's datapoints 
                datas.append(metric)
            '''record the transaction
            '''  
            # open up the csv
            with open('data/made/test_account_data.csv', 'a') as file:
                # fit the writer
                writer = csv.writer(file)
                # document the transaction
                writer.writerow(datas)


if __name__ == '__main__':
    obj = Insta_Info_Scraper()
    obj.main()
