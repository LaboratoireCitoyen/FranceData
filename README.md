FranceData permet de crawler le site de l'assemblée nationnale pour en extraire
tout les votes.

Fait pour la Societe Citoyenne, pour IlsTravaillentPourVous.fr

Mettre à jour les données
-------------------------

Lancez les crawlers pour extraire les données parlementaires :

    rm data/parlementaires.json
    scrapy crawl parlspider -o data/parlementaires.json
    rm data/dossiers.json
    scrapy crawl dossierspider -o data/dossiers.json
    rm data/scrutins.json
    scrapy crawl scrutinspider -o data/scrutins.json
    rm data/votes.json
    scrapy crawl votespider -o data/votes.json -a DATADIR=data

Note: le crawler des votes fonctionne de manière incrémentale.  Il se base sur
le fichier `data/scrutins.json`, il faut donc exécuter le crawler des scrutins
avant.  Par ailleurs il utilise les fichiers dans `data/votes/` pour éviter de
re-crawler des scrutins déjà exportés, ne videz pas ce dossier !

Déployer sur Openshift
----------------------

Installer et configurer RHC puis créer une app comme suit:

    rhc app-create \
        python-2.7 cron-1.4 \
        -a francedata \
        -e OPENSHIFT_PYTHON_WSGI_APPLICATION=wsgi.py \
        --from-code http://github.com/SocieteCitoyenne/FranceData.git \
        --no-git

Il est conseillé d'exécuter manuellement le script `bin/update_all` une première
fois pour initialiser les données.  Par la suite un job cron quotidien tiendra
les données à jour.
