FranceData permet de crawler le site de l'assemblée nationnale pour en extraire
tout les votes, et fournit des modeles Django.

Fait pour la Societe Citoyenne, pour IlsTravaillentPourVous.fr

Downloaded les données
----------------------

Installez scrappy et lancez ces commandes dans le dossier FranceData:

    curl -o deputes.json http://www.nosdeputes.fr/deputes/json
    scrapy crawl parlspider -o parlementaires.json
    scrapy crawl votespider -o votes.json
    scrapy crawl dossierspider -o dossiers.json
    scrapy crawl scrutinspider -o scrutins.json

Installer les données
---------------------

Dans votre projet Django, ajoutez aux ``INSTALLED_APPS``::

    'francedata.parlementaires',
    'francedata.dossiers',
    'francedata.groupes',
    'francedata.scrutins',
    'francedata.votes',

Puis lancez la synchronisation::

    ./manage.py deputes ~/env/src/francedata/deputes.json
    ./manage.py dossiers ~/env/src/francedata/dossiers.json
    ./manage.py groupes ~/env/src/francedata/votes.json
    ./manage.py scrutins ~/env/src/francedata/scrutins.json
    ./manage.py votes ~/env/src/francedata/votes.json
