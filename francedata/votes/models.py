from django.db import models


class Vote(models.Model):
    DIVISION_ABSTENTION = 0
    DIVISION_POUR = 1
    DIVISION_CONTRE = 2

    DIVISION_CHOICES = (
        (DIVISION_POUR, 'Pour'),
        (DIVISION_CONTRE, 'Contre'),
        (DIVISION_ABSTENTION, 'Abstention'),
    )

    scrutin = models.ForeignKey('scrutins.Scrutin')
    parlementaire = models.ForeignKey('parlementaires.Parlementaire')
    groupe = models.ForeignKey('groupes.Groupe')
    division = models.SmallIntegerField(choices=DIVISION_CHOICES)
