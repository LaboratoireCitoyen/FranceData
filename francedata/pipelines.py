# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import gzip
import json

from scrapy import signals
from scrapy.exceptions import DropItem
from scrapy.utils.serialize import ScrapyJSONEncoder


class FrancedataPipeline(object):
    has_items = False
    urls = set()

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls(crawler.settings.get('OUTPUT_FILE'))
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def __init__(self, outfile):
        self.json = gzip.open(outfile, 'wb')

    def spider_opened(self, spider):
        self.json.write('[')

        try:
            spider.set_pipeline(self)
        except:
            pass

    def process_item(self, item, spider):
        if 'url' in item:
            if item['url'] in self.urls:
                raise DropItem()
            else:
                self.urls.add(item['url'])

        if self.has_items:
            self.json.write(',\n')

        json.dump(item, self.json, cls=ScrapyJSONEncoder)
        self.has_items = True

        return item

    def spider_closed(self, spider):
        self.json.write(']')
        self.json.close()
