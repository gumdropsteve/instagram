import pandas as pd
from infos import redo_unfollow_log  # , re_verified_unfollow_log
from bot import InstagramBot
a=sum(redo_unfollow_log.possible_404)
ig = InstagramBot(username='u', password='p')
b=len(ig.analyze_following(follow_backers=True))
print(f'{a}\n{b}\n\n{a+b}')
