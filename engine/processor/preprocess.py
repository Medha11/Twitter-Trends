"""
 Extract tweets from temp folder and clean it.
 Save the timestamp, username, entities, retweet_details, urls, coordinates, place, id.
 Dump into a temp_raw collection.
"""
import json
from os import remove
from os.path import join
import pytz

from pymongo import MongoClient

from utilities.constants import *
from utilities.entities.Collection import Collection
from utilities.miscellaneous import display_percentage
from utilities.mongo import check_or_create_collection, insert_many
from utilities.time_management import datetime, start_timing, stop_timing
from utilities.os_util import dirname, get_dir, get_files_in_dir


ENGINE_ROOT = dirname(get_dir(__file__))
TEMP_PATH = join(ENGINE_ROOT, EXTRACTOR_DIR, TEMP_DIR)

check_or_create_collection(RAW_TWEETS_DB_NAME, TEMP_RAW_COLLECTION_NAME, Collection.TEMP)

client = MongoClient()
db = client[RAW_TWEETS_DB_NAME]
collection = db[TEMP_RAW_COLLECTION_NAME]


def is_retweet(tweet):
    return RETWEETED_STATUS in tweet.keys()


def extract_data(file_path):  # load json file into a list of dictionaries
    tweets = []
    tweets_file = open(file_path, 'r')
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets.append(tweet)
        except ValueError:  # TODO find the exceptions and mention it after except
            continue
    tweets_file.close()
    return tweets


def extract_time(date):
    date = datetime.strptime(date, DATETIME_FORMAT)
    date = date.replace(tzinfo=pytz.UTC)
    return date


def get_hash_and_mentions(entities):
    new_entities = []
    hashtags = entities[HASHTAGS]
    mentions = entities[MENTIONS]

    for hashtag in hashtags:
        new_entities.append('#'+hashtag[TEXT])
    for mention in mentions:
        new_entities.append('@'+mention[SCREEN_NAME])

    return new_entities


def get_urls(entities):
    urls = []
    for url in entities[URLS]:
        urls.append({URL: url[URL], EXPANDED_URL: url[EXPANDED_URL]})
    return urls


def process(tweets):  # extract relevant information from tweets
    processed_data = []
    for tweet in tweets:
        try:
            if is_retweet(tweet):
                tweet = tweet[RETWEETED_STATUS]  # TODO see if this is needed
            processed_tweet = {ENTITIES: get_hash_and_mentions(tweet[ENTITIES])}
            if len(processed_tweet[ENTITIES]) == 0:  # checking if tweet has hashtags or user mentions
                continue  # TODO is this necessary?

            processed_tweet[TIMESTAMP] = extract_time(tweet[CREATED_AT])
            processed_tweet[USERNAME] = tweet[USER][SCREEN_NAME]
            processed_tweet[TWEET] = tweet[TEXT]
            processed_tweet[RETWEETS] = tweet[RETWEET_COUNT]
            processed_tweet[URLS] = get_urls(tweet[ENTITIES])
            processed_tweet[COORDINATES] = tweet[COORDINATES]
            processed_tweet[PLACE] = tweet[PLACE]
            processed_tweet[ID] = tweet[ID]
            processed_data.append(processed_tweet)

        except:  # TODO
            'Tweet Error'
            print tweet

    return processed_data


def execute():
    data_files = get_files_in_dir(TEMP_PATH, JSON)
    l = len(data_files)
    print 'Started Preprocessing ' + str(l) + ' files... '
    start_timing()

    cnt = 0
    percent_interval = 1  # increment for the completion percent display
    display_percentage(cnt, l, percent_interval)

    for data_file in data_files:
        data_file_path = join(TEMP_PATH, data_file)
        tweets_data = extract_data(data_file_path)
        processed_tweets = process(tweets_data)

        insert_many(collection, processed_tweets)
        remove(data_file_path)

        # updating completion status
        cnt += 1
        display_percentage(cnt, l, percent_interval)

    client.close()
    print
    print 'Finished'

    stop_timing()


if __name__ == '__main__':
    execute()
