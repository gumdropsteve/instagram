import itertools
from time import sleep
from selenium import webdriver

username = 'ttv.princearthur'  # <username here>
password = 'WarfArE2+++'  # <password here>
# pre-set inputs
login_page = 'https://www.instagram.com/accounts/login/'
username_input = "//div/input[@name='username']"
password_input = "//div/input[@name='password']"
login_button = "//div/button[@type='submit']"
followers_href = "//a[@href='/instagram/followers/']"

def login(driver, user, pwrd):
    '''
    input) set-up Selenium webdriver {driver}
    input) Instagram username, email, or phone number {username}
    input) Instagram password {password}
    '''
    # load login page
    driver.get(login_page)
    # login

    def sign_on():
        driver.find_element_by_xpath(username_input).send_keys(user)
        sleep(2)
        driver.find_element_by_xpath(password_input).send_keys(pwrd)
        sleep(2)
        driver.find_element_by_xpath(login_button).click()
        sleep(2)

    available = driver.find_element_by_xpath(username_input)
    if available:
        sign_on()
    else:
        sleep(5)
        try:
            sign_on()
        except:
            return 'unable to sign on'
    # wait for the user dashboard page to load
    we_see_people = driver.find_element_by_xpath("//a/span[@aria-label='Find People']")
    if we_see_people:
        print('we see people')
    else:
        print('issa ghost town, adding sleep')
        sleep(5)


def scrape_followers(driver, account):
    # load account page
    driver.get(f'https://instagram.com/{account}/')
    # click the 'Follower(s)' link
    # driver.find_element_by_partial_link_text('follower').click()
    driver.find_element_by_xpath(followers_href).click()
    # wait for the followers modal to load
    sleep(2)
    if driver.find_element_by_xpath("//div[@role='dialog']"):
        sleep(0)
    else:
        sleep(5)
    # At this point a Followers modal pops open. If you immediately scroll to the bottom,
    # you hit a stopping point and a "See All Suggestions" link. If you fiddle with the
    # model by scrolling up and down, you can force it to load additional followers for
    # that person.

    # Now the modal will begin loading followers every time you scroll to the bottom.
    # Keep scrolling in a loop until you've hit the desired number of followers.
    # In this instance, I'm using a generator to return followers one-by-one
    follower_css = "ul div li:nth-child({}) a.notranslate"  # Taking advange of CSS's nth-child functionality
    for group in itertools.count(start=1, step=12):
        for follower_index in range(group, group + 12):
            yield driver.find_element_by_css_selector(follower_css.format(follower_index)).text

        # Instagram loads followers 12 at a time. Find the last follower element
        # and scroll it into view, forcing instagram to load another 12
        # Even though we just found this elem in the previous for loop, there can
        # potentially be large amount of time between that call and this one,
        # and the element might have gone stale. Lets just re-acquire it to avoid
        # that
        last_follower = driver.find_element_by_css_selector(follower_css.format(follower_index))
        driver.execute_script("arguments[0].scrollIntoView();", last_follower)


if __name__ == "__main__":
    account = 'instagram'
    # driver
    # options = webdriver.FirefoxOptions()  
    # options.set_preference("dom.push.enabled", False)  # blocks popups 
    driver = webdriver.Firefox(executable_path='‎⁨Macintosh HD/Users/winston/Downloads/geckodriver')  # adds options
    try:
        login(driver, username, password)
        # Print the first 75 followers for the "instagram" account
        print(f'Followers of the "{account}" account')
        for count, follower in enumerate(scrape_followers(driver, account=account), 1):
            print('\t{:>3}: {}'.format(count, follower))
            if count >= 75:
                break
    finally:
        driver.quit()
