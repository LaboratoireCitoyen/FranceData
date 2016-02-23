FranceData permet de crawler le site de l'assemblée nationnale pour en extraire
tout les votes.

Fait pour la Societe Citoyenne, pour IlsTravaillentPourVous.fr

Downloaded les données
----------------------

Installez scrappy et lancez ces commandes dans le dossier FranceData:

    scrapy crawl parlspider -o data/parlementaires.json
    scrapy crawl votespider -o data/votes.json
    scrapy crawl dossierspider -o data/dossiers.json
    scrapy crawl scrutinspider -o data/scrutins.json

Installer les données
---------------------

FranceData inclu un serveur d'API simple basé sur django-representatives et
django-representatives-votes.

Dans ``apiserver/``, synchronisez la base de données (fichier SQLite3 local par
défaut)::

    ./manage.py migrate

Puis, lancez le serveur::

    ./manage.py
