# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrutinItem(scrapy.Item):
    numero = scrapy.Field()
    objet = scrapy.Field()
    date = scrapy.Field()
    url = scrapy.Field()
    dossier_url = scrapy.Field()


class DossierItem(scrapy.Item):
    url = scrapy.Field()
    titre = scrapy.Field()


class VoteItem(scrapy.Item):
    scrutin_url = scrapy.Field()

    prenom = scrapy.Field()
    nom = scrapy.Field()
    groupe = scrapy.Field()
    division = scrapy.Field()
