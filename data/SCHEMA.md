# Schéma de données

## Fichiers JSON

### data/parlementaires.json

Contient la liste de tous les députés et sénateurs.  Les données sont au format
renvoyé par [les API nosdéputés.fr et nossénateurs.fr][rcapi] avec en complément
les champs suivants:

	<listitem>

		chambre: abréviation de la chambre du parlementaire
			"AN" ou "SEN"

		photo_url: URL vers la photo du parlementaire
			"http://www.nosdeputes.fr/depute/photo/gilda-hobert"

		adresses

			<listitem>

				geo: géocodage de l'adresse
					contient le 1er "feature" de l'objet GeoCodeJSON renvoyé par api-adresse.data.gouv.fr

Voir [la spécification GeoCodeJSON][geocodejson].

[geocodejson]: https://github.com/geocoders/geocodejson-spec
[rcapi]: http://cpc.regardscitoyens.org/trac/wiki/API#Informationdund%C3%A9put%C3%A9particulier

### data/dossiers.json

Contient la liste des dossiers législatifs de l'Assemblée nationale et du Sénat.

	<listitem>

		chambre: abréviation de la chambre parlementaire du dossier
			"AN" ou "SEN"

		url_an: URL du dossier sur le site officiel de l'Assemblée nationale, peut être absent pour un dossier passé uniquement au Sénat
			"http://www.assemblee-nationale.fr/14/dossiers/prorogation_application_loi_55-385.asp"

		url_sen: URL du dossier sur le site officiel du Sénat, peut être absent pour un dossier passé uniquement à l'Assemblée nationale
			"http://www.senat.fr/dossier-legislatif/pjl15-356.html"

		titre: titre du dossier
			"Pouvoirs publics : application de la loi relative à l'état d'urgence"

### data/scrutins.json

Contient la liste des scrutins publics de l'Assemblée nationale et du Sénat.

	<listitem>

		chambre: abréviation de la chambre parlementaire du scrutin
			"AN" ou "SEN"

		numero: numéro de scrutin, attention ce n'est pas toujours un entier
			"1238" ou "2014-121"

		url: URL du scrutin sur le site officiel de la chambre (PK)
			"http://www2.assemblee-nationale.fr/scrutins/detail/(legislature)/14/(num)/1238"

		objet: objet du scrutin
			"L'ensemble du projet de loi prorogeant l'application de la loi n° 55-385 du 3 avril 1955 relative à l'état d'urgence (première lecture)"

		date: date du scrutin au format "YYYY-MM-DD"
			"2016-02-16"

		dossier_url: URL du dossier concerné (FK -> data/dossiers.json:url_an ou url_sen suivant la chambre)
			"http://www.assemblee-nationale.fr/14/dossiers/prorogation_application_loi_55-385.asp"

### data/votes.json

Contient la liste des votes lors de scrutins publics de l'Assemblée nationale et
du Sénat.

	<listitem>

		chambre: abréviation de la chambre parlementaire du vote
			"AN" ou "SEN"

		scrutin_url: URL du scrutin concerné (FK -> data/scrutins.json:url)

		division: vote du parlementaire
			"Pour", "Contre" ou "Abstention"

		prenom: prénom du parlementaire, absent pour les sénateurs
			"Jean-Pierre"

		nom: nom du parlementaire, absent pour les sénateurs
			"Allossery"

		parl_url: URL de la page du parlementaire, absent pour les députés
			"http://www.senat.fr/senateur/abate_patrick14263u.html"
