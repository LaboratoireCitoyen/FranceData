# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deputes', '0005_circonscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Circonscription',
        ),
    ]
