# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DossierItem(scrapy.Item):
    url = scrapy.Field()
    chambre = scrapy.Field()
    titre = scrapy.Field()


class ScrutinItem(scrapy.Item):
    url = scrapy.Field()
    chambre = scrapy.Field()
    numero = scrapy.Field()
    objet = scrapy.Field()
    date = scrapy.Field()
    dossier_url = scrapy.Field()


class VoteItem(scrapy.Item):
    scrutin_url = scrapy.Field()
    chambre = scrapy.Field()
    nom = scrapy.Field()
    prenom = scrapy.Field()
    groupe = scrapy.Field()
    division = scrapy.Field()
    parl_url = scrapy.Field()
