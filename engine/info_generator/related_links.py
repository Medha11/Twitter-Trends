"""
Find the most frequently shared URLs for each topic.
Use MapReduce to get the frequency of URLs per topic.
"""
# TODO Try to add more intelligence to neglect unrelated URLs etc.
from bson.code import Code
from os.path import join

from pymongo import MongoClient, DESCENDING

from utilities.config import NUMBER_OF_TOPICS, NUMBER_OF_URLS_TO_EXTRACT
from utilities.constants import *
from utilities.entities.Collection import Collection
from utilities.mongo import check_or_create_collection
from utilities.os_util import get_dir
from utilities.time_management import start_timing, stop_timing


ROOT = get_dir(__file__)
JAVASCRIPT_PATH = join(ROOT, JAVASCRIPT_DIR)
URLS_DIR_PATH = join(ROOT, URLS_DIR)

client = MongoClient()
topics_db = client[TOPIC_TWEETS_DB_NAME]

MAP_FUNCTION = Code(open(join(JAVASCRIPT_PATH, MAP_FUNCTION_FILENAME), READ).read())
REDUCE_FUNCTION = Code(open(join(JAVASCRIPT_PATH, REDUCE_FUNCTION_FILENAME), READ).read())


def write_urls(topic_id, urls):
    file_path = join(URLS_DIR_PATH, TOPIC_FILE_PREFIX + str(topic_id) + TXT)
    x = open(file_path, WRITE)
    for url in urls:
        x.write(url + '\n')
    x.close()


def aggregate_urls(topic_ids):
    for topic_id in topic_ids:
        coll_name = TOPIC_COLLECTION_NAME(topic_id)
        results_coll_name = TOPIC_URL_AGGR_COLLECTION_NAME(topic_id)

        check_or_create_collection(TOPIC_TWEETS_DB_NAME, coll_name, Collection.TOPIC)
        check_or_create_collection(TOPIC_TWEETS_DB_NAME, results_coll_name, Collection.URL_RESULT)

        coll = topics_db[coll_name]
        coll.map_reduce(MAP_FUNCTION, REDUCE_FUNCTION, results_coll_name)


def get_hot_topics():
    counts = []
    for i in range(NUMBER_OF_TOPICS):
        coll_name = TOPIC_COLLECTION_NAME(i)
        counts.append((topics_db[coll_name].count(), i))

    counts.sort(reverse=True)
    topic_ids = []
    for i in range(5): # TODO
        topic_ids.append(counts[i][1])

    return topic_ids


def execute():
    print 'Started Entity Aggregation... '
    start_timing()

    topics = get_hot_topics()
    print topics
    aggregate_urls(topics)

    for topic_id in topics:
        results_coll_name = TOPIC_URL_AGGR_COLLECTION_NAME(topic_id)
        results_coll = topics_db[results_coll_name]

        top_urls = []

        results = results_coll.find(limit=NUMBER_OF_URLS_TO_EXTRACT).sort([(VALUE, DESCENDING)])
        for result in results:
            top_urls.append(result[GENERAL_ID_TAG])

        write_urls(topic_id, top_urls)

    client.close()

    print 'Finished'
    stop_timing()


if __name__ == '__main__':
    execute()
