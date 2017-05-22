import re

import nltk
from nltk.corpus import stopwords
from string import digits
from collections import defaultdict


STOPWORDS = ['amp', 'get', 'got', 'hey', 'hmm', 'hoo', 'hop', 'iep', 'let', 'ooo', 'par',
             'pdt', 'pln', 'pst', 'wha', 'yep', 'yer', 'aest', 'didn', 'nzdt', 'via',
             'one', 'com', 'new', 'like', 'great', 'make', 'top', 'awesome', 'best',
             'good', 'wow', 'yes', 'say', 'yay', 'would', 'thanks', 'thank', 'going',
             'new', 'use', 'should', 'could', 'really', 'see', 'want', 'nice',
             'while', 'know', 'free', 'today', 'day', 'always', 'last', 'put', 'live',
             'week', 'went', 'wasn', 'was', 'used', 'ugh', 'try', 'kind', 'http', 'much',
             'need', 'next', 'app', 'ibm', 'appleevent', 'using']


def convert_hashtag(obj):
    return ' '.join(filter(None, re.split(r'([A-Z][a-z]*)', obj.group(0)[1:])))


def process_hashtags(tweet):
    return re.sub(r'([#]\w+)', convert_hashtag, tweet)


def remove_urls(tweet):
    tweet = re.sub(r'(?:\@|http?\://)\S+', '', tweet)
    tweet = re.sub(r'(?:\@|https?\://)\S+', '', tweet)
    return tweet


def create_exclusion_list(tokenized_docs):
    unigrams = [word for doc in tokenized_docs for word in doc if len(word) == 1]
    bigrams = [word for doc in tokenized_docs for word in doc if len(word) == 2]

    return set(stopwords.words('english') + STOPWORDS + unigrams + bigrams)


def get_token_freq(tweets):
    token_frequency = defaultdict(int)
    for tweet in tweets:
        for token in tweet:
            token_frequency[token] += 1
    return token_frequency


def filter_condition(token, stoplist, token_freq):
    return token not in stoplist and token_freq[token] > 1 and len(token.strip(digits)) == len(token)


def filter_tokens(tweets, token_freq):
    stoplist = create_exclusion_list(tweets)
    return [[token for token in tweet if filter_condition(token, stoplist, token_freq)] for tweet in tweets]


def tokenize(tweet):
    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(tweet.lower())


def clean(tweets):
    cleaned_tweets = []
    for tweet in tweets:
        tweet = remove_urls(tweet)
        # tweet = process_hashtags(tweet)
        tweet = tokenize(tweet)
        cleaned_tweets.append(tweet)

    token_freq = get_token_freq(cleaned_tweets)
    cleaned_tweets = filter_tokens(cleaned_tweets, token_freq)

    return cleaned_tweets


if __name__ == '__main__':
    s = 'Hello #JustinBeiber sucks bad app mustn'
    print clean([s, s])
