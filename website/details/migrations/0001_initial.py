# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic_id', models.IntegerField()),
                ('article_head', models.CharField(default=None, max_length=1000)),
                ('article_body', models.CharField(default=None, max_length=5000)),
            ],
        ),
        migrations.AddField(
            model_name='entities',
            name='topic',
            field=models.ForeignKey(to='details.Topic'),
        ),
    ]
