-* up to date status: reasonably
# Instagram
## InstagramBot ([bot.py](https://github.com/gumdropsteve/instagram/blob/master/bot.py))
Object-oriented Selenium (Python) WebDriver class providing deep-insight and task automation for Instagram users.

<a href="https://github.com/SeleniumHQ/selenium" target="_blank">
  <img src="https://img.shields.io/badge/built%20with-Selenium-yellow.svg" /></a>
<a href="https://www.python.org/" target="_blank">
  <img src="https://img.shields.io/badge/built%20with-Python3-red.svg" /></a>
 
#### Abilities: 
  - Log in to Instagram
    - .login()
  - Like posts based on hashtag
    - .like_posts(hashtag, hrefs)
  - Unfollow specific accounts
    - unfollow(start, end)
      - records the following about each unfollowed account in .csv
        - account id
        - username
        - profile_url
        - time_unfollowed
        - following_button
          - 0 if successful in finding "Following" button
          - 1 is unsuccessful in finding "Following" button
            - occours when account has either been deleted or has changed its username 
              - on lookout for possible other causes
        - unfollow_button
          - 0 if successful in finding "Unfollow" button
          - 1 if unsuccessful in finding "Unfollow" button
            - occours when following_button returns 1 
              - on lookout for possible other causes 
      - must be given list of account urls 
#### Future:
  - General comments
  - Smart comments
    - Understanding context 
  - Follow accounts
    - By hashtag
    - By other accounts
  - Bring back .analyze_following()
  - More follower analysis
    - Compairson to other accounts
    - Identify similar accounts
    - Identify specific patterns/behaviors
  - Post analysis 
    - Compairson
      - Similar accounts
      - Similar posts
    - Success tracker
      - Early indicators of post success
    - Post scraping
      - Memes & etc..
  - Account/post tracking 


Collection of data was done via [Helper Tools for Instagram](https://bit.ly/2RarbLj)
