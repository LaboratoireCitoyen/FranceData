# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deputes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='depute',
            name='numero_departement',
            field=models.CharField(default='', max_length=2, db_index=True),
            preserve_default=False,
        ),
    ]
