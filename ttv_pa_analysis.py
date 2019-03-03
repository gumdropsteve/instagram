import pandas as pd

ttv_princearthur = 'data/unfinished-All_users_ttv.princearthur_20190303_0543.csv'

def egg_check(data, *non_default_outcome):
    # build dataframe (df)
    df = pd.read_csv(data)
    # iso links to users in df
    profiles = df[['user_profile']]

    # profiles that do not follow us
    profiles_that_dont_follow = profiles[df['follows_viewer'] == False]
    non_followers = profiles_that_dont_follow.values.tolist()
    # profiles who follow us
    profiles_that_follow = profiles[df['follows_viewer'] == True]
    followers = profiles_that_follow.values.tolist()
    # profiles we follow
    profiles_we_follow = profiles[df['followed_by_viewer'] == True]
    following = profiles_we_follow.values.tolist()

    # return profiles we follow that do not follow back 
    do_not_follow_back = []
    # for profile we follow
    for profile in following:
        # if that profile is in non_followers and not in followers
        if profile in non_followers and profile not in followers:
            # add that profile to those that do_not_follow_back
            do_not_follow_back.append(profile)

    # return profiles we follow that do follow back 
    good_eggs = []
    duplicates = []
    multi_duplicate_count = 0
    # for profile we follow
    for profile in following:
        # if that profile is in followers and not in non_followers
        if profile in followers and profile not in non_followers:
            # check for duplicates
            if profile not in good_eggs:
                # add that profile to those that do_not_follow_back
                good_eggs.append(profile)
            # record duplicates 
            else:
                # check that this is the first unorigional occourance 
                if profile not in duplicates:
                    duplicates.append(profile)
                # if it's not, tally it and then continue as usual
                else:
                    multi_duplicate_count += 1
                    duplicates.append(profile)
    
    # if optional is argued
    if non_default_outcome:
        # just the good eggs
        if non_default_outcome == 1:
            print(good_eggs)
        # just the bad eggs
        if non_default_outcome == 2:
            print(do_not_follow_back)
        # both good and bad eggs
        if non_default_outcome == 3:
            print(good_eggs)
            print(do_not_follow_back)

    return f'good egg count = {len(good_eggs)} \nbad egg count = {len(do_not_follow_back)}'


print(egg_check(ttv_princearthur))
