# -*- coding: utf-8 -*-
import json
import re
import urlparse

from scrapy import Request
from scrapy.contrib.spiders import CrawlSpider


class DeputeSpider(CrawlSpider):
    name = "deputespider"

    allowed_domains = [
        "www.nosdeputes.fr"
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
        depute = json.loads(response.body_as_unicode());
        if 'depute' in depute:
            depute = depute['depute']

        yield depute
