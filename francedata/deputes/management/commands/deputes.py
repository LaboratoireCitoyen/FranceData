import wikipedia
import ijson.backends.yajl2 as ijson

from django.core.management.base import BaseCommand

from ...models import Depute


class Command(BaseCommand):
    def handle(self, *args, **options):
        wikipedia.set_lang('fr')

        for source in args:
            with open(args[0], 'r') as f:
                for items in ijson.items(f, 'deputes'):
                    for item in items:
                        item = item['depute']

                        depute, created = Depute.objects.get_or_create(
                            nom=item['nom_de_famille'], prenom=item['prenom'])

                        depute.numero_departement = item['num_deptmt']
                        depute.url_an = item['url_an']
                        depute.url_nosdeputes = item['url_nosdeputes']

                        if not depute.url_wikipedia:
                            try:
                                depute.url_wikipedia = wikipedia.page(item['nom']).url
                            except wikipedia.exceptions.DisambiguationError:
                                depute.url_wikipedia = wikipedia.page(item['nom'] + ' politique').url
                            except wikipedia.exceptions.PageError:
                                depute.url_wikipedia = ''
                        print depute, depute.url_nosdeputes, depute.url_an, depute.url_wikipedia
                        depute.save()
