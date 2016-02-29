# -*- coding: utf-8 -*-
import json
import re
import os

from scrapy import Request
from scrapy.utils.serialize import ScrapyJSONEncoder

from francedata.items import VoteItem

from .base import BaseSpider


class VoteSpider(BaseSpider):
    name = "votespider"

    DATADIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
        __file__))), 'data')

    DIVISIONS = ['Pour', 'Contre', 'Abstention']
    DIV_SEN = {
        u'Ont voté pour': 'Pour',
        u'Ont voté contre': 'Contre',
        u'Abstentions': 'Abstention'
    }

    def __init__(self, category=None, *args, **kwargs):
        super(VoteSpider, self).__init__(*args, **kwargs)
        if 'DATADIR' in kwargs:
            self.DATADIR = kwargs['DATADIR']

    def vote_file(self, scrutin):
        '''
        Générer le nom de fichier pour les votes d'un scrutin
        '''
        return os.path.join(self.DATADIR, 'votes',
            '%(chambre)s-%(numero)s.json' % scrutin)

    def has_votes(self, scrutin):
        '''
        Vérifie si le fichier de votes d'un scrutin existe
        '''
        return os.path.exists(self.vote_file(scrutin))

    def write_votes(self, scrutin, votes):
        '''
        Enregistre les votes d'un scrutin
        '''
        outfile = self.vote_file(scrutin)

        if len(votes) == 0:
            return

        if not os.path.exists(os.path.dirname(outfile)):
            os.makedirs(os.path.dirname(outfile))

        # Ecriture atomique
        with open('%s.tmp' % outfile, 'w') as f:
            json.dump(votes, f, cls=ScrapyJSONEncoder)
            f.flush()
            os.fsync(f.fileno())

        os.rename('%s.tmp' % outfile, outfile)

    def get_votes(self, scrutin):
        '''
        Lit les votes d'un scrutin
        '''
        infile = self.vote_file(scrutin)

        with open(infile, 'r') as f:
            votes = json.load(f)

        for v in votes:
            yield v

    def set_pipeline(self, pipeline):
        self.pipeline = pipeline

    def start_requests(self):
        '''
        Génère les requêtes pour le crawler pour chaque scrutin n'ayant pas
        (encore) son fichier de votes, et ré-envoie au pipeline les items
        précédemment crawlés
        '''
        infile = os.path.join(self.DATADIR, 'scrutins.json')

        if not os.path.exists(infile):
            raise Exception('Fichier %s inexistant' % infile)

        with open(infile, 'r') as f:
            scrutins = json.loads(f.read())

        reloaded = []
        for scrutin in scrutins:
            if self.has_votes(scrutin):
                # Le scrutin a déjà des votes, on les recharge
                for v in self.get_votes(scrutin):
                    vote = VoteItem()

                    vote['chambre'] = v['chambre']
                    vote['scrutin_url'] = v['scrutin_url']
                    vote['division'] = v['division']
                    if vote['chambre'] == 'AN':
                        vote['prenom'] = v['prenom']
                        vote['nom'] = v['nom']
                    else:
                        vote['parl_url'] = v['parl_url']

                    self.pipeline.process_item(vote, self)
            else:
                # Nouveau scrutin
                if scrutin['chambre'] == 'AN':
                    cb = self.parse_an_votes
                else:
                    cb = self.parse_senat_votes

                req = Request(url=scrutin['url'], callback=cb)
                req.meta['scrutin'] = scrutin
                yield req

    def parse_an_votes(self, response):
        '''
        Parse les votes d'un scrutin AN, les exporte *et* les enregistre dans
        un fichier spécifique au scrutin
        '''
        scrutin = response.meta['scrutin']
        votes = []

        for sel in response.xpath('//div[@class="TTgroupe"]'):
            nomgroupe = sel.xpath('p[@class="nomgroupe"]/text()')
            nomgroupe = nomgroupe.extract()[0]
            nomgroupe = re.search('([^(]+)', nomgroupe).groups(1)[0].strip()

            for division in self.DIVISIONS:
                reps = sel.xpath(
                    '//div[@class="%s"]/ul[@class="deputes"]/li' % division)

                for rep in reps:
                    if len(rep.xpath('b/text()').extract()) == 0:
                        continue

                    vote = VoteItem()
                    vote['chambre'] = 'AN'
                    vote['scrutin_url'] = scrutin['url']
                    vote['division'] = division
                    vote['prenom'] = rep.xpath('text()').extract()[0].strip()
                    vote['nom'] = rep.xpath('b/text()').extract()[0].strip()

                    votes.append(vote)
                    yield vote

        self.write_votes(scrutin, votes)

    def parse_senat_votes(self, response):
        '''
        Parse les votes d'un scrutin Sénat, les exporte *et* les enregistre
        dans un fichier spécifique au scrutin
        '''
        scrutin = response.meta['scrutin']
        votes = []

        for label, division in self.DIV_SEN.items():
            votants = response.xpath(
                ('//p/b/text()[contains(., "%s")]/../..' % label) +
                '/following-sibling::table[1]' +
                '//a[contains(@href,"/senateur/")]/@href')

            for votant in votants:
                vote = VoteItem()
                vote['chambre'] = 'SEN'
                vote['scrutin_url'] = scrutin['url']
                vote['division'] = division
                vote['parl_url'] = self.make_url(response, votant.extract())

                votes.append(vote)
                yield vote

        self.write_votes(scrutin, votes)
