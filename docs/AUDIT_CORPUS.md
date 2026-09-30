# Audit du corpus brut

## Objectif

Observer, mesurer et documenter uniquement. Aucune correction, tokenisation NLP ou extraction d’entités. Les exigences du professeur (UTF-8, pages impaires, listes futures) sont distinguées des supports de cours et de nos conventions de mesure. Les seuils et motifs ci-dessous sont nos outils de diagnostic, pas des obligations du professeur.

## Corpus analysé

- `results/extracted/Fondation.txt`
- `results/extracted/Fondation_et_empire.txt`
- `results/extracted/Seconde_Fondation.txt`

## Extraction actuelle

pdfplumber 0.11.9 ; TXT UTF-8 bruts. `\f` (U+000C) est le séparateur technique défini dans corpus_reader.py. Caractères hors séparateurs et lignes par page sont comparables à la tâche 1. Les mots sont estimés par split(), sans nettoyage. Les majuscules sont mesurées sur ces mêmes formes, ponctuation comprise : premier caractère majuscule, isupper(), islower(). Ces catégories peuvent se chevaucher et ne détectent pas des personnages.

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Caractères hors séparateurs | 205057 | 226390 | 237404 | 668851 |
| Caractères TXT | 205164 | 226505 | 237523 | 669192 |
| Lignes | 3989 | 4361 | 4407 | 12757 |
| Lignes vides | 0 | 0 | 0 | 0 |
| Lignes très courtes (1–10 caractères) | 260 | 278 | 248 | 786 |
| Mots bruts split() | 35456 | 39339 | 39724 | 114519 |
| Séparateurs | 107 | 115 | 119 | 341 |
| Séquences de ≥2 espaces ASCII | 0 | 0 | 0 | 0 |
| Lignes avec espace/tabulation initial | 0 | 0 | 0 | 0 |

## Frontières de pages

| Roman | Séparateurs observés | Attendus (tâche 1) | Concordance |
| --- | --- | --- | --- |
| Fondation | 107 | 107 | True |
| Fondation et Empire | 115 | 115 | True |
| Seconde Fondation | 119 | 119 | True |

Les pages conservées ne sont pas consécutives dans le roman : une page paire manque entre elles. Une phrase, un dialogue ou un paragraphe peut donc être interrompu, sans que les deux côtés soient à raccorder. Les compteurs suivants sont des indices, pas une détection certaine des phrases, mots ou paragraphes. Pour observer la fin narrative, un dernier pied candidat encadré est écarté uniquement dans une vue en mémoire.

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Frontières après ligne narrative sans ponctuation finale | 43 | 55 | 64 | 162 |
| Frontières suivies de minuscule | 41 | 41 | 39 | 121 |
| Frontières suivies de marqueur de dialogue | 37 | 41 | 41 | 119 |
| Frontières après tiret final narratif | 1 | 0 | 1 | 2 |

- Fondation, frontière PDF 1→2 : ` points de la Galaxie.\n± 3 ±` → `heures annoncées par les hau`.

- Fondation, frontière PDF 2→3 : `uerai pas ", fit Gaal.\n± 5 ±` → `même pas de mur devant lui :`.

- Fondation et Empire, frontière PDF 1→2 : `e sourit au vieillard.\n± 3 ±` → `On lui avait dit un jour que`.

- Fondation et Empire, frontière PDF 2→3 : `t autour d'eux. Il y a\n± 5 ±` → `commander les défilés milita`.

- Seconde Fondation, frontière PDF 1→2 : `l se garde de la\nmanifester.` → `son regard à travers la cara`.

- Seconde Fondation, frontière PDF 2→3 : `nt toute satisfaction.\n- 5 -` → `Bail Channis était l'un d'eu`.

## Retours à la ligne

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Lignes | 3989 | 4361 | 4407 | 12757 |
| Lignes vides | 0 | 0 | 0 | 0 |
| Lignes très courtes (1–10 caractères) | 260 | 278 | 248 | 786 |
| Transitions de lignes potentiellement continues | 2341 | 2617 | 2741 | 7699 |

Très courte = 1 à 10 caractères après strip() pour la mesure seulement. Transition candidate = ligne sans .!?…»"’ final suivie d’une ligne commençant par une minuscule, dans une même page. Cela suggère des retours de mise en page ; les paragraphes réels ne peuvent pas être reconstitués sûrement avec ce seul test.

