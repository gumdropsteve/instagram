# imports
from instapy import InstaPy
from instapy import smart_run

# login credentials
from user import u, p
insta_username = u
insta_password = p

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=True)

# set call of duty hashtags
cod_tags = ["codnation","callofduty","codblackout","blackout","blackops4","bo4",
            "modernwarfare","codtoplays","callofdutymodernwarfare","bo4clips",
            "callofdutybo4","codclips","blackops4clips","bo4multiplayer","codbo4",
            "callofdutyclips","treyarch","activision"]

with smart_run(session):
    """ Activity flow """		
    # general settings		
    session.set_dont_include(["friend1", "friend2", "friend3"])		

    # activity		
    session.like_by_tags(cod_tags, amount=11)

    # Joining Engagement Pods
    session.join_pods()
