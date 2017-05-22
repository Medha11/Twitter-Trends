# Import the necessary methods from tweepy library
from os import rename
from os.path import join

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

from utilities.config import *
from utilities.constants import *
from utilities.miscellaneous import is_json
from utilities.os_util import get_dir
from utilities.time_management import get_time


display_number = DISPLAY_COMPLETED_TWEETS_INTERVAL

file_number = 1
tweets_cnt = 0
total_tweets_cnt = 0

ROOT = get_dir(__file__)

FILE_PATH = join(ROOT, DATA_DIR)
TEMP_PATH = join(ROOT, TEMP_DIR)


def get_filename(directory, number):
    return join(directory, DATA_FILE_PREFIX + FILE_NAME_FORMATTER % number + JSON)


def change_file():
    global tweets_file, file_name, file_number

    tweets_file.close()
    rename(file_name, get_filename(TEMP_PATH, file_number))  # moving file to temp folder

    file_number += 1
    if file_number == FILE_NUMBER_RESET_VALUE:
        file_number = 1

    file_name = get_filename(FILE_PATH, file_number)
    tweets_file = open(file_name, WRITE)


# This is a basic listener that gives the tweets.
class StdOutListener(StreamListener):

    def on_data(self, data):

        if not is_json(data):  # checking if invalid tweet
            return True
        global tweets_cnt, file_number, tweets_file, file_name, display_number, total_tweets_cnt

        tweets_cnt += 1
        total_tweets_cnt += 1
        tweets_file.write(data)

        if total_tweets_cnt == display_number:  # check if completion status is to be updated
            print '\r',
            print str(display_number) + ' Tweets Downloaded',
            display_number += DISPLAY_COMPLETED_TWEETS_INTERVAL

        if tweets_cnt == MAX_TWEETS_IN_FILE:
            tweets_cnt = 0
            change_file()

        return True

    def on_error(self, status):
        print 'Error: ' + status


if __name__ == '__main__':

    file_name = get_filename(FILE_PATH, file_number)
    tweets_file = open(file_name, WRITE)

    print "Started extracting tweets at " + get_time() + "... "

    while True:  # ensures continuous stream extraction

        try:
            # This handles Twitter authentication and the connection to Twitter Streaming API

            l = StdOutListener()
            auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

            stream = Stream(auth, l)
            stream.filter(languages=[ENGLISH], track=FILTER_KEYWORDS)

        except:  # TODO
            continue
