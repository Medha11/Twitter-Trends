"""
Iterate over all tweets in each of the 100 collections.
Each tweet has to be categorized into a topic.

As each hashtag normally falls into one category, try to find percentage match to a topic and assign
all tweets in the collection to the best matched topic.

For mentions, each tweet is independently categorized into a topic. TODO

Also while iterating, find the best tweet that matches a topic, for each topic.
This can be used to summarize the topic in the homepage.
"""
import io
from os.path import join

from gensim import models, corpora
from pymongo import MongoClient, DESCENDING

from utilities.cleaner import clean
from utilities.constants import *
from utilities.config import NUMBER_OF_TOP_ENTITIES, NUMBER_OF_TOPICS
from utilities.entities.Collection import Collection
from utilities.mongo import check_or_create_collection, copy_into_collection
from utilities.os_util import get_dir
from utilities.time_management import get_prev_day, start_timing, stop_timing, get_today, get_date_string, get_time, get_differenced_day

TODAY = get_today()
TODAY_STRING = get_date_string(TODAY)
COLLECTION_DAY = TODAY #get_prev_day(TODAY)
COLLECTION_DAY_STRING = get_date_string(COLLECTION_DAY)

ROOT = get_dir(__file__)
DICTIONARY_PATH = join(ROOT, DATA_DIR, DICTIONARY_PREFIX + TODAY_STRING + DICT)
CORPUS_PATH = join(ROOT, DATA_DIR, CORPUS_PREFIX + TODAY_STRING + MM)
LDA_PATH = join(ROOT, DATA_DIR, LDA_MODEL_PREFIX + TODAY_STRING + LDA)
MODEL_DATA_PATH = join(ROOT, MODEL_DATA_DIR)

CORPUS = corpora.MmCorpus(CORPUS_PATH)
DICTIONARY = corpora.Dictionary.load(DICTIONARY_PATH)
LDA_MODEL = models.LdaModel.load(LDA_PATH)

COLLECTION_NAME = RAW_COLLECTION_PREFIX + COLLECTION_DAY_STRING
RESULTS_COLLECTION_NAME = ENTITY_RESULTS_COLLECTION_PREFIX + COLLECTION_DAY_STRING

client = MongoClient()
raw_db = client[RAW_TWEETS_DB_NAME]
topic_db = client[TOPIC_TWEETS_DB_NAME]
raw_collection = raw_db[COLLECTION_NAME]
entity_results_coll = raw_db[RESULTS_COLLECTION_NAME]

top_tweet = [None]*NUMBER_OF_TOPICS
top_prob = [0]*NUMBER_OF_TOPICS
actual_entity = {}
entity_topic = {}
entity_pseudos = {}
writers = []


def init_writer(tid):
    filename = TOPIC_FILE_PREFIX + str(tid) + TXT
    file_path = join(MODEL_DATA_DIR, filename)

    x = io.open(file_path, WRITE, encoding=UTF8)
    return x


def close_writer(tid):
    writers[tid].close()


def make_entry(tid, string):
    writers[tid].write(string + '\n')


def get_topic_for_entity(cleaned_tweets, original_tweets):

    probs = [0]*NUMBER_OF_TOPICS

    for i, tweet in enumerate(cleaned_tweets):
        distribution = LDA_MODEL.get_document_topics(DICTIONARY.doc2bow(tweet), minimum_probability=0)
        for topic_id, prob in distribution:
            probs[topic_id] += prob
            if prob > top_prob[topic_id]:
                top_prob[topic_id] = prob
                top_tweet[topic_id] = original_tweets[i]

    max_prob = 0
    topic = -1
    for topic_id, prob in enumerate(probs):
        if prob > max_prob:
            topic = topic_id
            max_prob = prob

    return topic


def save_to_collection():

    for lower_entity in entity_pseudos.keys():
        for entity in entity_pseudos[lower_entity]:
            topic_id = entity_topic[lower_entity]
            coll_name = TOPIC_COLLECTION_NAME(topic_id)
            check_or_create_collection(TOPIC_TWEETS_DB_NAME, coll_name, Collection.TOPIC)
            coll = topic_db[coll_name]
            copy_into_collection(raw_collection.find({ENTITIES: entity}), coll)


def save_model_data():

    for topic_id in range(NUMBER_OF_TOPICS):
        writers.append(init_writer(topic_id))

        make_entry(topic_id, u'Top 20 Word - Probability:')
        word_tuples = LDA_MODEL.show_topic(topic_id, 20)
        for word_tuple in word_tuples:
            make_entry(topic_id, word_tuple[0] + unicode('-' + str(word_tuple[1]), UTF8))

        make_entry(topic_id, u'')

        make_entry(topic_id, u'Top tweet:')
        make_entry(topic_id, top_tweet[topic_id][TWEET])

        make_entry(topic_id, u'')

        make_entry(topic_id, u'Entities:')

    for lower_entity in entity_topic.keys():
        topic_id = entity_topic[lower_entity]
        entity = actual_entity[lower_entity]
        make_entry(topic_id, entity)
        
    for topic_id in range(NUMBER_OF_TOPICS):
        close_writer(topic_id)


def execute():
    print 'Started at ' + get_time() + '... ',
    start_timing()

    client.drop_database(TOPIC_TWEETS_DB_NAME)
    results = entity_results_coll.find(limit=NUMBER_OF_TOP_ENTITIES, no_cursor_timeout=True) \
        .sort([(VALUE + '.' + COUNT, DESCENDING)])

    for result in results:
        tweets = []
        text = []
        lower_entity = result[LOWER_ENTITY]
        entities = result[VALUE][PSEUDONYMS]
        entity_pseudos[lower_entity] = entities

        max_tweets = 0
        for entity in entities:
            c = 0
            for tweet in raw_collection.find({ENTITIES: entity}):
                c += 1
                tweets.append(tweet)
                text.append(tweet[TWEET])
            if c > max_tweets:
                actual_entity[lower_entity] = entity
                max_tweets = c

        text = clean(text)
        topic_id = get_topic_for_entity(text, tweets)
        entity_topic[lower_entity] = topic_id

    save_to_collection()
    save_model_data()

    print 'Finished'
    stop_timing()


if __name__ == '__main__':
    execute()
