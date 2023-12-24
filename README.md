# Mini Projet Python

*Par Antonin MANSOUR et Zackary SAADA*

## Présentation générale

Ce projet est un Dashboard représentant le **montant des loyers** des appartements et maisons en **€/m2** en **fonction des communes de France** en 2022.

Le jeu de données est tiré du site du site **data.gouv.fr** : <https://www.data.gouv.fr/fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2022/>

Les liens utilisés pour accéder aux données du site sont stables  et ne seront donc jamais soumis au changement.

## Guide utilisateur

### Installation

Pour déployer le Dashboard, il est préférable que **Git** soit installé sur la machine cible. Ouvrez un terminal dans le dossier où vous voulez télécharger l'application puis tapez les quatre commandes suivantes :

```bash
git clone https://git.esiee.fr/mansouan/antoninzackarypythonminiproject.git

cd antoninzackarypythonminiproject

python -m pip install -r requirements.txt
#cette ligne peut prendre un peu de temps à se terminer, veuillez bien patienter le téléchargement avant de lancer la suivante

python main.py
```

> **Note** : Télécharger le dossier directement fonctionnera également, mais il faudra l'extraire et ouvrir un terminal dedans pour y taper les commandes `python -m pip install -r requirements.txt` et `python main.py`.

L'application lancera un serveur local accessible à l'adresse <http://127.0.0.1:8050/> contenant le Dashboard. Il est possible d'ouvrir la page en maintenant la touche **Ctrl** et en **cliquant** sur l'URL dans le Terminal.
  
Maintenir la touche **Ctrl** puis appuyer sur **C** ou **fermer la console** mettra fin au serveur.

### Utilisation

La page web permet de consulter un **histogramme** du nombre de communes par tranche de loyer moyen en €/m².
En scrollant vers le bas, il est possible de consulter une **carte de France colorée** en fonction du prix du loyer par département.
Quatre **boutons radio** sont disponibles en haut de la page pour **changer le jeu de données** et passer des loyers maison aux loyers des différents types d'appartement. L'histogramme et la carte seront actualisés conformément au jeu de données choisi.

## Rapport d'analyse

Nous remarquons qu'une grande partie des communes propose un loyer **maison** situé entre **6 et 9 €/m²**, avec un pic de communes entre 7 et 8 €/m².

Cette fourchette augmente pour les **appartements**, jusqu'à atteindre des fourchettes de **9 à 12€/m²** pour les T1 et T2, avec un pic de communes à 10-11€/m².

Ces informations démontrent que le prix du loyer réduit considérablement lorsque la taille du logement en m² augmente.

Nous remarquons également grâce à la carte que les régions où le loyer est le plus élevé sont l'**Ile de France** et la **Haute Savoie**, tandis que les loyers les moins chers sont situés dans la **[diagonale du vide](https://fr.wikipedia.org/wiki/Diagonale_du_vide)**.

## Guide développpeur

Le code est exécuté à partir du `main.py`. D'abord, créer le dataFrame, via la fonction `getDataFrame(url : str)` dans `Data.py` qui retourne le dataFrame à partir de l'URL. Les URLs utilisées retournent les loyers moyens par communes, sous format CSV.

Plusieurs autres fichiers s'articulent autour :

- `histogramme.py` : qui contient la fonction `getHistogramme(dataFrame: DataFrame)`, qui retourne l'histogramme à partir du dataFrame passé en paramètre.
- `map.py` : qui contient la fonction `getMap(dataFrame: DataFrame)` qui retourne la carte à partir du dataFrame passé en paramètre.

Dans `main.py`, on s'occupe de plusieurs autres choses.

D'abord, on crée l'histogramme et la carte pour chacun des 4 sources de données (maison, appartements T1 et T2, appartements T3 et plus, tous les appartements), afin d'éviter les temps de latence lorsqu'on change de source de données dans le menu.

Ensuite, on crée le layout du dashboard. Dans ce layout, on crée des objets de type `Graph` et `Ifram` vides. Ensuite, lorsqu'on sélectionne la source de données (par défaut maison), la fonction `update_data_source()` s'occupe de retourner les bons graphiques, et le `callback` les charge dans ces objets.

Si on veut ajouter un jeu de données, il y a plusieurs étapes à suivre (attention, le jeu de données doit être sur le même modèle que les autres (mêmes noms de colonnes, mêmes types de données, etc...)) :

- Ajouter l'url au dictionnaire `DATA_URLS`.
- Créer une option dans le radio bouton du layout, en prenant soin d'utiliser la même clé que le dictionnaire.

Si on veut ajouter un diagramme, il y a plusieurs étapes :

- Créer une fonction get_nouveau_diagrammme, qui s'occupe de créer le nouveau diagramme.
- Appeler la fonction créée dans la boucle `for` du `main.py`.
- Ajouter un objet au type correspondant, dans le layout, avec un titre, une légende, etc...
- Ajouter la sélection du diagramme dans la fonction `update_data_source`.

### Diagramme d'appels de fonctions

[![](https://mermaid.ink/img/pako:eNpVUMtOwzAQ_BVrT46U9gNyQNCGUpB6ghtGaLE3TYRjW44tVFX9d9YkIHqxrHns7M4ZtDcEDXTWf-keYxLipVVOuTs54uDW4VQJsVrdCLGRLSYsAJMLtpUHDNdQK_fDlPwx4jjSNfUkMYS1xZPPqSoZm4W4f1VwpFTm79hHMkdbKXhTbrsodrOC06TpZqpdqIeZ-pf6J1FuL29LpkZrP1B__t7yyJ4cDCZ65wcnn6MmPjjUgkeEvtihhpEil2C4nrNyQihIPY2koOGvoQ6zTQqUu7AUc_LPJ6ehSTFTvUxvBywrQdOhnRglMyQfD3PlP81fvgFimHod?type=png)](https://mermaid.live/edit#pako:eNpVUMtOwzAQ_BVrT46U9gNyQNCGUpB6ghtGaLE3TYRjW44tVFX9d9YkIHqxrHns7M4ZtDcEDXTWf-keYxLipVVOuTs54uDW4VQJsVrdCLGRLSYsAJMLtpUHDNdQK_fDlPwx4jjSNfUkMYS1xZPPqSoZm4W4f1VwpFTm79hHMkdbKXhTbrsodrOC06TpZqpdqIeZ-pf6J1FuL29LpkZrP1B__t7yyJ4cDCZ65wcnn6MmPjjUgkeEvtihhpEil2C4nrNyQihIPY2koOGvoQ6zTQqUu7AUc_LPJ6ehSTFTvUxvBywrQdOhnRglMyQfD3PlP81fvgFimHod)

*Nous déclarons sur l’honneur que l'entièreté code fourni a été produit par nous mêmes.*
