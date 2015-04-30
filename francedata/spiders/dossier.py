# -*- coding: utf-8 -*-
import re
import urlparse

from scrapy import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor

from francedata.items import DossierItem

from .base import BaseSpider


class DossierSpider(BaseSpider):
    name = "dossierspider"

    rules = [
        Rule(LinkExtractor(allow=['/scrutins/liste/.*']),
             'parse_page', follow=True),
        Rule(LinkExtractor(allow=['/\d+/dossiers/.*']),
             'parse_dossier'),
    ]

    def parse_page(self, response):
        dossiers = response.xpath(
            '//a[contains(@href, "/dossiers/")]/@href').extract()

        for dossier in set(dossiers):
            yield Request(url=self.make_url(response, dossier),
                          callback=self.parse_dossier)

        for result in super(DossierSpider, self).parse_page(response):
            yield result

    def parse_dossier(self, response):
        titre = response.xpath('//title/text()').extract()[0]

        item = DossierItem()
        item['uri'] = self.get_absolute_path(response.url)
        item['url'] = self.make_url(response, response.url)
        item['titre'] = titre.replace(u'Assemblée nationale - ', '').capitalize()

        yield item
