# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class FrancedataPipeline(object):
    urls = set()

    def process_item(self, item, spider):
        if 'url' in item:
            if item['url'] in self.urls:
                raise DropItem()
            else:
                self.urls.add(item['url'])

        return item
