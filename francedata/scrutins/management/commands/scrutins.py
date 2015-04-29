import json
import re

from django.core.management.base import BaseCommand, CommandError

from francedata.dossiers.models import Dossier
from ...models import Scrutin

NON_DECIMAL = re.compile(r'[^\d.]+')


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.dossiers = {}

        for source in args:
            with open(args[0], 'r') as f:
                items = json.load(f)

                for item in items:
                    self.process_scrutin(item)

    def process_scrutin(self, item):
        numero = NON_DECIMAL.sub('', item['numero'])

        try:
            scrutin = Scrutin.objects.get(numero=numero)
        except Scrutin.DoesNotExist:
            scrutin = Scrutin(numero=numero)

        scrutin.date = item['date']
        scrutin.objet = item['objet']
        scrutin.uri = item['uri']
        scrutin.url = item['url']

        if 'dossier_uri' in item:
            scrutin.dossier_id = self.get_dossier_id(item['dossier_uri'])

        scrutin.save()

    def get_dossier_id(self, uri):
        if uri in self.dossiers:
            return self.dossiers[uri]

        self.dossiers[uri] = Dossier.objects.get(uri=uri).pk

        return self.dossiers[uri]
