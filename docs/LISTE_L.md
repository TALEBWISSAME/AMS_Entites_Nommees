# Génération de la liste L

## Définition de L selon les consignes

Source principale : `docs/AMS1_EN (1).pdf`, pages 1 à 3. Le sujet demande de produire `L`, une liste d'entités nommées candidates, en vrac et sans filtrage. Il demande aussi de manipuler le corpus sous forme de n-grammes et indique que les n-grammes `n=1,2,3` aident à produire des listes d'entités nommées potentielles pouvant contenir du bruit.

Le sujet ne précise pas un format de fichier exact, un ordre de tri, une règle complète de tokenisation, ni si les fréquences doivent être incluses dans `L`. Il mentionne l'antidictionnaire, FreeLing/POS et NLTK comme ressources possibles, mais ne les impose pas pour la production de `L`.

## Choix techniques

Décision du projet pour cette étape : produire des candidats par n-grammes `n=1,2,3` dont le premier token commence par une majuscule. Ce choix conserve volontairement du bruit, notamment les débuts de phrases, conformément au caractère "en vrac et sans filtrage" de `L`.

Les formes candidates sont dédupliquées dans la sortie, avec leur fréquence. Cela évite de perdre l'information d'occurrence tout en gardant un fichier exploitable pour les étapes LP/LL.

## Langage utilisé

La génération de `L` est implémentée en C++ dans `src/entites_nommees/generate_l.cpp`, avec compilation C++17 par `scripts/generate_l.sh`. Le code n'utilise pas de dépendance externe lourde et ne modifie pas les fichiers d'entrée.

## Tokenisation

Le tokeniseur lit les fichiers UTF-8 et décode les code points avant de décider les frontières de token. Il ne traite donc pas un octet UTF-8 comme un caractère complet.

Un token est une suite de lettres ou chiffres. Les apostrophes (`'`, `’`) et tirets (`-`, U+2010 à U+2014) sont conservés seulement lorsqu'ils sont internes, c'est-à-dire entourés par deux caractères de coeur de token. La ponctuation ordinaire, les guillemets, parenthèses, deux-points, points, virgules et glyphes suspects servent de séparateurs.

## Gestion UTF-8

Les entrées sont validées par décodage UTF-8 strict dans le programme. Les sorties `results/lists/liste_L.txt` et `results/lists/liste_L_stats.txt` sont écrites en UTF-8. Les tests relisent les sorties en UTF-8.

## Gestion de la casse

La casse est conservée. Aucune normalisation en minuscules n'est effectuée. Le critère de candidature examine seulement le premier code point du premier token du n-gramme : il doit être une majuscule ASCII ou une majuscule accentuée française reconnue.

## Retours à la ligne

Les retours à la ligne internes à une page sont traités comme des séparateurs blancs logiques. Ils ne créent pas de token vide et ne modifient pas physiquement les fichiers `results/processed/`.

## Frontières U+000C

U+000C reste une frontière absolue. Le programme découpe chaque fichier en pages avant la tokenisation et construit les n-grammes seulement à l'intérieur d'une même page. Aucun unigramme, bigramme ou trigramme n'est produit par concaténation de deux pages.

## N-grammes

Les valeurs de `n` utilisées sont `1`, `2` et `3`, conformément à la mention explicite des n-grammes `n=1,2,3` dans l'énoncé. Tous les n-grammes candidats commencent par un token à majuscule ; les tokens suivants peuvent être majuscules ou minuscules afin de conserver des candidats bruités mais utiles.

## Critère de candidature

Un n-gramme entre dans `L` si :

- il est construit dans une seule page ;
- `n` vaut `1`, `2` ou `3` ;
- son premier token commence par une majuscule ;
- la forme n'est pas vide.

Aucune classification PERSON/lieu/organisation n'est faite. Aucun antidictionnaire n'est appliqué à cette étape.

## Format de sortie

`results/lists/liste_L.txt` est un TSV UTF-8 déterministe :

```text
n	forme	frequence
```

Le tri est stable : d'abord `n` croissant, puis forme lexicographique byte à byte UTF-8. Les statistiques d'exécution sont dans `results/lists/liste_L_stats.txt`.

## Tests

Les tests automatiques sont dans `tests/test_generate_l.sh`. Ils compilent le programme sur un mini-corpus artificiel et vérifient : candidat simple, accents UTF-8, apostrophe, tiret interne, retour à la ligne normal, espaces multiples, ponctuation, bigramme, trigramme, interdiction de traverser U+000C, faux nom propre inter-page interdit, conservation de la casse, déterminisme, sortie UTF-8 et invariant de frontière.

Résultat : 15 tests réussis, 0 échoué.

## Statistiques obtenues

| Roman | Tokens | Pages | Frontières | Occurrences n=1 | Occurrences n=2 | Occurrences n=3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fondation | 33021 | 108 | 107 | 4292 | 4280 | 4275 |
| Fondation_et_empire | 36928 | 116 | 115 | 4514 | 4495 | 4489 |
| Seconde_Fondation | 37406 | 120 | 119 | 4481 | 4464 | 4454 |
| Total | 107355 | 344 | 341 | 13287 | 13239 | 13218 |

Formes candidates uniques : n=1 : 1246 ; n=2 : 7974 ; n=3 : 11911 ; total : 21131. Occurrences candidates totales : 39744. Traversées U+000C : 0.

## Limites

La méthode produit volontairement du bruit : débuts de phrases, mots en capitales, formes typographiques et fragments imparfaits peuvent entrer dans `L`. Les glyphes suspects conservés par le prétraitement ne sont pas réparés. Les tokens commençant par une minuscule après apostrophe, par exemple certaines formes avec article élidé, ne sont pas promus artificiellement en candidats.

## Préparation de l'étape LP/LL

`L` fournit une base large et fréquentielle pour les raffinements futurs. Les étapes LP et LL devront filtrer, regrouper et classer les candidats, éventuellement avec expressions régulières, antidictionnaire, informations grammaticales ou autres heuristiques justifiées. Aucune de ces classifications n'est commencée ici.
