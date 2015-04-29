import ijson.backends.yajl2 as ijson

from django.core.management.base import BaseCommand

from ...models import Depute


class Command(BaseCommand):
    def handle(self, *args, **options):
        for source in args:
            with open(args[0], 'r') as f:
                for items in ijson.items(f, 'deputes'):
                    for item in items:
                        item = item['depute']

                        depute, created = Depute.objects.get_or_create(
                            nom=item['nom_de_famille'], prenom=item['prenom'])

                        depute.numero_departement = item['num_deptmt']
                        depute.save()
