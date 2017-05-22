from django.db import models


class Topic(models.Model):
    topic_id = models.IntegerField()
    article_head = models.CharField(max_length=1000, default=None, blank=True)
    article_body = models.TextField(max_length=5000, default=None, blank=True)

    def __unicode__(self):  # __str__ on Python 3
        return str(self.topic_id)


class Entities(models.Model):
    topic = models.ForeignKey('Topic')
    entity = models.CharField(max_length=100)

    def __unicode__(self):  # __str__ on Python 3
        return self.entity