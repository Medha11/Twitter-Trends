"""
Preprocess the tweets for lda
Perform cleaning
Create and save dictionary and corpus
"""
from os.path import join

from gensim import corpora
from pymongo import MongoClient, DESCENDING

from utilities.cleaner import clean
from utilities.config import NUMBER_OF_TOP_ENTITIES, TWEET_POOLING_SIZE
from utilities.constants import *
from utilities.os_util import get_dir
from utilities.time_management import get_prev_day, get_today, get_date_string, start_timing, stop_timing


TODAY = get_today()
TODAY_STRING = get_date_string(TODAY)
COLLECTION_DAY = TODAY #get_prev_day(TODAY)
COLLECTION_DAY_STRING = get_date_string(COLLECTION_DAY)

ROOT = get_dir(__file__)
DICTIONARY_PATH = join(ROOT, DATA_DIR, DICTIONARY_PREFIX + TODAY_STRING + DICT)
CORPUS_PATH = join(ROOT, DATA_DIR, CORPUS_PREFIX + TODAY_STRING + MM)

COLLECTION_NAME = RAW_COLLECTION_PREFIX + COLLECTION_DAY_STRING
RESULTS_COLLECTION_NAME = ENTITY_RESULTS_COLLECTION_PREFIX + COLLECTION_DAY_STRING

client = MongoClient()
raw_db = client[RAW_TWEETS_DB_NAME]
raw_collection = raw_db[COLLECTION_NAME]
results_coll = raw_db[RESULTS_COLLECTION_NAME]


def get_documents():
    documents = []
    results = results_coll.find(limit=NUMBER_OF_TOP_ENTITIES, no_cursor_timeout=True) \
        .sort([(VALUE + '.' + COUNT, DESCENDING)])
    for result in results:
        entities = result[VALUE][PSEUDONYMS]
        for entity in entities:
            cnt = 0
            document = ''
            for tweet in raw_collection.find({ENTITIES: entity}):
                cnt += 1
                document += tweet[TWEET] + ' '  # Pooling tweets
                if cnt == TWEET_POOLING_SIZE:
                    documents.append(document)
                    document = ''
                    cnt = 0
            if document != '':
                documents.append(document)
    results.close()

    return documents


def execute():
    start_timing()
    print 'Starting Pre-processing for LDA...',

    documents = get_documents()
    tokenized_documents = clean(documents)

    dictionary = corpora.Dictionary([doc for doc in tokenized_documents])
    dictionary.compactify()
    dictionary.save(DICTIONARY_PATH)

    corpus = [dictionary.doc2bow(doc) for doc in tokenized_documents]
    corpora.MmCorpus.serialize(CORPUS_PATH, corpus)

    print 'Finished'
    stop_timing()

    client.close()


if __name__ == '__main__':
    execute()
