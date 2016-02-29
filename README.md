FranceData permet de crawler le site de l'assemblée nationnale pour en extraire
tout les votes.

Fait pour la Societe Citoyenne, pour IlsTravaillentPourVous.fr

Mettre à jour les données
-------------------------

Installez le package :

    pip install -e .

Lancez les crawlers pour extraire les données parlementaires :

    francedata_update parl
    francedata_update dossiers
    francedata_update scrutins
    francedata_update votes

Par défaut les résultats sont stockés au format JSON dans le répertoire `data`.
Vous pouvez passer un autre répertoire en 2ème paramètre au script
`francedata_update`.

**Note:** le crawler des votes fonctionne de manière incrémentale.  Il se base
sur le fichier `data/scrutins.json`, il faut donc exécuter le crawler des
scrutins avant.  Par ailleurs il utilise les fichiers dans `data/votes/` pour
éviter de re-crawler des scrutins déjà exportés, ne videz pas ce dossier !

Déployer sur Openshift
----------------------

Installer et configurer RHC puis créer une app comme suit:

    rhc app-create \
        python-2.7 cron-1.4 \
        -a francedata \
        -e OPENSHIFT_PYTHON_WSGI_APPLICATION=wsgi.py \
        --from-code http://github.com/SocieteCitoyenne/FranceData.git \
        --no-git

Un script cron lancera la mise à jour quotidiennement.  Vous pouvez initialiser
les données en exécutant via `rhc ssh`:

    cd $OPENSHIFT_REPO_DIR
    bin/update_all ${OPENSHIFT_DATA_DIR}json

