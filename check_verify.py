import pandas as pd
df=pd.read_csv('data/made/verified_accounts_ttvpa_used_to_follow.csv')
accounts=list(df.account_id.values)
good=0
for account in accounts:
    count=accounts.count(account)
    if count!=1:
        raise Exception(f"count != 1 ; count == {count}")
    elif count==1:
        good+=1
if good!=len(accounts):
    raise Exception(f"good!=len(accounts) ; good=={len(accounts)}")
else:
    print(good)
