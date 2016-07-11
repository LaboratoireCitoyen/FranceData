# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from francedata.items import DossierItem

from .base import BaseSpider


class DossierSpider(BaseSpider):
    name = "dossierspider"

    rules = [
        Rule(LinkExtractor(allow=['index-dossier']),
             'parse_an_index', follow=True),
        Rule(LinkExtractor(allow=['/(\d+/)?dossiers/[^/]+.asp']),
             'parse_an_dossier'),
        Rule(LinkExtractor(allow=['index-general']),
             'parse_senat_index', follow=True),
        Rule(LinkExtractor(allow=['/dossier-legislatif/[^/+].html']),
             'parse_senat_dossier', follow=True)
    ]

    start_urls = [
        'http://www.assemblee-nationale.fr/14/documents/index-dossier.asp',
        'http://www.senat.fr/dossiers-legislatifs/index-general-projets-propositions-de-lois.html' # noqa
    ]

    def parse_an_index(self, response):
        an_dossiers = response.xpath(
            '//a[contains(@href, "/dossiers/")]/@href').extract()

        for dossier in set(an_dossiers):
            yield Request(url=self.make_url(response, dossier),
                          callback=self.parse_an_dossier)

    def parse_an_dossier(self, response):
        titre = response.xpath('//title/text()').extract()[0]

        item = DossierItem()
        item['chambre'] = 'AN'
        item['url_an'] = self.make_url(response, response.url)
        item['titre'] = titre.replace(u'Assemblée nationale - ',
                                      '').capitalize()

        url_sen = response.xpath(
            '//a[contains(@href, "senat.fr/dossier-legislatif/")]/@href')
        if len(url_sen):
            item['url_sen'] = self.make_url(response, url_sen[0].extract())

        yield item

    def parse_senat_index(self, response):
        sen_dossiers = response.xpath(
            '//a[contains(@href, "/dossier-legislatif/")]/href').extract()

        for dossier in set(sen_dossiers):
            yield Request(url=self.make_url(response, dossier),
                          callback=self.parse_senat_dossier)

    def parse_senat_dossier(self, response):
        titre = response.xpath('//title/text()').extract()[0]

        item = DossierItem()
        item['chambre'] = 'SEN'
        item['url_sen'] = self.make_url(response, response.url)
        item['titre'] = titre.replace(u' - Sénat', '').capitalize()

        url_an = response.xpath(
            '//a[contains(@href, "assemblee-nationale.fr")]' +
            '[contains(@href, "/dossiers/")]/@href')
        if len(url_an):
            item['url_an'] = self.make_url(response, url_an[0].extract())

        yield item
