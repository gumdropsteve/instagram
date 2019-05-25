"""testing for 'impossible' cases
defined: 
    instances where following_button was not found/clicked (1) and
    unfollow_button was found/clicked
why 'impossible':
    'Unfollow' button appearance is dependent on 'Following' button being clicked
method:
    simple, followable by novice
"""
# imports
import pandas as pd
# load current unfollow data
df=pd.read_csv('accounts_ttvpa_used_to_follow.csv')
# collect 0,1 instances 
zero_one_s=[]
# collect 1,0 instances (not primary goal; looking into possiblities for improvement)
what_happened_here=[]
# tag list of 'following_button' column
fing_btn=list(df.following_button)
# tag list of 'unfollow_button' column
uflow_btn=list(df.unfollow_button)
# go though each instance 
for i in range(len(uflow_btn)):
    # determine if the 'Following' button was or was not found/clicked
    if fing_btn[i]==1:
        # look at that instance's 'Unfollow' button, for success
        if uflow_btn[i]==0:
            # it was somehow successful, make note this
            zero_one_s.append(i)
    # let's also check out instances where 'Following' button was found/clicked
    if fing_btn==0:
        # so pull up that instance's 'Unfollow' button, for failure
        if uflow_btn[i]==1:
            # ok, we might need to adjust something; note position
            what_happened_here.append(i)
# check for number of 'impossible' instances
print(len(zero_one_s))
# if there are any
if len(zero_one_s)>0:
    # show us
    print(zero_one_s)
# check for number of 1,0 instances
print(len(what_happened_here))
# if there are any
if len(what_happened_here)>0:
    # show us
    print(what_happened_here)
# did expected outcome occour
if len(zero_one_s) == 0 and len(what_happened_here) == 0:
    # great, let us know
    print('all is well, proceed coding bot.py')
