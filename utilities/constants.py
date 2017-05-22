DATETIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'

# Keys in Twitter JSON
CREATED_AT = 'created_at'
ENTITIES = 'entities'
TEXT = 'text'
RETWEET_COUNT = 'retweet_count'
ID = 'id'
USER = 'user'
SCREEN_NAME = 'screen_name'
PLACE = 'place'
COORDINATES = 'coordinates'
HASHTAGS = 'hashtags'
MENTIONS = 'user_mentions'
URLS = 'urls'
URL = 'url'
EXPANDED_URL = 'expanded_url'
RETWEETED_STATUS = 'retweeted_status'
LOWER_ENTITY = '_id'


# Keys in MongoDB
TIMESTAMP = 'Timestamp'
TWEET = 'Tweet'
RETWEETS = 'Retweets'
USERNAME = 'Username'

VALUE = 'value'
COUNT = 'count'
PSEUDONYMS = 'pseudos'
GENERAL_ID_TAG = '_id'


# MongoDB Literals
RAW_TWEETS_DB_NAME = 'raw_tweets'
TOPIC_TWEETS_DB_NAME = 'topic_tweets'
URL_RESULTS_DB_NAME = 'url_results'

RAW_COLLECTION_PREFIX = 'raw_'
ENTITY_RESULTS_COLLECTION_PREFIX = 'entity_result_'
TEMP_RAW_COLLECTION_NAME = 'raw_temp'
TEMP_RESULTS_COLLECTION_NAME = 'result_temp'
URL_RESULTS_COLLECTION_PREFIX = 'url_result_'
TOPIC_COLLECTION_PREFIX = 'topic_'


def TOPIC_URL_AGGR_COLLECTION_NAME(topic_id):
    return URL_RESULTS_COLLECTION_PREFIX + str(topic_id)


def TOPIC_COLLECTION_NAME(topic_id):
    return TOPIC_COLLECTION_PREFIX + str(topic_id)


# FileNames
MAP_FUNCTION_FILENAME = 'mapFunction.js'
REDUCE_FUNCTION_FILENAME = 'reduceFunction.js'
AGGREGATION_MAP_ADD_FUNCTION_FILENAME = 'aggregationAddMapFunction.js'
AGGREGATION_MAP_SUBTRACT_FUNCTION_FILENAME = 'aggregationSubtractMapFunction.js'
AGGREGATION_REDUCE_FUNCTION_FILENAME = 'aggregationReduceFunction.js'

MONGO_INIT_FILE = 'start_mongo.bat'

ENGINE_MANAGER = 'manager.py'
PREPROCESSOR = 'preprocess.py'
ENTITY_AGGREGATOR = 'entity_aggregation.py'
EXTRACTOR = 'tweet_extractor.py'
PROCESSOR = 'process.py'
GRAPH_APPROXIMATOR = 'graph_approximation.py'
LDA_PROCESS = 'lda.py'
LDA_PREPROCESSOR = 'lda_preprocessing.py'
TWEET_SEGREGATOR = 'tweet_segregation.py'
MODELLER = 'modeller.py'

DJANGO_MANAGER = 'manage.py'
RUNSERVER_COMMAND = 'runserver'

DATA_FILE_PREFIX = 'data'
TOPIC_FILE_PREFIX = 'topic'

REQUIREMENTS = 'requirements.txt'
PIP_INSTALL_FILE = 'get-pip.py'
PYTHON_INSTALL_FILE = 'python_install.lnk'
MONGO_INSTALL_FILE = 'mongo_install.lnk'


# LDA Files
DICTIONARY_PREFIX = 'dictionary_'
CORPUS_PREFIX = 'corpus_'
LDA_MODEL_PREFIX = 'model_'


# Directories
JAVASCRIPT_DIR = 'javascript'
EXTRACTOR_DIR = 'extractor'
PROCESSOR_DIR = 'processor'
DATA_DIR = 'data'
TEMP_DIR = 'temp'
ENGINE_DIR = 'engine'
MISCELLANEOUS_DIR = 'miscellaneous'
DEPENDENCIES_DIR = 'dependencies'
BATCH_DIR = 'batch'
MONGO_DIR = 'MongoDB'
INFO_GENERATOR_DIR = 'info_generator'
HTML_DIR = 'html'
MODEL_DATA_DIR = 'model_data'
TOPIC_MODELLER_DIR = 'topic_modeller'

WEBSITE_DIR = 'website'
STATIC_DIR = 'static'
TSV_DIR = 'tsv'
URLS_DIR = 'urls'
WORDCLOUD_DIR = 'wordclouds'

WHEELHOUSE = 'wheelhouse'


# Processes
MANAGER_PROCESS = 'Manager'
PROCESSOR_PROCESS = 'Processor'


# MongoDB Operators
LESS_THAN = '$lt'
GREATER_THAN_OR_EQUAL = '$gte'


# File Extensions
JSON = '.json'
TSV = '.tsv'
HTML = '.html'
MM = '.mm'
DICT = '.dict'
LDA = '.lda'
TXT = '.txt'


# File Constants
UTF8 = 'utf-8'
WRITE = 'w'
READ = 'r'
