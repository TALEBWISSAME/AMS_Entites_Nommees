# Contexte du projet

## Objectifs

Projet universitaire de TAL sur des romans d’Isaac Asimov, visant progressivement la construction d’un réseau de personnages. Le travail actuel se limite au TP « Entités Nommées ». Les supports généraux et l’énoncé de septembre 2026 sont maintenant disponibles dans `docs/` ; voir [la synthèse des consignes](docs/CONSIGNES_PROF.md). Les méthodes présentées pour la suite ne sont pas automatiquement des exigences du TP actuel.

## Exigences confirmées par l’énoncé

Travail en binômes ; Python est autorisé. Le rendu demandé est un rapport de **2 à 3 pages sur les algorithmes**, accompagné des **listes L, LP, LL et des statistiques du corpus**. L’énoncé prévoit deux séances, sans date précise de dépôt dans le document fourni.

Le périmètre confirmé par l’étudiant comprend uniquement **Fondation**, **Fondation et empire** et **Seconde Fondation**. Leurs trois PDF sont conservés dans `corpus/` ; les deux romans supplémentaires en ont été supprimés à sa demande.

- **L** : liste générale de candidats entités nommées, en vrac et sans filtrage de raffinement.
- **LP** : liste des personnes/personnages, obtenue à partir de L avec des raffinements.
- **LL** : liste des lieux/catégories prévues par le sujet, notamment cités, organisations, universités, villes et planètes. Elle exploitera L, LP et les informations disponibles selon une méthode à décider.

## Corpus et contraintes

Les textes sont fournis par le professeur et restent exclusivement dans le dossier local `corpus/`, ignoré par Git. Ne jamais les publier ni modifier les originaux.

Le corpus n'est pas inclus dans le dépôt pour des raisons de droits et conformément aux consignes du cours.

Seules les pages impaires ont été conservées ; des paragraphes ou mots peuvent être coupés. L’extraction brute utilise pdfplumber ; les TXT UTF-8 sont stockés localement dans `results/extracted/`, ignoré par Git comme les PDF. Ne pas copier de longs extraits des romans dans la documentation. L’énoncé impose également d’effacer le corpus à la fin du cours ; aucune suppression n’est à effectuer maintenant.

## Notions mentionnées dans le cadrage

Corpus, tokens, tokenisation, unigrammes, bigrammes, trigrammes, occurrences/fréquences, modèle de langue, co-occurrences si utiles, entités nommées, heuristiques, filtrage, expressions régulières, antidictionnaire et informations POS. FreeLing et NLTK sont des possibilités à étudier, pas des dépendances retenues. Le niveau de maîtrise de chaque notion reste à confirmer avec l’étudiant.

## Étapes prévues

1. Lecture et compréhension du corpus.
2. Statistiques initiales.
3. Étude du prétraitement.
4. Définition, implémentation et test de la tokenisation.
5. Unigrammes, bigrammes et trigrammes.
6. Fréquences et modèle de langue.
7. Analyse du bruit observé.
8. Heuristiques pour les candidats.
9. Production de L.
10. Raffinement de L vers LP.
11. Production de LL.
12. Évaluation des erreurs et limites.
13. Résultats finaux en UTF-8.

Voir [le plan détaillé](docs/PLAN_REALISATION.md). Les choix non fixés figurent dans [DECISIONS.md](docs/DECISIONS.md).

## Règles pour les prochaines sessions

1. Ne pas inventer d’exigence du professeur.
2. Ne pas inventer de résultats.
3. Ne pas fabriquer LP ou LL à partir de listes Internet de personnages ou de lieux.
4. Ne pas remplacer le TP par une API NER externe.
5. N’utiliser des outils linguistiques que s’ils sont pertinents et compatibles avec le sujet.
6. Justifier et documenter les décisions algorithmiques.
7. Préférer du Python simple et lisible.
8. Tester chaque étape avant la suivante.
9. Ne pas modifier le corpus original.
10. Ne jamais publier le corpus.
11. Ne pas développer plusieurs phases d’un coup.
12. Demander le document correspondant lorsqu’une consigne du professeur manque.

## État actuel

Tâche 3 : audit du corpus brut réalisé.

Tâche 4 — Prétraitement conservateur Bash/AWK : TERMINÉE