## Coupures potentielles de mots

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Coupures suspectes tiret + retour | 17 | 24 | 35 | 76 |

Motif : lettres + tiret (-, ‐, ‑, –, —) + retour de ligne + lettres, dans une même page. Un composé ou une inversion grammaticale reste possible. Suspect ne signifie pas erreur certaine ; aucun cas n’est corrigé. Ce motif ne détecte pas toutes les coupures, notamment celles sans tiret.

- Fondation : page PDF 2, `années-\nlumière` ; page PDF 9, `le-\nchamp` ; page PDF 18, `vous-\nmême`

- Fondation et Empire : page PDF 2, `Dites-\nmoi` ; page PDF 3, `monde-\nfrontière` ; page PDF 8, `eux-\nmêmes`

- Seconde Fondation : page PDF 2, `au-\ndessus` ; page PDF 5, `au-\ndessous` ; page PDF 6, `diriez-\nvous`

## Ponctuation

| Signe | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| `!` | 152 | 132 | 149 | 433 |
| `"` | 687 | 709 | 673 | 2069 |
| `%` | 0 | 0 | 1 | 1 |
| `'` | 2480 | 2593 | 2494 | 7567 |
| `(` | 5 | 14 | 25 | 44 |
| `)` | 5 | 14 | 26 | 45 |
| `,` | 2046 | 2474 | 2312 | 6832 |
| `-` | 1225 | 1217 | 1445 | 3887 |
| `.` | 2773 | 3068 | 2924 | 8765 |
| `...` | 149 | 186 | 228 | 563 |
| `/` | 0 | 2 | 0 | 2 |
| `:` | 176 | 143 | 95 | 414 |
| `;` | 78 | 87 | 77 | 242 |
| `?` | 441 | 437 | 448 | 1326 |
| `[` | 0 | 0 | 0 | 0 |
| `\` | 0 | 1 | 0 | 1 |
| `]` | 0 | 1 | 0 | 1 |
| `_` | 1 | 0 | 0 | 1 |
| `«` | 0 | 0 | 0 | 0 |
| `¶` | 3 | 5 | 0 | 8 |
| `»` | 0 | 0 | 0 | 0 |
| `–` | 0 | 0 | 0 | 0 |
| `—` | 0 | 0 | 0 | 0 |
| `’` | 0 | 0 | 0 | 0 |
| `…` | 0 | 0 | 0 | 0 |

Les points de « ... » sont inclus dans le compteur du point ; les occurrences de « ... » sont comptées séparément, sans chevauchement. Les déséquilibres ouvrants/fermants ne prouvent pas une erreur (pages manquantes).

## Apostrophes

| Signe | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| `'` | 2480 | 2593 | 2494 | 7567 |
| `’` | 0 | 0 | 0 | 0 |

## Tirets

| Signe | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| `-` | 1225 | 1217 | 1445 | 3887 |
| `–` | 0 | 0 | 0 | 0 |
| `—` | 0 | 0 | 0 | 0 |
| `‐` | 0 | 0 | 0 | 0 |
| `‑` | 0 | 0 | 0 | 0 |

- Fondation : `'` : ` Né en l'an 11988,`; `-` : `ctique (- 79, an I`

- Fondation et Empire : `'` : `\nRiose s'acquit le`; `-` : `ait peut-être\nsupé`

- Seconde Fondation : `'` : ` : ... C'est après`; `-` : `Union " - titre\nof`

Les tirets peuvent marquer dialogues, composés ou inversions : aucune normalisation décidée.

## Casse

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Formes dont le premier caractère est majuscule | 4285 | 4496 | 4451 | 13232 |
| Formes isupper() | 172 | 62 | 115 | 349 |
| Formes islower() | 28553 | 32303 | 32827 | 93683 |

## Espaces

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Séquences de ≥2 espaces ASCII | 0 | 0 | 0 | 0 |
| Lignes avec espace/tabulation initial | 0 | 0 | 0 | 0 |
| Lignes avec espace/tabulation final | 0 | 0 | 0 | 0 |
| Tabulations | 0 | 0 | 0 | 0 |
| Espaces insécables U+00A0 | 0 | 0 | 0 | 0 |
| Espaces insécables fins U+202F | 0 | 0 | 0 | 0 |

