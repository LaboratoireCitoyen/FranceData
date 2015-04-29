from django.db import models


class Dossier(models.Model):
    uri = models.URLField()
    url = models.URLField()
    titre = models.CharField(max_length=255)

    def __unicode__(self):
        return self.titre
