# Bienvenue sur le projet FranceData

FranceData permet de crawler le site de l'assemblée nationnale pour en extraire
tout les votes.

Fait par la Startup Citoyenne, pour le projet IlsTravaillentPourVous.fr.

## Usage

    scrapy crawl votespider -o votes.json
    scrapy crawl dossierspider -o dossiers.json
    scrapy crawl scrutinspider -o scrutins.json
