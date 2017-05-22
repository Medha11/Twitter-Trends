from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import BulkWriteError

from utilities.constants import VALUE, ENTITIES, TIMESTAMP, ID, COUNT, READ
from utilities.entities.Collection import Collection


client = MongoClient()


def get_urls():
    f = open('urls/topic4.tsv', READ)
    return [url for url in f]


def check_collection(db, coll):
    if db in client.database_names():
        db = client[db]
        if coll in db.collection_names():
            print 'Collection ' + coll + ' exists!!!'
            return True
    return False


def create_index(coll, coll_type=None):
    if coll_type == Collection.RAW:
        coll.create_index([(ENTITIES, ASCENDING), (TIMESTAMP, ASCENDING)])
    elif coll_type == Collection.ENTITY_RESULT:
        coll.create_index([(VALUE + '.' + COUNT, DESCENDING)])
    elif coll_type == Collection.URL_RESULT:
        coll.create_index([(VALUE, DESCENDING)])
    elif coll_type == Collection.TEMP:
        coll.create_index([(ID, ASCENDING)], unique=True)
    elif coll_type == Collection.TOPIC:
        coll.create_index([(TIMESTAMP, ASCENDING), (ID, ASCENDING)], unique=True)


def check_or_create_collection(db_name, coll_name, coll_type=None):
    if not check_collection(db_name, coll_name):
        print 'Creating collection ' + coll_name + '!!!'
        db_name = client[db_name]
        coll = db_name[coll_name]
        create_index(coll, coll_type)


def copy_into_collection(cursor, dest_coll):

    c = 0
    tw = []
    for t in cursor:
        c += 1
        tw.append(t)
        if c == 10000:
            c = 0
            insert_many(dest_coll, tw)
            tw = []

    if c > 0:
        insert_many(dest_coll, tw)    # transfer remaining
    cursor.close()


def insert_many(coll, documents):
    try:
        coll.insert_many(documents, ordered=False)
    except BulkWriteError:
        pass