Entrées : `results/extracted/`. Sorties : `results/processed/` (trois TXT UTF-8 locaux ignorés par Git). Journal : `results/preprocessing_report.txt`. GNU awk 5.3.2, locale C.utf8 ; 18 tests réussis et SHA-256 des sources inchangés. 343 paginations supprimées, 40 jonctions avec espace, 10 formes avec tiret réunies ; 341 frontières préservées. Les règles et leurs limites sont détaillées dans `docs/PRETRAITEMENT.md`. Attendre la validation avant la tokenisation.

Tâche suivante — Génération de L : IMPLÉMENTÉE POUR VALIDATION

Entrées : `results/processed/` uniquement. Implémentation C++17 : `src/entites_nommees/generate_l.cpp`, lancée par `scripts/generate_l.sh`. Sorties : `results/lists/liste_L.txt` et `results/lists/liste_L_stats.txt`. Règle : n-grammes `n=1,2,3` construits dans une même page, retenus si le premier token commence par une majuscule ; fréquences conservées ; aucune classification PERSON/lieu, aucun antidictionnaire. Tests : `tests/test_generate_l.sh`, 15 tests réussis. Documentation : `docs/LISTE_L.md`.

Tâche suivante — Génération de LP : IMPLÉMENTÉE POUR VALIDATION

Entrée : `results/lists/liste_L.txt`. Implémentation Python standard : `scripts/generate_lp.py`. Sorties : `results/lists/liste_LP.txt` et `results/lists/liste_LP_stats.txt`. Règle : filtrage déterministe de L vers des entités nommées de personnes/personnages probables ; rejets et ambigus comptés ; aucune ressource ENT inventée ; aucun NER externe. Tests : `tests/test_generate_lp.sh`, 15 tests réussis. Documentation : `docs/LISTE_LP.md`.

État actuel : extraction, audit, prétraitement conservateur, génération de L et génération de LP réalisés ; LL non commencée.

Le script `src/entites_nommees/corpus_reader.py` ouvre les trois PDF, extrait le texte en mémoire et affiche un bilan brut. L’option `--export` génère les trois TXT bruts sans nettoyage. Aucun résultat L, LP ou LL n’a été créé. Attendre l’analyse des résultats et une autorisation explicite avant de poursuivre.

Tâche 2 exécutée avec succès : `Fondation.txt` (210059 octets), `Fondation_et_empire.txt` (231990 octets), `Seconde_Fondation.txt` (243617 octets), dans `results/extracted/`. Chaque fichier a été relu en UTF-8 strict et comparé intégralement aux pages en mémoire. Les caractères U+000C (`\f`) ajoutés entre pages sont respectivement au nombre de 107, 115 et 119 ; ils sont exclus des caractères extraits dans le tableau ci-dessous. Les empreintes SHA-256 des PDF sont inchangées. Les six fichiers PDF/TXT du corpus sont ignorés et non suivis par Git. Aucun nettoyage, aucune correction ni tokenisation n’a été effectué.

## État d’avancement au 30 septembre 2026

Inspection/extraction technique exécutée avec pdfplumber 0.11.9 :

| Roman | Pages | Avec texte | Sans texte | Caractères | Lignes | Mots bruts approximatifs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fondation | 108 | 108 | 0 | 205057 | 3989 | 35456 |
| Fondation et Empire | 116 | 116 | 0 | 226390 | 4361 | 39339 |
| Seconde Fondation | 120 | 120 | 0 | 237404 | 4407 | 39724 |
| Total | 344 | 344 | 0 | 668851 | 12757 | 114519 |

Les aperçus sont lisibles et les accents présents. Inspection limitée : retours de ligne de mise en page, phrases interrompues entre pages conservées, titres et numéros de pages inclus, caractères `±` autour de certains numéros dans les deux premiers romans. L’ordre des titres de la première page de Seconde Fondation mérite une vérification visuelle avant toute correction. Ces constats ne constituent pas une validation exhaustive du texte. Aucun OCR ni nettoyage effectué ; comptage par blancs uniquement, distinct de la future tokenisation NLP.

Les trois PDF du corpus retenu sont présents localement. Les six PDF pédagogiques sont copiés sans modification dans `docs/` et ont été examinés ; l’image du réseau a été convertie en `docs/2eme_Fondation.pdf`. La synthèse `docs/CONSIGNES_PROF.md` distingue les exigences, les supports et les points à clarifier. Pour assurer la continuité ChatGPT/Codex, partager ces fichiers de contexte à chaque reprise plutôt que supposer les conversations synchronisées.
