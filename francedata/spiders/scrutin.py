# -*- coding: utf-8 -*-
import re

from scrapy import Request
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor

from francedata.items import ScrutinItem

from .base import BaseSpider

_months = {
    u"janvier": 1,
    u"février": 2,
    u"mars": 3,
    u"avril": 4,
    u"mai": 5,
    u"juin": 6,
    u"juillet": 7,
    u"août": 8,
    u"septembre": 9,
    u"octobre": 10,
    u"novembre": 11,
    u"décembre": 12
}


class ScrutinSpider(BaseSpider):
    name = "scrutinspider"

    rules = [
        Rule(LinkExtractor(allow=['/scrutins/liste/.*']),
             'parse_an_scrutins', follow=True),
        Rule(LinkExtractor(allow=['/scrutin-public/scr\d+.html']),
             'parse_senat_session', follow=True)
    ]

    start_urls = [
        'http://www2.assemblee-nationale.fr/scrutins/liste/',
        'http://www.senat.fr/seancepub.html'
    ]

    def parse_an_scrutins(self, response):
        for scrutin in response.xpath('//table[@class="scrutins"]/tbody/tr'):
            item = ScrutinItem()
            item['chambre'] = 'AN'
            item['numero'] = self.get_text(scrutin, 'td[1]').rstrip('*')
            item['objet'] = self.get_text(scrutin, 'td[3]').strip(
                ' [').capitalize()
            item['url'] = self.make_url(response, scrutin.select(
                'td/a[contains(text(), "analyse")]/@href')[0].extract())

            matches = re.search('(\d{1,2})/(\d{1,2})/(\d{1,4})',
                                self.get_text(scrutin, 'td[2]'))
            item['date'] = '-'.join((matches.group(3), matches.group(2),
                                     matches.group(1)))

            try:
                item['dossier_url'] = self.make_url(response, scrutin.select(
                    'td/a[contains(text(), "dossier")]/@href')[0].extract())
            except IndexError:
                pass

            yield item

    def parse_senat_session(self, response):
        for bloc in response.xpath('//div[@class="blocscr"]'):
            href = bloc.xpath('span[@class="blocscrnr"]/a/@href')[0].extract()
            dlink = bloc.xpath(
                '//a[contains(@href, "/dossier-legislatif/")]/@href')

            req = Request(url=self.make_url(response, href),
                          callback=self.parse_senat_scrutin)
            if len(dlink):
                req.meta['dlink'] = dlink[0].extract()

            yield req

    def parse_senat_scrutin(self, response):
        item = ScrutinItem()
        item['chambre'] = 'SEN'

        titlediv = response.xpath('//div[@class="title"]')[0]
        title = self.get_text(titlediv, 'h1')

        matches = re.search(ur'scrutin-public/(\d+)/scr.*\.html', response.url)
        session = matches.group(1)

        matches = re.search(ur'^Scrutin n° (\d+) - séance du (.*)$', title)
        item['numero'] = '%s-%s' % (session, matches.group(1))

        objet = self.get_text(response, '//div[@id="wysiwyg"]/p/i')
        item['objet'] = objet

        item['url'] = response.url

        dmatches = re.search(r'^(\d+) (\D+) (\d+)$', matches.group(2))
        item['date'] = '%04d-%02d-%02d' % (int(dmatches.group(3)),
                                           _months[dmatches.group(2)],
                                           int(dmatches.group(1)))

        if 'dlink' in response.meta:
            item['dossier_url'] = response.meta['dlink']
        else:
            dlink = response.xpath(
                '//a[contains(@href, "/dossier-legislatif/")]/@href')

            if len(dlink):
                item['dossier_url'] = self.make_url(response,
                    dlink[0].extract())

        yield item
