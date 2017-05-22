"""
 Does map reduce on temp_raw collection to find freq of entities
 Merges the results into a single result collection.
"""
from bson.code import Code
from os.path import join

from pymongo import MongoClient

from utilities.constants import *

from utilities.entities.Collection import Collection
from utilities.mongo import check_or_create_collection, copy_into_collection
from utilities.os_util import get_dir
from utilities.time_management import get_today, get_date_string, start_timing, stop_timing


ROOT = get_dir(__file__)
JAVASCRIPT_PATH = join(ROOT, JAVASCRIPT_DIR)


TODAY = get_today()
TODAY_STRING = get_date_string(TODAY)
COLLECTION_NAME = RAW_COLLECTION_PREFIX + TODAY_STRING
RESULTS_COLLECTION_NAME = ENTITY_RESULTS_COLLECTION_PREFIX + TODAY_STRING

check_or_create_collection(RAW_TWEETS_DB_NAME, TEMP_RAW_COLLECTION_NAME, Collection.TEMP)
check_or_create_collection(RAW_TWEETS_DB_NAME, COLLECTION_NAME, Collection.RAW)
check_or_create_collection(RAW_TWEETS_DB_NAME, TEMP_RESULTS_COLLECTION_NAME, Collection.ENTITY_RESULT)
check_or_create_collection(RAW_TWEETS_DB_NAME, RESULTS_COLLECTION_NAME, Collection.ENTITY_RESULT)

client = MongoClient()
db = client[RAW_TWEETS_DB_NAME]
coll = db[COLLECTION_NAME]
temp_raw = db[TEMP_RAW_COLLECTION_NAME]
temp_results = db[TEMP_RESULTS_COLLECTION_NAME]


def execute():
    print 'Started Entity Aggregation... ',

    start_timing()

    map_function = Code(open(join(JAVASCRIPT_PATH, MAP_FUNCTION_FILENAME), 'r').read())
    reduce_function = Code(open(join(JAVASCRIPT_PATH, REDUCE_FUNCTION_FILENAME), 'r').read())
    aggregate_map_function = Code(open(join(JAVASCRIPT_PATH, AGGREGATION_MAP_ADD_FUNCTION_FILENAME), 'r').read())
    aggregate_reduce_function = Code(open(join(JAVASCRIPT_PATH, AGGREGATION_REDUCE_FUNCTION_FILENAME), 'r').read())

    temp_raw.map_reduce(map_function, reduce_function, TEMP_RESULTS_COLLECTION_NAME)
    temp_results.map_reduce(aggregate_map_function, aggregate_reduce_function, {'reduce': RESULTS_COLLECTION_NAME})

    if temp_raw.count() > 0:
        copy_into_collection(temp_raw.find(no_cursor_timeout=True), coll)

    temp_results.drop()
    temp_raw.drop()

    client.close()
    
    print 'Finished'
    stop_timing()


if __name__ == '__main__':
    execute()
