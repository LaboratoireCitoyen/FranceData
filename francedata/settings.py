# -*- coding: utf-8 -*-

# Scrapy settings for francedata project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'francedata'

SPIDER_MODULES = ['francedata.spiders']
NEWSPIDER_MODULE = 'francedata.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'francedata (+http://www.yourdomain.com)'

CLOSESPIDER_ITEMCOUNT = 3

EXTENSIONS = {
    'scrapy.contrib.closespider.CloseSpider': 4,
}
