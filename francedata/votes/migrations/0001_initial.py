# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deputes', '__first__'),
        ('scrutins', '__first__'),
        ('groupes', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('division', models.SmallIntegerField(choices=[(1, b'Pour'), (2, b'Contre'), (0, b'Abstention')])),
                ('depute', models.ForeignKey(to='deputes.Depute')),
                ('groupe', models.ForeignKey(to='groupes.Groupe')),
                ('scrutin', models.ForeignKey(to='scrutins.Scrutin')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
