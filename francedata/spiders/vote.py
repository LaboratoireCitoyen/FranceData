# -*- coding: utf-8 -*-
import re
import urlparse

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from francedata.items import VoteItem

from .base import BaseSpider


class VoteSpider(BaseSpider):
    name = "votespider"

    DIVISIONS = ['Pour', 'Contre', 'Abstention']
    DIV_SEN = {
        u'Ont voté pour': 'Pour',
        u'Ont voté contre': 'Contre',
        u'Abstentions': 'Abstention'
    }

    rules = [
        Rule(LinkExtractor(allow=['/scrutins/liste/.*']), 'parse_an_liste',
             follow=True),
        Rule(LinkExtractor(allow=['/scrutins/detail/.*']), 'parse_an_votes',
             follow=True),
        Rule(LinkExtractor(allow=['/scrutin-public/scr\d+.html']),
             'parse_senat_session', follow=True)
    ]

    start_urls = [
        'http://www2.assemblee-nationale.fr/scrutins/liste/',
        'http://www.senat.fr/seancepub.html'
    ]

    def parse_an_liste(self, response):
        pages = response.xpath(
            '//a[contains(@href, "/scrutins/liste/")]/@href').extract()

        for page in pages:
            yield Request(url=self.make_url(response, page),
                          callback=self.parse_an_liste)

    def parse_an_votes(self, response):
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
                    if len(votant.xpath('b/text()').extract()) == 0:
                        continue

                    item = VoteItem()
                    item['chambre'] = 'AN'
                    item['scrutin_url'] = self.make_url(response, response.url)
                    item['division'] = division
                    item['prenom'] = votant.xpath('text()').extract()[0].strip()
                    item['nom'] = votant.xpath('b/text()').extract()[0].strip()

                    yield item


    def parse_senat_session(self, response):
        for link in response.xpath('//span[@class="blocscrnr"]'):
            href = link.xpath('a/@href')[0].extract()
            yield Request(url=self.make_url(response, href),
                          callback=self.parse_senat_scrutin)

    def parse_senat_scrutin(self, response):
        for label, division in self.DIV_SEN.items():
            votants = response.xpath('//p/b/text()[contains(., "%s")]/../../following-sibling::table[1]//a[contains(@href,"/senateur/")]/@href' % label)

            for votant in votants:
                item = VoteItem()
                item['chambre'] = 'SEN'
                item['scrutin_url'] = self.make_url(response, response.url)
                item['division'] = division
                item['parl_url'] = self.make_url(response, votant.extract())

                yield item