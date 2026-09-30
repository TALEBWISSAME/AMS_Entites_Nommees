# AMS — Entités nommées dans un corpus d’Isaac Asimov

## Présentation

Ce projet universitaire de traitement automatique du langage analyse un corpus littéraire d’Isaac Asimov. Il vise à extraire des informations permettant progressivement d’étudier les personnages et leurs relations, puis d’aboutir à un réseau de personnages.

## Travail actuel

Le TP actuel porte sur la détection d’entités nommées. L’inspection technique des trois PDF est réalisée ; les traitements NLP ne sont pas commencés.

## Objectifs du TP actuel

- **L** : liste générale d’entités nommées candidates, en vrac et sans filtrage de raffinement.
- **LP** : personnes/personnages identifiés à partir de L par raffinements.
- **LL** : lieux et catégories prévues par le sujet : cités, organisations, universités, villes et planètes.

## Méthode générale prévue

Corpus → lecture → prétraitement → tokenisation → n-grammes → fréquences / modèle de langue → candidats → L → raffinements → LP / LL.

Cette chaîne pourra être ajustée selon les résultats expérimentaux et les documents du professeur. Les étapes détaillées figurent dans [le plan de réalisation](docs/PLAN_REALISATION.md).

## Architecture du dépôt

```text
corpus/                       # Local uniquement, ignoré par Git
src/entites_nommees/README.md  # Plan de développement
results/entites_nommees/README.md
results/extracted/             # TXT bruts locaux, ignorés par Git
rapport/README.md
docs/PLAN_REALISATION.md
docs/DECISIONS.md
README.md
CONTEXTE_PROJET.md
.gitignore
```

## Corpus

Le corpus n'est pas inclus dans le dépôt pour des raisons de droits et conformément aux consignes du cours.

Les textes fournis par le professeur doivent être placés localement dans `corpus/`, à créer après un clonage du dépôt. Ce dossier est ignoré par Git et ne doit jamais être publié. Les originaux ne doivent pas être modifiés. Certaines pages seulement ont été conservées : des paragraphes ou mots peuvent être coupés. Ne pas reproduire de longs extraits dans la documentation.

## Installation

Le projet utilise Python et `pdfplumber==0.11.9` pour l’inspection PDF. Installer la dépendance avec `python -m pip install -r requirements.txt`. Aucun outil linguistique n’est choisi à ce stade.

## Utilisation

Depuis la racine : `python src/entites_nommees/corpus_reader.py`.

Pour produire les trois extractions brutes UTF-8 : `python src/entites_nommees/corpus_reader.py --export`. Elles sont stockées dans `results/extracted/`, ignoré par Git, et régénérées à chaque exécution de cette commande. Ce sont des données intermédiaires locales, sans nettoyage, pas des résultats finaux. Les frontières des pages sont conservées par le caractère technique `\f` (U+000C).

Depuis un autre dossier, utiliser le chemin absolu du script. Le programme retrouve le corpus à partir de son propre emplacement, affiche les statistiques et un aperçu limité, sans écrire les textes extraits. Voir [les conventions de comptage](src/entites_nommees/README.md).

## État du projet

Le prétraitement conservateur Bash/AWK est disponible : `bash scripts/preprocess.sh` depuis Git Bash. Tests : `bash tests/test_preprocess.sh`. Les sorties locales `results/processed/` sont ignorées par Git. Voir [les règles, résultats et limites](docs/PRETRAITEMENT.md). La tokenisation n’est pas commencée.

Inspection technique réalisée : 344 pages sur les trois PDF, toutes avec du texte extractible. Prétraitement conservateur exécuté ; aucune tokenisation ni liste L/LP/LL.

Pour reprendre le travail avec ChatGPT ou Codex, consulter [le contexte du projet](CONTEXTE_PROJET.md) et [les décisions techniques](docs/DECISIONS.md).

Les six PDF pédagogiques et l’illustration du réseau convertie en PDF sont disponibles dans `docs/`. Voir [la synthèse des consignes du professeur](docs/CONSIGNES_PROF.md) pour leur rôle et les références de pages. Le rendu du TP comprend un rapport de 2 à 3 pages, les listes L/LP/LL et les statistiques du corpus. Le périmètre confirmé comprend uniquement Fondation, Fondation et empire et Seconde Fondation, dont les trois PDF sont présents dans `corpus/`.
