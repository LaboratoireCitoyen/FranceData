# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime
import slugify
from django.utils.timezone import utc


def set_slug(apps, schema_editor):
    Dossier = apps.get_model('dossiers', 'Dossier')

    for dossier in Dossier.objects.all():
        dossier.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dossiers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dossier',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, populate_from='titre', always_update=True, unique=True),
            preserve_default=False,
        ),
        migrations.RunPython(set_slug),
        migrations.AlterField(
            model_name='dossier',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, null=True, editable=False),
            preserve_default=False,
        ),
    ]
