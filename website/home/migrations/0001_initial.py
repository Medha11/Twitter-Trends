# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopHashTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashtag', models.CharField(max_length=200)),
                ('rank', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TopUserMentions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mentioned_user', models.CharField(max_length=200)),
                ('rank', models.IntegerField()),
            ],
        ),
    ]
