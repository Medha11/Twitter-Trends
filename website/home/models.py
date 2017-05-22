from django.db import models


class TopHashTags(models.Model):
    hashtag = models.CharField(max_length=200)
    rank = models.IntegerField()

    # ...
    def __unicode__(self):  # __str__ on Python 3
        return self.hashtag


class TopUserMentions(models.Model):
    mentioned_user = models.CharField(max_length=200)
    rank = models.IntegerField()

    # ...
    def __unicode__(self):  # __str__ on Python 3
        return self.mentioned_user
