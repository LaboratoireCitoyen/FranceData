# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor

from francedata.items import DossierItem

from .base import BaseSpider


class DossierSpider(BaseSpider):
    name = "dossierspider"

    rules = [
        Rule(LinkExtractor(allow=['/scrutins/liste/.*']),
             'parse_an_scrutins', follow=True),
        Rule(LinkExtractor(allow=['/\d+/dossiers/.*']),
             'parse_an_dossier'),
        Rule(LinkExtractor(allow=['/scrutin-public/scr\d+.html']),
             'parse_senat_session', follow=True),
        Rule(LinkExtractor(allow=['/dossier-legislatif/.*']),
             'parse_senat_dossier', follow=True)
    ]

    start_urls = [
        'http://www2.assemblee-nationale.fr/scrutins/liste/',
        'http://www.senat.fr/seancepub.html'
    ]

    def parse_an_scrutins(self, response):
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

    def parse_senat_session(self, response):
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
