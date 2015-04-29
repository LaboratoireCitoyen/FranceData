import ijson.backends.yajl2 as ijson

from django.core.management.base import BaseCommand

from ...models import Groupe


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.groups = list(Groupe.objects.values_list('nom', flat=True))

        for source in args:
            with open(args[0], 'r') as f:
                for item in ijson.items(f, 'item'):
                    if item['groupe'] in self.groups:
                        continue

                    groupe, created = Groupe.objects.get_or_create(
                        nom=item['groupe'])

                    self.groups.append(item['groupe'])
