# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dossiers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scrutin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.IntegerField(db_index=True)),
                ('objet', models.TextField()),
                ('date', models.DateField()),
                ('uri', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('dossier', models.ForeignKey(blank=True, to='dossiers.Dossier', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
