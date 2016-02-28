# -*- coding: utf-8 -*-
from scrapy.dupefilters import RFPDupeFilter


class URLScreenFilter(RFPDupeFilter):
    urls = set()

    def request_seen(self, request):
        if not request.url.endswith('#nodedupe') and request.url in self.urls:
            return True
        else:
            self.urls.add(request.url)
            return False
