# -*- coding: utf-8 -*-

import logging
import os
import sys

import scrapy
from scrapy.crawler import CrawlerProcess

from spiders.dossier import DossierSpider
from spiders.parl import ParlSpider
from spiders.scrutin import ScrutinSpider
from spiders.vote import VoteSpider


logger = logging.getLogger('francedata')
commands = {
    'parl': { 'class': ParlSpider, 'output': 'parlementaires.json' },
    'dossiers': { 'class': DossierSpider, 'output': 'dossiers.json' },
    'scrutins': { 'class': ScrutinSpider, 'output': 'scrutins.json' },
    'votes': { 'class': VoteSpider, 'output': 'votes.json' },
}


def crawl(spider, datadir, output, **spargs):
    tmpfile = os.path.join(datadir, 'tmp-%s' % output)
    outfile = os.path.join(datadir, output)

    process = CrawlerProcess({
        'BOT_NAME': 'francedata',
        'LOG_LEVEL': 'INFO',
        'TELNETCONSOLE_ENABLED': False,
        'FEED_URI': tmpfile,
        'FEED_FORMAT': 'json',
        'DUPEFILTER_CLASS': 'francedata.filters.URLScreenFilter',
        'ITEM_PIPELINES': {
            'francedata.pipelines.FrancedataPipeline': 500
        },
    })

    process.crawl(spider, **spargs)

    if os.path.exists(tmpfile):
        os.remove(tmpfile)

    logger.info('** Start crawling with %s **' % spider)
    process.start()

    if os.path.exists(outfile):
        os.remove(outfile)

    os.rename(tmpfile, outfile)

    logger.info('** Finished crawling with %s **' % spider)


def update():
    if len(sys.argv) < 2:
        print 'Usage: %s command [datadir]'
        sys.exit(1)

    cmd = sys.argv[1]
    if len(sys.argv) > 2:
        datadir = sys.argv[2]
    else:
        datadir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
            'data')

    if cmd not in commands:
        print 'Unknown command "%s"' % cmd
        sys.exit(1)

    command = commands[cmd]
    crawl(command['class'], datadir, command['output'], DATADIR=datadir)
