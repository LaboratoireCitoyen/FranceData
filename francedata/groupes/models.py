from django.db import models


class Groupe(models.Model):
    nom = models.CharField(max_length=255)
