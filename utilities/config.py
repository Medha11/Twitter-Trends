from datetime import timedelta


# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = "2583390259-eRijiycaorQHFeVGTI2YNfT6kc9JWtNSOdwlfnR"
ACCESS_TOKEN_SECRET = "IWhMPVdw9sdSJ4ex20ObFgS2BbGLxo3nWHyqp4sy4Bga2"
CONSUMER_KEY = "SVI97pI1bbxjHOevoGoyCUH5X"
CONSUMER_SECRET = "anAQ83bkPT7JmIEvPssQ8CbP2tUmADq9Jn68VdHg1HiROcoJr2"


# General
PYTHON_VERSION = '2.7.10'
TIMEZONE = 'Asia/Kolkata'


# time constants
SECONDS = 1
MINUTES = 60 * SECONDS
HOURS = 60*MINUTES


# Preprocessor
PROCESSOR_SLEEP_TIME = 10*MINUTES


# Tweets Extractor
MAX_TWEETS_IN_FILE = 10000
DISPLAY_COMPLETED_TWEETS_INTERVAL = 1000

FILE_NUMBER_RESET_VALUE = 1000
FILE_NAME_SUFFIX_DIGITS = len(str(FILE_NUMBER_RESET_VALUE - 1))  # number of digits in the suffix
FILE_NAME_FORMATTER = '%0' + str(FILE_NAME_SUFFIX_DIGITS) + 'd'

# The top 20 most used keywords from the following URL:
# http://techland.time.com/2009/06/08/the-500-most-frequently-used-words-on-twitter/
FILTER_KEYWORDS = ["a", "the", "i", "you", "to", "and", "is", "in", "u", "of", "it"]
ENGLISH = 'en'


# Manager Process
DEBUG = True
STOP_DATA_EXTRACTION_TIME = '23:55'
RESTART_DATA_EXTRACTION_TIME = '00:05'
WEEK_RANGE = 7  # Represents number of days in a week

CHECK_SAFE_DATE_TIME = '01:00'  # This is to check if TODAY is actually the day in consideration


# Graph Approximation
DAY_START = '16:25'
APPROXIMATION_RANGE = timedelta(minutes=1)


# LDA Params
NUMBER_OF_TOP_ENTITIES = 50
TWEET_POOLING_SIZE = 100  # tweets
NUMBER_OF_TOPICS = 18
NUMBER_OF_PASSES = 20
ALPHA = 0.001


# Info Generator
NUMBER_OF_URLS_TO_EXTRACT = 15
