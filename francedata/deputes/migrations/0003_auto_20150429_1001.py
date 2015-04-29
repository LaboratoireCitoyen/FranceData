# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deputes', '0002_depute_numero_departement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='depute',
            name='numero_departement',
            field=models.CharField(max_length=3, db_index=True),
            preserve_default=True,
        ),
    ]
