# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% PERCENTAGE COMPLETION FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
import json

from utilities.constants import *


def display_percentage(cur_count, total_count, interval):      # interval it is the interval of display,
    if total_count == 0:
        print '\r',
        print str(100) + '% complete',
        return

    percent = (cur_count * 100) / total_count
    rounded_percent = (percent/interval)*interval

    print '\r',
    print str(rounded_percent) + '% complete',


def is_json(obj):
    necessary_keys = [CREATED_AT, ENTITIES, TEXT, RETWEET_COUNT, ID, USER, COORDINATES, PLACE]
    try:
        keys = json.loads(obj).keys()
        for key in necessary_keys:
            if key not in keys:
                return False
    except:  # TODO
        return False
    return True


