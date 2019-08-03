# imports
from instapy import InstaPy
from instapy import smart_run
from time import sleep
import random

# login credentials
from user import u, p

# get an InstaPy session!
# set headless_browser=True to run InstaPy in the background
session = InstaPy(username=u,
                  password=p,
                  headless_browser=True)

# set call of duty hashtags
cod_tags = ["codnation","callofduty","codblackout","blackout","blackops4","bo4",
            "modernwarfare","codtoplays","callofdutymodernwarfare","bo4clips",
            "callofdutybo4","codclips","blackops4clips","bo4multiplayer","codbo4",
            "callofdutyclips","treyarch","activision"]

with smart_run(session):
    """ Activity flow """		
    # general settings		
    # session.set_dont_include(["friend1", "friend2", "friend3"])		

    # track number of tags
    n_tags = 0
    # collect tags to like in groups of 3
    bag_tags = []
    # looping to add sleep between tags
    for tag in cod_tags:	
        # update tag bag
        bag_tags.append(tag)
        # update tag count
        n_tags += 1
        # every 3rd tag
        if n_tags == 3:
            # display bag
            print(f'\nthis bag = {bag_tags}\n')
            # execute likes on tags in this bag
            session.like_by_tags(tags=bag_tags, amount=21)
            # add random rest (hedge like only engagement ban)
            rest = random.randint(a=60, b=120)
            sleep(rest)
            # reset tag bag & count
            bag_tags = []
            n_tags = 0 

    # Joining Engagement Pods
    session.join_pods()
