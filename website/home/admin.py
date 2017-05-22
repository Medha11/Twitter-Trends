from django.contrib import admin

from .models import TopHashTags, TopUserMentions

admin.site.register(TopHashTags)
admin.site.register(TopUserMentions)