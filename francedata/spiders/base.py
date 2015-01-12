import urlparse

from scrapy.contrib.spiders import CrawlSpider
from scrapy import Request


class BaseSpider(CrawlSpider):
    allowed_domains = [
        "www.assemblee-nationale.fr",
        "www2.assemblee-nationale.fr"
    ]

    start_urls = (
        'http://www2.assemblee-nationale.fr/scrutins/liste/',
    )

    def get_text(self, element, selector):
        return element.select('%s/text()' % selector).extract()[0].strip()

    def get_absolute_path(self, url):
        return urlparse.urlparse(url).path

    def make_url(self, response, url):
        if '://' in url:
            return url

        parse = urlparse.urlparse(response.url)
        return '%s://%s%s' % (parse.scheme, parse.netloc, url)

    def parse_page(self, response):
        pages = response.xpath(
            '//a[contains(@href, "/scrutins/liste/")]/@href').extract()

        for page in pages:
            yield Request(url=self.make_url(response, page),
                          callback=self.parse_page)
