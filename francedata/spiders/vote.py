# -*- coding: utf-8 -*-
import re
import urlparse

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from francedata.items import VoteItem, ScrutinItem, DossierItem


class VoteSpider(CrawlSpider):
    DIVISIONS = ['Pour', 'Contre', 'Abstention']

    name = "votespider"
    allowed_domains = [
        "www.assemblee-nationale.fr",
        "www2.assemblee-nationale.fr"
    ]
    start_urls = (
        'http://www2.assemblee-nationale.fr/scrutins/liste/',
    )
    rules = [
        Rule(LinkExtractor(allow=['/scrutins/.*', '/\d+/dossiers/.*']), 'parse_page'),
    ]

    def get_text(self, element, selector):
        return element.select('%s/text()' % selector).extract()[0].strip()

    def get_absolute_path(self, url):
        return urlparse.urlparse(url).path

    def make_url(self, url):
        return 'http://www.assemblee-nationale.fr' + url

    def parse_page(self, response):
        pages = response.xpath(
            '//a[contains(@href, "/scrutins/liste/")]/@href').extract()

        for result in self.parse_scrutins(response):
            yield result

        for page in pages:
            yield Request(url=self.make_url(page), callback=self.parse_page)

    def parse_dossier(self, response):
        title = response.xpath('/html/head/title/text()').extract()[0]
        titre = re.sub('[^-]*-', '', title).strip()

        item = DossierItem()
        item['url'] = self.get_absolute_path(response.url)
        item['titre'] = titre

        yield item

    def parse_scrutins(self, response):
        for scrutin in response.xpath('//table[@class="scrutins"]/tbody/tr'):
            item = ScrutinItem()
            item['numero'] = self.get_text(scrutin, 'td[1]')
            item['objet'] = re.sub('\.[^.]*?$', '', self.get_text(scrutin, 'td[3]'))
            item['url'] = self.get_absolute_path(scrutin.select(
                'td/a[contains(text(), "analyse")]/@href')[0].extract())

            yield Request(url=self.make_url(item['url']),
                          callback=self.parse_scrutin)

            matches = re.search('(\d{1,2})/(\d{1,2})/(\d{1,4})',
                                self.get_text(scrutin, 'td[2]'))
            item['date'] = '-'.join((matches.group(3), matches.group(2),
                                     matches.group(1)))

            try:
                item['dossier_url'] = self.get_absolute_path(scrutin.select(
                    'td/a[contains(text(), "dossier")]/@href')[0].extract())
            except IndexError:
                pass
            else:
                yield Request(url=self.make_url(item['dossier_url']),
                              callback=self.parse_dossier)

            yield item

    def parse_scrutin(self, response):
        votes = response.xpath(
            '//div[@class="TTgroupe"]/div/ul[@class="deputes"]/li')

        for sel in response.xpath('//div[@class="TTgroupe"]'):
            nomgroupe = sel.select('p[@class="nomgroupe"]/text()')
            nomgroupe = nomgroupe.extract()[0]
            nomgroupe = re.search('([^(]+)', nomgroupe).groups(1)[0].strip()

            for division in self.DIVISIONS:
                votants = sel.select(
                    'div[@class="%s"]/ul[@class="deputes"]/li/*[b]' % division)

                for votant in votants:
                    item = VoteItem()
                    item['scrutin_url'] = self.get_absolute_path(response.url)
                    item['groupe'] = nomgroupe
                    item['division'] = division
                    item['prenom'] = votant.select(
                        'text()').extract()[0].strip()
                    item['nom'] = votant.select('b/text()').extract()[0].strip()

                    yield item
