import urlparse

from scrapy.contrib.spiders import CrawlSpider


class BaseSpider(CrawlSpider):
    allowed_domains = [
        "www.assemblee-nationale.fr",
        "www2.assemblee-nationale.fr",
        "www.senat.fr"
    ]

    def get_text(self, element, selector):
        return element.xpath('%s/text()' % selector).extract()[0].strip()

    def get_absolute_path(self, url):
        return urlparse.urlparse(url).path

    def make_url(self, response, href):
        if '://' in href:
            return href

        if href.startswith('/'):
            parse = urlparse.urlparse(response.url)
            return '%s://%s%s' % (parse.scheme, parse.netloc, href)

        return urlparse.urljoin(response.url, href)
