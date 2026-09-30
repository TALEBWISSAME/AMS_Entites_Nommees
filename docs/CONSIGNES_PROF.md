# Consignes du professeur et synthèse de travail

Mis à jour le 30 septembre 2026 à partir des documents fournis par l’étudiant. Cette synthèse sert de référence commune pour les échanges avec ChatGPT et le travail dans Codex. Elle ne remplace pas les énoncés originaux.

## Documents disponibles

| Document dans `docs/` | Rôle |
| --- | --- |
| [0-plan.pdf](0-plan.pdf) | Présentation du projet, objectifs, organisation et ressources (14 pages). |
| [1-Defis.pdf](1-Defis.pdf) | Objectif global : extraction des personnages, liens de proximité, calcul et visualisation du graphe (20 pages). |
| [2-stat.pdf](2-stat.pdf) | Support de TAL statistique : corpus, tokenisation, types/tokens, fréquences, Zipf, collocations et concordances (49 pages). |
| [3-enertex.pdf](3-enertex.pdf) | Énergie textuelle, représentations matricielles, interactions entre phrases, résumé et segmentation thématique (25 pages). |
| [4-artex.pdf](4-artex.pdf) | Résumé extractif par pondération de phrases, représentations vectorielles et pistes avec embeddings (17 pages). |
| [AMS1_EN (1).pdf](AMS1_EN%20%281%29.pdf) | Énoncé du TP Entités Nommées, septembre 2026 : tâches et rendu (3 pages). |
| [2eme_Fondation.pdf](2eme_Fondation.pdf) | Image fournie, convertie en un PDF d’une page : illustration d’un réseau de personnages. |

Les six PDF originaux ont été copiés sans modification. L’image du réseau est une illustration fournie, pas un résultat calculé par notre projet ni une liste à recopier pour construire LP. Sa légende représente le degré par la taille des nœuds et le poids par l’épaisseur des liens ; la méthode exacte de calcul des liens n’est pas donnée par cette image.

## Ce que demande explicitement le TP actuel

Source : `AMS1_EN (1).pdf`, pages 1 à 3.

- Travail en binômes. Python est autorisé ; R, Java et JavaScript sont exclus pour le TP.
- Romans cités : **Fondation**, **Fondation et empire**, **Seconde Fondation** (page 1).
- Tâche 1 : produire **L**, liste de candidats entités nommées en vrac, sans filtrage.
- Tâche 2 : produire **LP**, personnes/personnages, à partir de L par raffinements (filtrage, expressions régulières, etc.).
- Tâche 3 : produire **LL**, à partir de L et LP, pour les lieux/catégories indiqués : cités, organisations, universités, villes, planètes.
- Manipuler le corpus et ses représentations en n-grammes, notamment n=1,2,3 ; concevoir et développer les algorithmes de production des listes.
- Le modèle de langue est présenté comme des tables de fragments et de leurs occurrences. Les tables de co-occurrences sont une possibilité évoquée, sans fenêtre imposée.
- FreeLing/POS, NLTK et l’antidictionnaire français de l’ENT sont des ressources possibles ; aucun choix de bibliothèque n’est imposé dans cet énoncé.
- Produire les ressources textuelles en **UTF-8**.
- Réfléchir aux conséquences du traitement de la ponctuation et des symboles ; aucune suppression générale n’est prescrite.
- Le corpus ne contient que les pages impaires : tenir compte des mots et paragraphes incomplets.
- Le corpus est réservé au cours, ne doit pas être redistribué et doit être effacé à la fin du cours. Cette dernière règle est consignée pour le futur ; aucune suppression n’est effectuée maintenant.

## Rendu attendu

Source : énoncé, page 3.

- **Petit rapport de 2 à 3 pages concernant les algorithmes.**
- **Résultats : listes L, LP et LL.**
- **Statistiques du corpus.**

Le sujet prévoit deux séances de TP. Il ne donne pas ici de date limite précise de dépôt, de convention de nommage des fichiers ni de liste exhaustive des statistiques. Ne pas en inventer. Les calendriers des diapositives introductives ne sont pas à reprendre automatiquement comme échéances de 2026.

## Projet global et supports de méthodes

`0-plan.pdf` (pages 10–11) et `1-Defis.pdf` (pages 2–3 et 16–19) replacent le TP dans l’objectif final : caractériser le corpus, extraire les personnages, calculer leurs liens de proximité, construire et visualiser un réseau, puis l’évaluer.

`2-stat.pdf` explique les difficultés de tokenisation (ponctuation, abréviations, apostrophes, casse, tirets, accents), les occurrences et types, les fréquences, les hapax, la loi de Zipf et les collocations. Ces notions éclairent les choix ; elles ne constituent pas toutes des livrables obligatoires du TP.

`3-enertex.pdf` étudie une représentation phrases/mots et les interactions directes ou indirectes entre phrases, avec des applications au résumé et à la segmentation. `4-artex.pdf` présente un résumé extractif et propose notamment d’explorer les embeddings et la recherche d’entités dans le texte complet ou un résumé (page 17). Ces pistes sont conservées pour la suite : l’énoncé actuel ne demande pas explicitement leur implémentation pour produire L, LP et LL.

## État réel du dépôt et points à clarifier

- Trois PDF de romans sont présents dans `corpus/`, ignoré par Git. Ils sont inchangés ; leur extraction brute est disponible en TXT UTF-8 dans `results/extracted/`, également ignoré par Git.
- Périmètre confirmé par l’étudiant le 30 septembre 2026 : **Fondation**, **Fondation et empire** et **Seconde Fondation** uniquement. Les PDF de **Fondation foudroyée** et **Terre et Fondation** ont été supprimés de `corpus/` à sa demande. Les fichiers sources dans Téléchargements sont conservés.
- L’antidictionnaire de l’ENT n’a pas été fourni. Le demander si cette ressource est retenue.
- L’extraction technique est réalisée avec pdfplumber 0.11.9. Le stockage local des TXT bruts est validé ; le traitement des coupures reste à décider.
- Le script d’inspection existe ; les choix NLP restent ouverts dans `DECISIONS.md`. Aucune liste L/LP/LL n’existe à ce stade.

## Continuité entre ChatGPT et Codex

Pour reprendre une session, transmettre ou consulter `CONTEXTE_PROJET.md`, cette synthèse, `PLAN_REALISATION.md` et `DECISIONS.md`. Les conversations ne doivent pas être supposées synchronisées : les fichiers du projet consignent l’état validé, les décisions et les vérifications.

Distinguer les exigences de l’énoncé, les exemples des supports et nos propres propositions. Consigner chaque choix justifié et les résultats réellement obtenus. Développer une phase à la fois ; ne pas lancer les tâches des supports simplement parce qu’elles y sont décrites.
