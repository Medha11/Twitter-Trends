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
from string import Template

from gensim import models
from pytagcloud import create_tag_image, create_html_data, make_tags, \
    LAYOUT_HORIZONTAL, LAYOUTS
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts

from utilities.constants import *
from utilities.os_util import get_dir
from utilities.time_management import get_prev_day, start_timing, stop_timing, get_today, get_date_string, get_time, get_differenced_day

TODAY = get_today()
TODAY_STRING = get_date_string(TODAY)

ROOT = get_dir(__file__)
PROJECT_ROOT = get_dir(get_dir(ROOT))

LDA_PATH = join(ROOT, DATA_DIR, LDA_MODEL_PREFIX + TODAY_STRING + LDA)
MODEL_DATA_PATH = join(ROOT, MODEL_DATA_DIR)
WORDCLOUD_PATH = join(PROJECT_ROOT, WEBSITE_DIR, STATIC_DIR, WORDCLOUD_DIR)

LDA_MODEL = models.LdaModel.load(LDA_PATH)


def normalize(arr):
    sum = 0
    for i in arr:
        sum += i
    for i in range(len(arr)):
        arr[i] = arr[i]/sum


def create_wordcloud(topic_id):
    word_tuples = LDA_MODEL.show_topic(topic_id, 20)
    # array of words with their frequencies
    words_arr = []
    freq_arr = []
    for word_tuple in word_tuples:
        try:
            word = str(word_tuple[0])
            words_arr.append(word)
            freq_arr.append(word_tuple[1])

        except:
            continue
    print words_arr
    normalize(freq_arr)
    print freq_arr
    # code for generating word cloud
    word_count = len(words_arr)
    text = ""
    counts = []
    for i in range(word_count):
        counts.append((words_arr[i], int(freq_arr[i]*100)))
    for i in range(0, word_count):
        for j in range(0, (int)(freq_arr[i] * 100)):
            text = text + words_arr[i] + " "

    tags = make_tags(counts, minsize=20, maxsize=60, colors=COLOR_SCHEMES['audacity'])

    output = join(WORDCLOUD_PATH, 'cloud' + str(topic_id) + '.png')

    create_tag_image(tags=tags, output=output,
                     size=(500, 333),
                     background=(255, 255, 255, 255),
                     layout=3, fontname='PT Sans Regular', rectangular=True)


def execute():
    print 'Started at ' + get_time() + '... ',
    start_timing()

    hot_topics = [4,5,7, 8, 17]
    for topic in hot_topics:
        create_wordcloud(topic)
    print 'Finished'
    stop_timing()


if __name__ == '__main__':
    execute()