Les séquences de plusieurs espaces sont comptées comme groupes, pas comme nombre d’espaces excédentaires.

## Caractères Unicode

Inventaire ci-dessous : caractères non ASCII, contrôles et symboles. Les lettres accentuées ne sont pas des anomalies. Le compteur « inhabituel » couvre les catégories Unicode C (contrôle/format/autres), S (symboles), U+FFFD et les non-ASCII ni lettres ni ponctuation ; il exclut LF et le séparateur technique FF.

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Occurrences inhabituelles (définition ci-dessous) | 236 | 259 | 5 | 500 |

| Code | Caractère | Nom | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- | --- | --- |
| U+0009 | contrôle | contrôle | 0 | 0 | 0 | 0 |
| U+000A | contrôle | contrôle | 3881 | 4245 | 4287 | 12413 |
| U+000C | contrôle | contrôle | 107 | 115 | 119 | 341 |
| U+00A0 | NO-BREAK SPACE | NO-BREAK SPACE | 0 | 0 | 0 | 0 |
| U+00B0 | `°` | DEGREE SIGN | 20 | 27 | 5 | 52 |
| U+00B1 | `±` | PLUS-MINUS SIGN | 216 | 232 | 0 | 448 |
| U+00B6 | `¶` | PILCROW SIGN | 3 | 5 | 0 | 8 |
| U+00C7 | `Ç` | LATIN CAPITAL LETTER C WITH CEDILLA | 10 | 26 | 3 | 39 |
| U+00C8 | `È` | LATIN CAPITAL LETTER E WITH GRAVE | 0 | 0 | 1 | 1 |
| U+00C9 | `É` | LATIN CAPITAL LETTER E WITH ACUTE | 2 | 3 | 0 | 5 |
| U+00E0 | `à` | LATIN SMALL LETTER A WITH GRAVE | 637 | 601 | 704 | 1942 |
| U+00E2 | `â` | LATIN SMALL LETTER A WITH CIRCUMFLEX | 70 | 51 | 80 | 201 |
| U+00E7 | `ç` | LATIN SMALL LETTER C WITH CEDILLA | 113 | 149 | 94 | 356 |
| U+00E8 | `è` | LATIN SMALL LETTER E WITH GRAVE | 486 | 515 | 575 | 1576 |
| U+00E9 | `é` | LATIN SMALL LETTER E WITH ACUTE | 2698 | 3194 | 3967 | 9859 |
| U+00EA | `ê` | LATIN SMALL LETTER E WITH CIRCUMFLEX | 352 | 384 | 381 | 1117 |
| U+00EB | `ë` | LATIN SMALL LETTER E WITH DIAERESIS | 1 | 0 | 0 | 1 |
| U+00EE | `î` | LATIN SMALL LETTER I WITH CIRCUMFLEX | 76 | 70 | 66 | 212 |
| U+00EF | `ï` | LATIN SMALL LETTER I WITH DIAERESIS | 7 | 10 | 16 | 33 |
| U+00F4 | `ô` | LATIN SMALL LETTER O WITH CIRCUMFLEX | 88 | 60 | 72 | 220 |
| U+00F9 | `ù` | LATIN SMALL LETTER U WITH GRAVE | 65 | 88 | 67 | 220 |
| U+00FB | `û` | LATIN SMALL LETTER U WITH CIRCUMFLEX | 51 | 70 | 63 | 184 |
| U+0152 | `Œ` | LATIN CAPITAL LIGATURE OE | 0 | 0 | 0 | 0 |
| U+0153 | `œ` | LATIN SMALL LIGATURE OE | 0 | 0 | 0 | 0 |
| U+202F | NARROW NO-BREAK SPACE | NARROW NO-BREAK SPACE | 0 | 0 | 0 | 0 |
| U+FFFD | `�` | REPLACEMENT CHARACTER | 0 | 0 | 0 | 0 |

| Marqueurs textuels de glyphes PDF | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| (cid:n) | 0 | 8 | 0 | 8 |

