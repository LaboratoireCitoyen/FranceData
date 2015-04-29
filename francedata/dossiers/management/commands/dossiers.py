# -*- coding: utf8 -*-
import json
import slugify

from django.core.management.base import BaseCommand

from ...models import Dossier


class Command(BaseCommand):
    def handle(self, *args, **options):
        for source in args:
            with open(args[0], 'r') as f:
                items = json.load(f)

                for item in items:
                    dossier, created = Dossier.objects.get_or_create(
                        uri=item['uri'])

                    dossier.titre = item['titre']
                    dossier.url = item['url']
                    dossier.slug = slugify.slugify(dossier.titre)
                    dossier.save()
