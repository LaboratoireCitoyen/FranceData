from django.core.urlresolvers import reverse
from django.db import models

import autoslug


class Depute(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    numero_departement = models.CharField(max_length=3, db_index=True)
    url_an = models.URLField(blank=True, null=True)
    url_nosdeputes = models.URLField(blank=True, null=True)
    url_wikipedia = models.URLField(blank=True, null=True)
    slug = autoslug.AutoSlugField(unique=True,
        populate_from=lambda instance: unicode(instance))

    def __unicode__(self):
        return '%s %s' % (self.prenom, self.nom)

    def get_absolute_url(self):
        return reverse('depute_depute_detail', args=(self.slug,))
