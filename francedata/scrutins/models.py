from django.db import models


class Scrutin(models.Model):
    numero = models.IntegerField(db_index=True)
    objet = models.TextField()
    date = models.DateField()
    uri = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    dossier = models.ForeignKey('dossiers.Dossier', null=True, blank=True)

    def __unicode__(self):
        return self.numero

