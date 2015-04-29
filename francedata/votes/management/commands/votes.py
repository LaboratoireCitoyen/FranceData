import re

from optparse import make_option

import ijson.backends.yajl2 as ijson

from django.core.management.base import BaseCommand, CommandError

from scrutins.models import Scrutin
from deputes.models import Depute
from groupes.models import Groupe
from ...models import Vote


class Command(BaseCommand):
    DIVISIONS = {
        'Pour': Vote.DIVISION_POUR,
        'Contre': Vote.DIVISION_CONTRE,
        'Abstention': Vote.DIVISION_ABSTENTION,
    }

    option_list = BaseCommand.option_list + (
        make_option('--insert',
            action='store_true',
            dest='insert',
            default=False,
            help='Insert all votes - for quicker install'),
        )

    def handle(self, *args, **options):
        self.insert = options['insert']

        self.deputes = {}
        for depute in Depute.objects.values_list('nom', 'prenom', 'pk'):
            self.deputes[depute[0]+depute[1]] = depute[2]

        self.scrutins = {}
        for scrutin in Scrutin.objects.values_list('uri', 'pk'):
            self.scrutins[scrutin[0]] = scrutin[1]

        self.groupes = {}
        for groupe in Groupe.objects.values_list('pk', 'nom'):
            self.groupes[groupe[1]] = groupe[0]

        print 'loaded cache'

        votes = []

        for source in args:
            with open(source, 'r') as f:
                print 'opening json'
                items = ijson.items(f, 'item')
                print 'loaded json'

                for item in items:
                    try:
                        votes.append(self.get_vote(item))
                    except KeyError:
                        pass

                    if not self.insert:
                        continue

                    if len(votes) > 20000:
                        Vote.objects.bulk_create(votes)
                        votes = []
                        print 'flushing'

        if self.insert:
            Vote.objects.bulk_create(votes)

    def get_vote(self, item):
        kwargs = dict(depute_id=self.get_depute_id(item),
                      scrutin_id=self.get_scrutin_id(item['scrutin_uri']))

        if self.insert:
            vote = Vote(**kwargs)
        else:
            try:
                vote = Vote.objects.get(**kwargs)
            except Vote.DoesNotExist:
                vote = Vote(**kwargs)
            except Vote.MultipleObjectsReturned:
                duplicates = Vote.objects.filter(**kwargs)
                Vote.objects.filter(
                    pk__in=duplicates.values_list('pk', flat=True)[1:]
                ).delete()
                vote = Vote(**kwargs)

        vote.groupe_id = self.get_groupe_id(item['groupe'])
        vote.division = self.DIVISIONS[item['division']]

        return vote

    def get_depute_id(self, item):
        return self.deputes[item['nom'] + item['prenom']]

    def get_scrutin_id(self, url):
        return self.scrutins[url]

    def get_groupe_id(self, nom):
        return self.groupes[nom]
