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
        # specify 
        html = urllib.request.urlopen(url, context=self.ctx).read()
        # make soup
        soup = BeautifulSoup(html, 'html.parser')
        # identify interest 
        data = soup.find_all('meta', attrs={'property': 'og:description'})
        # tag & bag data 
        text = data[0].get('content').split()
        # user name as account calls itself
        user = '%s %s' % (text[-3], text[-2])
        # number of followers
        followers = text[0]
        # scan for number abbreviatiions
        if 'k' in followers or 'm' in followers:
            # keep exactly how is, for study
            followers = followers
        # if there are no indicators 
        else:
            followers = int(followers.replace(',',''))
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
        # que through each account in records
        for _ in range(len(df[:30])):
            # focus whichever account is up
            account = df.loc[_]
            # list out it's datapoints
            datas = [i for i in account]
            # will fail if 404 
            try:
                # pull metrics on that account via url
                metrics = list(self.getinfo(account.user_profile))
            # so for the potential 426 fails
            except:
                metrics = ['nan','nan','nan','nan']
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
