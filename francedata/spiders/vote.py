# -*- coding: utf-8 -*-
import re
import urlparse

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from francedata.items import VoteItem

from .base import BaseSpider


class VoteSpider(BaseSpider):
    DIVISIONS = ['Pour', 'Contre', 'Abstention']

    name = "votespider"

    rules = [
        Rule(LinkExtractor(allow=['/scrutins/liste/.*']), 'parse_page',
             follow=True),
        Rule(LinkExtractor(allow=['/scrutins/detail/.*']), 'parse_votes',
             follow=True),
    ]

    def parse_page(self, response):
        scrutins = response.xpath(
            '//a[contains(@href, "/scrutins/detail/")]/@href').extract()

        for scrutin in set(scrutins):
            yield Request(url=self.make_url(response, scrutin),
                          callback=self.parse_votes)

        for result in super(VoteSpider, self).parse_page(response):
            yield result

    def parse_votes(self, response):
        votes = response.xpath(
            '//div[@class="TTgroupe"]/div/ul[@class="deputes"]/li')

        for sel in response.xpath('//div[@class="TTgroupe"]'):
            nomgroupe = sel.xpath('p[@class="nomgroupe"]/text()')
            nomgroupe = nomgroupe.extract()[0]
            nomgroupe = re.search('([^(]+)', nomgroupe).groups(1)[0].strip()

            for division in self.DIVISIONS:
                votants = sel.xpath(
                    '//div[@class="%s"]/ul[@class="deputes"]/li' % division)

                for votant in votants:
                    item = VoteItem()
                    item['scrutin_url'] = self.get_absolute_path(response.url)
                    item['groupe'] = nomgroupe
                    item['division'] = division
                    item['prenom'] = votant.xpath('text()').extract()[0].strip()
                    item['nom'] = votant.xpath('b/text()').extract()[0].strip()

                    yield item
