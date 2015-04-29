from django.db import models

import autoslug


class Dossier(models.Model):
    uri = models.URLField()
    url = models.URLField()
    titre = models.CharField(max_length=255)
    slug = autoslug.AutoSlugField(unique=True, populate_from='titre')

    def __unicode__(self):
        return self.titre
