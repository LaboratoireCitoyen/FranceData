# -*- coding: utf-8 -*-
import json
import re
from urllib import quote

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider


class ParlSpider(CrawlSpider):
    name = "parlspider"
    geocode_url = 'http://api-adresse.data.gouv.fr/search/?q=%s'
    nd_photo_url = 'http://www.nosdeputes.fr/depute/photo/%s'
    ns_photo_url = 'http://www.nossenateurs.fr/senateur/photo/%s'

    allowed_domains = [
        "www.nosdeputes.fr",
        "www.nossenateurs.fr",
        "api-adresse.data.gouv.fr"
    ]

    start_urls = [
        "http://www.nosdeputes.fr/deputes/json",
        "http://www.nossenateurs.fr/senateurs/json"
    ]

    def parse(self, response):
        reps = json.loads(response.body_as_unicode())

        if 'deputes' in reps:
            reps = reps['deputes']
        elif 'senateurs' in reps:
            reps = reps['senateurs']

        for rep in reps:
            if 'depute' in rep:
                rep = rep['depute']
                yield Request(url=rep['url_nosdeputes_api'],
                              callback=self.parse_parlementaire)
            elif 'senateur' in rep:
                rep = rep['senateur']
                yield Request(url=rep['url_nossenateurs_api'],
                              callback=self.parse_parlementaire)

    def parse_parlementaire(self, response):
        rep = json.loads(response.body_as_unicode())
        if 'depute' in rep:
            rep = rep['depute']
            rep['chambre'] = 'AN'
            rep['photo_url'] = self.nd_photo_url % rep['slug']
        elif 'senateur' in rep:
            rep = rep['senateur']
            rep['chambre'] = 'SEN'
            rep['photo_url'] = self.ns_photo_url % rep['slug']

        reqs = []

        for ad in rep['adresses']:
            adresse = ad['adresse']

            pattern = ur'Télé(phone|copie)\s*:\s*(\d[0-9 ]+\d)'
            for telm in re.finditer(pattern, adresse):
                if telm.group(1) == 'phone':
                    ad['tel'] = telm.group(2)
                else:
                    ad['fax'] = telm.group(2)

            lad = adresse.lower()
            if (not lad.startswith(u'assemblée nationale') and
                    not lad.startswith(u'sénat')):
                trimmed = re.sub(pattern, '', adresse)
                req = Request(url=self.get_geocode_url(trimmed),
                              callback=self.parse_geocode)

                req.meta['rep'] = rep
                req.meta['adresse'] = ad
                reqs.append(req)

        if len(reqs) > 0:
            req = reqs.pop()
            req.meta['requests'] = reqs
            yield req
        else:
            yield rep

    def get_geocode_url(self, q):
        return self.geocode_url % quote(q.encode('utf-8'))

    def parse_geocode(self, response):
        rep = response.meta['rep']
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
            yield rep
