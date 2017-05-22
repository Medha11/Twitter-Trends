# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('details', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='article_body',
            field=models.TextField(default=None, max_length=5000),
        ),
    ]
