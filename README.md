# Instagram
## InstagramBot ([bot.py](https://github.com/gumdropsteve/instagram/blob/master/bot.py))
Object-oriented Selenium (Python) WebDriver class providing deep-insight and task automation for Instagram users.

#### Abilities: 
  - Log in to Instagram
    - login()
  - like Instagram posts based on hashtag(s)
    - like_photos(hashtag)
  - Evaluate following
    - analyze_following(followers, following, to_unfollow=False, follow_backers=False)
      - if to_unfollow=True
        - returns urls of accounts which the user follows but is not followed by
      - if follow_backers=True
        - returns urls of accounts which the user both follows and is followed by
      - must be given data
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
