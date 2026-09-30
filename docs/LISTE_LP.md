# Génération de la liste LP

## Définition de LP selon le professeur

Source principale : `docs/AMS1_EN (1).pdf`, page 1. Le sujet demande, pour la tâche 2 : à partir de `L`, produire par raffinements, filtrage et expressions régulières éventuelles une liste d'entités nommées de personnes, appelée `LP`.

Cette définition est plus précise que `L` : `LP` ne doit pas rester une liste générale de candidats, mais viser les personnes/personnages. Le sujet ne donne pas de format imposé, de seuil, d'ordre de tri, ni de méthode unique obligatoire.

## Source L

La source unique est `results/lists/liste_L.txt`, au format :

```text
n	forme	frequence
```

La génération de `LP` ne régénère pas `L`, ne modifie pas `L` et ne modifie pas les fichiers `results/processed/*.txt`.

## Méthode choisie

La méthode retenue est un filtrage déterministe de `L`, sans modèle NER externe. Chaque forme de `L` est classée en :

- `retenu` : forme exportée dans `LP`;
- `rejet` : bruit ou indice non-personne;
- `ambigu` : forme plausible ou informative mais insuffisante pour être exportée automatiquement.

Le choix est volontairement explicable à l'oral : on réduit le bruit de début de phrase, on rejette les artefacts et indices non-personnes, on conserve les formes de noms propres simples fréquentes et les séquences nominales majuscules compatibles avec des noms de personnes.

## Rôle de l'antidictionnaire

L'énoncé mentionne un antidictionnaire français sur l'ENT parmi les ressources possibles, mais aucun fichier officiel n'est présent dans le dépôt et le sujet ne l'impose pas explicitement pour `LP`. Aucun antidictionnaire n'a donc été inventé. La méthode actuelle reste reproductible avec les seules ressources locales.

## Ressources utilisées

Ressources internes uniquement :

- `results/lists/liste_L.txt`;
- une courte liste locale de mots grammaticaux fréquents servant à rejeter les débuts de phrase évidents;
- une courte liste locale d'indices non-personnes et de titres/fonctions pour classer retenu, rejet ou ambigu.

Ces listes ne prétendent pas remplacer une ressource linguistique complète.

## Langage choisi

LP est générée en Python par `scripts/generate_lp.py`. Python est autorisé par l'énoncé et adapté ici, car l'étape consiste surtout à appliquer des règles lisibles, à produire des statistiques et à tracer les raisons de décision.

## Dépendances

Aucune dépendance externe n'est ajoutée. Le script utilise seulement la bibliothèque standard Python.

## Règles de filtrage

Sont rejetés notamment :

- formes contenant des marqueurs d'artefact (`(cid:n)`, `¶`, `°`, etc.);
- formes contenant des nombres;
- débuts par mots grammaticaux fréquents (`Il`, `Je`, `Vous`, `Mais`, `C'est`, etc.);
- indices non-personnes évidents (`Fondation`, `Empire`, `Galaxie`, `Trantor`, etc.);
- séquences en majuscules structurelles;
- n-grammes de contexte de type nom + verbe ou nom + mot grammatical.

Sont retenus notamment :

- unigrammes majuscules fréquents et non rejetés;
- bigrammes nominaux dont les tokens sont compatibles avec des noms propres;
- trigrammes nominaux seulement s'ils sont plus solides, soit fréquence au moins 2, soit titre suivi de noms;
- formes avec titre si le titre est suivi de tokens nominaux.

Les cas faibles sont classés `ambigu` plutôt que supprimés silencieusement.

## Traitement uni/bi/trigrammes

Les trois valeurs `n=1,2,3` héritées de `L` sont lues. Les trigrammes sont traités plus strictement, car le contrôle manuel a montré qu'ils capturent souvent un vrai nom suivi d'un mot de contexte. Aucun n-gramme nouveau n'est généré à cette étape.

## Traitement des débuts de phrases

Les débuts de phrase fréquents sont traités par une petite ressource de mots grammaticaux et narratifs. Cette règle rejette par exemple les pronoms, déterminants, conjonctions et formes élidées de dialogue les plus fréquentes. Elle reste une approximation documentée.

## Traitement des noms composés

Les noms composés de deux tokens majuscules compatibles avec des noms propres sont conservés. Les trigrammes sont conservés seulement avec une preuve plus forte, afin de limiter les séquences nom + contexte. Aucun regroupement sémantique de type `Hari`, `Seldon`, `Hari Seldon` n'est fait automatiquement.

## Traitement des fréquences

La fréquence exportée pour une forme LP est la fréquence de cette forme dans `L`. Les fréquences de formes imbriquées ne sont pas additionnées : `Hari`, `Seldon` et `Hari Seldon` restent des formes distinctes si elles sont retenues.

## Traitement des variantes

La casse originale est conservée. Les variantes de casse ou de graphie ne sont pas fusionnées automatiquement. Le script compte les variantes potentielles par `casefold()` dans les statistiques.

## UTF-8

Les fichiers sont lus et écrits en UTF-8. Les tests relisent les sorties en UTF-8 strict. Les accents sont conservés.

## Tests

`tests/test_generate_lp.sh` utilise un mini-fichier `L` artificiel. Il vérifie : nom simple, nom composé, rejet d'un début de phrase, accents, apostrophe, tiret interne, fréquence conservée, déterminisme, source `L` non modifiée, cas ambigu, variante de casse, absence de LL, absence de faux n-gramme contextuel, UTF-8 et statistiques d'artefacts.

Résultat : 15 tests réussis, 0 échoué.

## Statistiques

| Mesure | Valeur |
| --- | ---: |
| Lignes dans L | 21131 |
| Candidats examinés | 21131 |
| Retenus dans LP | 922 |
| Rejetés | 18791 |
| Ambigus | 1418 |
| Occurrences LP | 5562 |
| Retenus n=1 | 479 |
| Retenus n=2 | 439 |
| Retenus n=3 | 4 |
| Artefacts rejetés | 0 |
| Variantes de casse potentielles | 1 |

Principales raisons : `debut_mot_grammatical` 8368, `nom_suivi_contexte` 8111, `indice_non_personne` 1911, `unigramme_rare` 610, `2gramme_nominal_majuscule` 425, `unigramme_majuscule_frequent` 479.

## Limites

LP reste une liste produite par heuristiques. Elle peut contenir des faux positifs, surtout des titres ou fonctions employés comme noms, et peut manquer des personnages rares cités une seule fois. Sans antidictionnaire officiel, POS tagging ou validation manuelle complète, cette étape ne prétend pas atteindre une reconnaissance parfaite.

La méthode ne répare pas les glyphes suspects du corpus et ne classe pas les lieux. Les lieux ou organisations évidents sont seulement rejetés comme non-personnes quand ils perturbent LP.

## Cas ambigus

Les formes ambiguës ne sont pas exportées dans `liste_LP.txt`, mais elles sont comptées et documentées dans les statistiques. Elles couvrent notamment les titres seuls, les unigrammes rares et les séquences où un nom est suivi d'un mot de contexte.

## Préparation de l'étape LL

LP pourra servir à ne pas confondre personnes et lieux lors de la future construction de `LL`. L'étape `LL` n'est pas commencée ici : aucun lieu n'est exporté comme résultat, aucun graphe ni cooccurrence n'est calculé.
