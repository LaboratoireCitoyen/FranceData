# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deputes', '0003_auto_20150429_1001'),
    ]

    operations = [
        migrations.AddField(
            model_name='depute',
            name='url_an',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='depute',
            name='url_nosdeputes',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='depute',
            name='url_wikipedia',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
