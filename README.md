## Instagram ([bot.py](https://github.com/gumdropsteve/instagram/blob/master/bot.py))
Object-oriented Selenium (Python) WebDriver class providing insight and task automation for Instagram users. 

<a href="https://github.com/SeleniumHQ/selenium" target="_blank">
  <img src="https://img.shields.io/badge/built%20with-Selenium-yellow.svg" /></a>
<a href="https://www.python.org/" target="_blank">
  <img src="https://img.shields.io/badge/built%20with-Python3-red.svg" /></a>

#### Primary Abilities: 
- Log in to Instagram
  - ig.[login()](https://github.com/gumdropsteve/instagram/blob/master/bot.py#L70)
- Gather posts by hashtag
  - ig.[gather_posts()](https://github.com/gumdropsteve/instagram/blob/master/bot.py#L100)
- Like posts based on hashtag
  - ig.[like_posts()](https://github.com/gumdropsteve/instagram/blob/master/bot.py#L246)
- Comment or add hashtags to a post
  - ig.[comment()](https://github.com/gumdropsteve/instagram/blob/master/bot.py#L302)

#### Example Uses:
- [add_hashtags](https://github.com/gumdropsteve/instagram/blob/master/run.py#L24) to a post as a comment
- Gather posts then [like_by_hashtag](https://github.com/gumdropsteve/instagram/blob/master/run.py#L45) after making sure you haven't already liked them 
- [rec_n_check](https://github.com/gumdropsteve/instagram/blob/master/run.py#L6) an account's followers and following to identify then (optionally) unfollow non-followbackers
  
