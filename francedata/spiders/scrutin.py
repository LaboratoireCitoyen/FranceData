# -*- coding: utf-8 -*-
import re
import urlparse

from scrapy import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor

from francedata.items import ScrutinItem

from .base import BaseSpider


class ScrutinSpider(BaseSpider):
    name = "scrutinspider"

    rules = [
        Rule(LinkExtractor(allow=['/scrutins/liste/.*']),
             'parse_scrutins', follow=True),
    ]

    def parse_scrutins(self, response):
        for scrutin in response.xpath('//table[@class="scrutins"]/tbody/tr'):
            item = ScrutinItem()
            item['numero'] = self.get_text(scrutin, 'td[1]')
            item['objet'] = self.get_text(scrutin, 'td[3]').strip(' [')
            item['uri'] = self.get_absolute_path(scrutin.select(
                'td/a[contains(text(), "analyse")]/@href')[0].extract())
            item['url'] = self.make_url(response, item['uri'])

            matches = re.search('(\d{1,2})/(\d{1,2})/(\d{1,4})',
                                self.get_text(scrutin, 'td[2]'))
            item['date'] = '-'.join((matches.group(3), matches.group(2),
                                     matches.group(1)))

            try:
                item['dossier_uri'] = self.get_absolute_path(scrutin.select(
                    'td/a[contains(text(), "dossier")]/@href')[0].extract())
            except IndexError:
                pass
            else:
                item['dossier_url'] = self.make_url(response,
                                                    item['dossier_uri'])

            yield item
