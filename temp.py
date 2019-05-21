import pandas as pd
df=pd.read_csv('accounts_ttvpa_used_to_follow.csv')
df=df[df.account_id!='account_id']
df.to_csv('accounts_ttvpa_used_to_follow.csv',index=False)
