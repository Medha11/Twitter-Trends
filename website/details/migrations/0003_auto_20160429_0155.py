# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0002_auto_20160429_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='article_body',
            field=models.TextField(default=None, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='article_head',
            field=models.CharField(default=None, max_length=1000, null=True),
        ),
    ]