Les marqueurs `(cid:n)` sont des chaînes ASCII : ils ne seraient pas détectés par un simple inventaire Unicode. Les nombres qu’ils contiennent sont inclus dans le comptage numérique brut. Exemples courts observés : `l’°uvre` (apostrophe ASCII dans le TXT), `O¶amour-propre` et `(cid:10)°il` dans les deux premiers romans. Ces formes suggèrent des glyphes mal extraits, à confirmer au PDF, sans correction. Dans Seconde Fondation, `1°` est aussi un emploi légitime du signe degré : le caractère seul ne suffit pas. Aucun U+FFFD ni œ/Œ n’est présent ; cette absence ne garantit pas que les ligatures originales ont été fidèlement extraites.

## Motifs numériques

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Nombres isolés (occurrences) | 127 | 125 | 143 | 395 |
| Lignes entièrement numériques | 0 | 0 | 0 | 0 |

Nombres isolés = suites de chiffres non adjacentes à un caractère de mot Unicode. Ils peuvent désigner dates, quantités ou pages ; aucune suppression automatique.

- Fondation, dix nombres les plus fréquents : 5 (3), 1 (3), 99 (3), 79 (2), 3 (2), 7 (2), 9 (2), 85 (2), 77 (2), 11988 (1)

- Fondation et Empire, dix nombres les plus fréquents : 3 (6), 17 (2), 10 (2), 45 (2), 5 (1), 7 (1), 9 (1), 11 (1), 13 (1), 15 (1)

- Seconde Fondation, dix nombres les plus fréquents : 55 (3), 1 (3), 11 (2), 13 (2), 15 (2), 3 (2), 2 (2), 83 (2), 5 (1), 7 (1)

## En-têtes / pieds de page potentiels

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | --- | --- | --- | --- |
| Pieds numériques encadrés candidats | 108 | 116 | 119 | 343 |

Pied candidat : dernière ligne constituée d’un entier encadré du même signe ±, -, – ou —. Motifs répétés : égalité exacte dans les deux premières/dernières lignes des pages ; leur fréquence porte sur ces positions, pas sur tout le roman. Un titre de chapitre est du contenu possible, pas un artefact certain.

- Fondation, pieds : p. PDF 1 `± 3 ±`; p. PDF 2 `± 5 ±`; p. PDF 3 `± 7 ±`

- Fondation, marges répétées : `"` (2)

- Fondation et Empire, pieds : p. PDF 1 `± 3 ±`; p. PDF 2 `± 5 ±`; p. PDF 3 `± 7 ±`

- Fondation et Empire, marges répétées : `y vint répondre à celle qui brillait dans les` (2); `VIII` (2)

- Seconde Fondation, pieds : p. PDF 2 `- 5 -`; p. PDF 3 `- 7 -`; p. PDF 4 `- 9 -`

- Seconde Fondation, marges répétées : aucune parmi les motifs retenus.

## Problèmes observés

Les mesures révèlent des retours de mise en page, des marqueurs de pagination et des discontinuités de pages. Les motifs suspects et la typographie sont détaillés ci-dessus ; leur origine exacte (source ou extraction) nécessite parfois une comparaison au PDF. Une extraction décodable ne garantit pas la fidélité de chaque mot. Aucune correction ni décision de prétraitement ne découle automatiquement de cet audit.

Contrôle d’intégrité : SHA-256 avant/après identiques pour les trois TXT. Empreintes :

- `Fondation.txt` : `b10a71e7705cc2da41cc7e41817d568aebaf65ea263ba59d745ffb1934f2e54c`
- `Fondation_et_empire.txt` : `547c7c3be6a7dcd362a3ad6b85f6dff41bf7609e9b5c54bb851b718fe73d2b2c`
- `Seconde_Fondation.txt` : `803011045188f19d2df09577390817fcdf74d56dac7c9bcd3b41549b13ba183e`

## Questions à décider avant prétraitement

- Faut-il fusionner certains retours à la ligne ? → À décider

- Faut-il normaliser les apostrophes ? → À décider

- Faut-il normaliser les différents tirets ? → À décider

- Comment traiter les frontières entre pages impaires ? → À décider

- Comment traiter les mots potentiellement coupés ? → À décider

- Quels éléments de ponctuation conserver ? → À décider

- Faut-il retirer certains artefacts répétitifs ? → À décider

- Comment préserver la casse et les accents utiles aux futures entités ? → À décider
