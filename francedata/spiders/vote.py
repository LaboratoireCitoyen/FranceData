# -*- coding: utf-8 -*-
import re
import urlparse

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
        Rule(LinkExtractor(allow=['/scrutins/detail/.*']), 'parse_vote'),
        Rule(LinkExtractor(allow=['/scrutins/liste/.*']), 'parse_scrutin'),
        Rule(LinkExtractor(allow=['/\d+/dossiers/.*']), 'parse_dossier'),
    ]

    def get_text(self, element, selector):
        return element.select('%s/text()' % selector).extract()[0].strip()

    def get_absolute_path(self, url):
        return urlparse.urlparse(url).path

    def parse_dossier(self, response):
        title = response.xpath('/html/head/title/text()').extract()[0]
        titre = re.sub('[^-]*-', '', title).strip()

        item = DossierItem()
        item['url'] = self.get_absolute_path(response.url)
        item['titre'] = titre

        yield item

    def parse_scrutin(self, response):
        for scrutin in response.xpath('//table[@class="scrutins"]/tbody/tr'):
            item = ScrutinItem()
            item['numero'] = self.get_text(scrutin, 'td[1]')
            item['date'] = self.get_text(scrutin, 'td[2]')
            item['objet'] = re.sub('\.[^.]*?$', '', self.get_text(scrutin, 'td[3]'))
            item['url'] = scrutin.select(
                'td/a[contains(text(), "analyse")]/@href')[0].extract()

            try:
                item['dossier_url'] = scrutin.select(
                    'td/a[contains(text(), "dossier")]/@href')[0].extract()
            except IndexError:
                pass

            yield item

    def parse_vote(self, response):
        votes = response.xpath(
            '//div[@class="TTgroupe"]/div/ul[@class="deputes"]/li')

        for sel in response.xpath('//div[@class="TTgroupe"]'):
            nomgroupe = sel.select('p[@class="nomgroupe"]/text()')
            nomgroupe = nomgroupe.extract()[0]
            nomgroupe = re.search('([^(]+)', nomgroupe).groups(1)[0].strip()

            for division in self.DIVISIONS:
                votants = sel.select(
                    'div[@class="%s"]/ul[@class="deputes"]/li' % division)

                for votant in votants:
                    item = VoteItem()
                    item['groupe'] = nomgroupe
                    item['division'] = division
                    item['prenom'] = votant.select(
                        'text()').extract()[0].strip()
                    item['nom'] = votant.select('b/text()').extract()[0].strip()

                    yield item
