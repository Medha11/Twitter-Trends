import tweepy
import os
from utilities.time_management import *
from utilities.config import *
import django
os.environ["DJANGO_SETTINGS_MODULE"] = "portal.settings"
django.setup()

from details.models import Entities, Topic

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class Tweet:

    def __init__(self, id, number, text, name, handle, date, dp_url):
        self.id = id
        self.number = number
        self.text = text
        self.name = name
        self.handle = handle
        self.date = date
        self.dp_url = dp_url


def get_tweets(topic_id, count, since_id=None):
    tweets = []
    try: 
        api = tweepy.API(auth)
        topic = Topic.objects.get(topic_id=topic_id)
        keyword = Entities.objects.filter(topic=topic)[0]
        new_tweets = api.search(q=keyword, count=count, since_id=since_id, lang='en')
        
        cnt = 1
        for tweet in new_tweets:
            id = tweet.id
            text = tweet.text
            name = tweet.author.name
            handle = '@' + tweet.author.screen_name
            dp_url = tweet.author.profile_image_url_https
            date = get_tweet_date_time_string(convert_datetime_to_local(tweet.created_at.replace(tzinfo=pytz.UTC)))

            tweets.append(Tweet(id, cnt, text, name, handle, date, dp_url))

            cnt += 1
    except: None

    return tweets
