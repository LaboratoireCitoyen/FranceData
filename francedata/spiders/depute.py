# -*- coding: utf-8 -*-
import json
import re
from urllib import quote
import urlparse

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider


class DeputeSpider(CrawlSpider):
    name = "deputespider"
    geocode_url = 'http://api-adresse.data.gouv.fr/search/?q=%s'
    photo_url = 'http://www.nosdeputes.fr/depute/photo/%s'

    allowed_domains = [
        "www.nosdeputes.fr",
        "api-adresse.data.gouv.fr"
    ]

    start_urls = (
        'http://www.nosdeputes.fr/deputes/json',
    )

    def parse(self, response):
        deputes = json.loads(response.body_as_unicode())

        if 'deputes' in deputes:
            deputes = deputes['deputes']

        for depute in deputes:
            if 'depute' in depute:
                depute = depute['depute']

            yield Request(url=depute['url_nosdeputes_api'],
                          callback=self.parse_depute)

    def parse_depute(self, response):
        depute = json.loads(response.body_as_unicode())
        if 'depute' in depute:
            depute = depute['depute']

        depute['photo_url'] = self.photo_url % depute['slug']

        reqs = []

        for ad in depute['adresses']:
            adresse = ad['adresse']

            pattern = ur'Télé(phone|copie)\s*:\s*(\d[0-9 ]+\d)'
            for telm in re.finditer(pattern, adresse):
                if telm.group(1) == 'phone':
                    ad['tel'] = telm.group(2)
                else:
                    ad['fax'] = telm.group(2)

            lad = adresse.lower()
            if not lad.startswith(u'assemblée nationale'):
                trimmed = re.sub(pattern, '', adresse)
                req = Request(url=self.get_geocode_url(trimmed),
                              callback=self.parse_geocode)

                req.meta['depute'] = depute
                req.meta['adresse'] = ad
                reqs.append(req)

        if len(reqs) > 0:
            req = reqs.pop()
            req.meta['requests'] = reqs
            yield req
        else:
            yield depute

    def get_geocode_url(self, q):
        return self.geocode_url % quote(q.encode('utf-8'))

    def parse_geocode(self, response):
        depute = response.meta['depute']
        adresse = response.meta['adresse']
        reqs = response.meta['requests']

        geo = json.loads(response.body_as_unicode())
        if 'features' in geo and len(geo['features']) > 0:
            adresse['geo'] = geo['features'][0]

        if len(reqs) > 0:
            req = reqs.pop()
            req.meta['requests'] = reqs
            yield req
        else:
            yield depute