from django.core.urlresolvers import reverse
from django.db import models

import autoslug


class Parlementaire(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    chambre = models.CharField(max_length=255)
    numero_departement = models.CharField(max_length=3, db_index=True)
    url_officielle = models.URLField(blank=True, null=True)
    url_rc = models.URLField(blank=True, null=True)
    url_wikipedia = models.URLField(blank=True, null=True)
    slug = autoslug.AutoSlugField(unique=True,
        populate_from=lambda instance: unicode(instance))

    def __unicode__(self):
        mandat = 'Député' if self.chambre == 'AN' else 'Sénateur'
        return '%s %s %s' % (mandat, self.prenom, self.nom)

    def get_absolute_url(self):
        return reverse('parlementaire_parlementaire_detail', args=(self.slug,))
