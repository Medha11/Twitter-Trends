from django.shortcuts import render
from django.http import HttpResponse
from home.models import TopHashTags, TopUserMentions
from utilities.live_tweets import *
import json


def detail(request, topic_id):
    context = {}
    context['tsv_name'] = 'topic' + str(topic_id)
    context['topic_name'] = 'Topic ' + str(topic_id)
    context['topic_id'] = topic_id

    topic = Topic.objects.get(topic_id=topic_id)
    if topic.article_head != '':
        context['article'] = True
        context['article_head'] = topic.article_head
        context['article_body'] = topic.article_body

    context['tweets'] = get_tweets(topic_id, 6)
    print context['tweets']
    if len(context['tweets']) > 0:
        context['since_id'] = context['tweets'][0].id
    else:
        context['since_id'] = ''
    context['tsv_name'] = 'tsv/' + context['tsv_name'] + '.tsv'
    return render(request, 'details/page.html', context)


def tweet(request):
    topic_id = request.GET['topic_id']
    try:
        since_id = int(request.GET['since_id'])
    except:
        since_id = None
    tweet = get_tweets(topic_id, 1, since_id)
    reply = {}

    if len(tweet) > 0:
        tweet = tweet[0]
        reply['text'] = tweet.text
        reply['dp_url'] = tweet.dp_url
        reply['name'] = tweet.name
        reply['handle'] = tweet.handle
        reply['tweet_id'] = str(tweet.id)
        reply['date'] = tweet.date

    # get_tweets(keyword, 5)
    return HttpResponse(json.dumps(reply),content_type="application/json")
