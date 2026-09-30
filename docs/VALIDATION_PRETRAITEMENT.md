# Validation finale du prétraitement

## Méthode

Validation effectuée sur les trois TXT régénérés depuis les PDF locaux, puis sur le prétraitement Bash/GNU awk existant. Les commandes relancées sont `python src/entites_nommees/corpus_reader.py --export`, `bash tests/test_preprocess.sh` via Git Bash, et `bash scripts/preprocess.sh` via Git Bash. L'audit des transformations réelles reproduit les règles de `scripts/preprocess.awk` sans modifier les sources.

Les résultats annoncés sont confirmés : 40 jonctions avec espace, 10 raccords avec tiret, 343 paginations supprimées, 341 frontières U+000C conservées, 8 `(cid:n)`, 8 `¶`, 52 `°`, et 6634 cas ambigus conservés.

## Validation des fusions

Les 40 fusions réelles ont été retrouvées. Classement : A=40, B=0, C=0, total=40. Par roman : Fondation=10, Fondation_et_empire=13, Seconde_Fondation=17.

| # | Roman | Page | Lignes | Déclencheur court | Cat. |
| ---: | --- | ---: | --- | --- | --- |
| 1 | Fondation | 13 | 6-7 | `silence se fit dans / la salle. Le Procureur` | A |
| 2 | Fondation | 18 | 11-12 | `silencieux. Hardin prit dans / la poche de sa` | A |
| 3 | Fondation | 49 | 17-18 | `d'hiver qui s'achevait sous / la neige et, une` | A |
| 4 | Fondation | 60 | 13-14 | `crainte constante... Poussé par / le désespoir, l'idée lui` | A |
| 5 | Fondation | 67 | 15-16 | `? demanda Gorov avec / un pâle sourire.` | A |
| 6 | Fondation | 76 | 37-38 | `qu'il faisait tourner entre / ses doigts. " C'est` | A |
| 7 | Fondation | 84 | 27-28 | `lorsqu'elle fut baignée par / la luminescence étrange, devint` | A |
| 8 | Fondation | 85 | 5-6 | `idées qui passaient dans / sa tête. " Et` | A |
| 9 | Fondation | 92 | 33-34 | `costume de Mallow avec / un air des plus` | A |
| 10 | Fondation | 103 | 27-28 | `à travers l'hyperespace vers / la Fondation.` | A |
| 11 | Fondation_et_empire | 19 | 21-22 | `bonnets qui restent dans / leur trou et qui` | A |
| 12 | Fondation_et_empire | 34 | 26-27 | `des édifices réunis par / des rampes ; creusés` | A |
| 13 | Fondation_et_empire | 35 | 25-26 | `monde-métropole le plongeait dans / une profonde mélancolie, née` | A |
| 14 | Fondation_et_empire | 57 | 7-8 | `un peu mieux dans / cette intrigue interstellaire. Je` | A |
| 15 | Fondation_et_empire | 64 | 11-12 | `il faut passer par / des négociations préliminaires dont` | A |
| 16 | Fondation_et_empire | 65 | 32-33 | `à nous d'entrer dans / la partie.` | A |
| 17 | Fondation_et_empire | 69 | 3-4 | `Magnifico étaient repliées sous / son menton en galoche,` | A |
| 18 | Fondation_et_empire | 79 | 22-23 | `récit, interrompu seulement par / les " Vraiment ?` | A |
| 19 | Fondation_et_empire | 81 | 13-14 | `être décelés seulement par / des examens microscopiques et` | A |
| 20 | Fondation_et_empire | 95 | 17-18 | `Il y avait dans / sa vieille voix comme` | A |
| 21 | Fondation_et_empire | 104 | 18-19 | `une certaine direction par / le conditionnement de mes` | A |
| 22 | Fondation_et_empire | 106 | 1-2 | `un rêve, regardant entre / ses deux interlocuteurs plutôt` | A |
| 23 | Fondation_et_empire | 113 | 35-36 | `sont des cadrans, avec / des aiguilles qui indiquent` | A |
| 24 | Seconde_Fondation | 3 | 18-19 | `pas. L'ascenseur l'enleva dans / une course rapide et` | A |
| 25 | Seconde_Fondation | 15 | 12-13 | `pour chercher refuge dans / ces coins déshérités de` | A |
| 26 | Seconde_Fondation | 40 | 33-34 | `Comme par exemple entre / ces deux hommes.` | A |
| 27 | Seconde_Fondation | 55 | 21-22 | `personnel - combiné avec / un transfert si habilement` | A |
| 28 | Seconde_Fondation | 57 | 29-30 | `qu'une modification survenue dans / la philosophie du sujet` | A |
| 29 | Seconde_Fondation | 58 | 2-3 | `qui était entrée dans / sa vie sur le` | A |
| 30 | Seconde_Fondation | 61 | 22-23 | `existe quelque tradition dans / ce monde-là, elle repose` | A |
| 31 | Seconde_Fondation | 69 | 18-19 | `était un intermédiaire entre / un visage rayonnant et` | A |
| 32 | Seconde_Fondation | 74 | 30-31 | `manières si conquérantes avec / les femmes... Vous ne` | A |
| 33 | Seconde_Fondation | 82 | 14-15 | `éclair, été illuminés par / une lueur sardonique.` | A |
| 34 | Seconde_Fondation | 83 | 3-4 | `faire tomber d'autres entre / leurs mains.` | A |
| 35 | Seconde_Fondation | 85 | 23-24 | `absorba le contenu avec / une moue significative.` | A |
| 36 | Seconde_Fondation | 86 | 3-4 | `opérations sont menées avec / une extrême diligence, et` | A |
| 37 | Seconde_Fondation | 92 | 19-20 | `romans-feuilletons. Elle vit dans / une atmosphère fantastique et` | A |
| 38 | Seconde_Fondation | 92 | 21-22 | `manifeste beaucoup d'intelligence dans / ce domaine ; suffisamment` | A |
| 39 | Seconde_Fondation | 99 | 10-11 | `vous graviez l'adresse dans / la mémoire. "` | A |
| 40 | Seconde_Fondation | 120 | 22-23 | `Orateur avait contemplé avec / une certaine méfiance ces` | A |

Toutes les fusions relient une ligne terminée par une préposition autorisée à une ligne commençant par un déterminant autorisé, sur la même page. Les contextes relus ne montrent pas de titre absorbé, de changement de page, ni de passage structurel évident.

## Risque de fusion de paragraphes

`continuation(a,b)` est conservatrice : elle exige deux lignes non structurelles, une ligne gauche d'au moins 25 caractères, une préposition finale limitée, et un déterminant initial limité. `structural(s)` bloque lignes vides, lignes indentées, débuts de dialogue/citation et titres en capitales/chiffres/ponctuation.

Risque restant : l'extraction brute ne contient pas de lignes vides de paragraphe. Une vraie rupture de paragraphe non marquée, finissant par une préposition et suivie d'un déterminant, pourrait donc satisfaire la règle et l'invariant par page. Aucun des 40 cas observés ne paraît être une telle erreur certaine.

## Validation des tirets

Les 10 raccords avec tiret ont été retrouvés. Classement : A=10, B=0, C=0, total=10. Par roman : Fondation=3, Fondation_et_empire=4, Seconde_Fondation=3.

| # | Roman | Page | Lignes | Forme autorisée | Cat. |
| ---: | --- | ---: | --- | --- | --- |
| 1 | Fondation | 2 | 5-6 | `années-lumière` | A |
| 2 | Fondation | 18 | 27-28 | `vous-même` | A |
| 3 | Fondation | 105 | 21-22 | `au-dessous` | A |
| 4 | Fondation_et_empire | 2 | 32-33 | `Dites-moi` | A |
| 5 | Fondation_et_empire | 8 | 4-5 | `eux-mêmes` | A |
| 6 | Fondation_et_empire | 49 | 24-25 | `vous-même` | A |
| 7 | Fondation_et_empire | 52 | 36-37 | `au-dessus` | A |
| 8 | Seconde_Fondation | 2 | 18-19 | `au-dessus` | A |
| 9 | Seconde_Fondation | 5 | 21-22 | `au-dessous` | A |
| 10 | Seconde_Fondation | 6 | 5-6 | `diriez-vous` | A |

Chaque raccord reste dans une même page. Le tiret est conservé : le traitement réunit seulement le retour à la ligne. La liste `allowed` limite volontairement le traitement à des graphies explicitement vues et validées ; elle évite une correction orthographique agressive, mais ne résout pas les 66 autres cas de tiret ambigus.

## Validation de la pagination

| Roman | Supprimées | Format | Min | Max | Progression | Anomalies |
| --- | ---: | --- | ---: | ---: | --- | ---: |
| Fondation | 108 | ± n ±: 108 | 3 | 217 | écarts {2: 107} | 0 |
| Fondation_et_empire | 116 | ± n ±: 116 | 3 | 233 | écarts {2: 115} | 0 |
| Seconde_Fondation | 119 | - n -: 119 | 5 | 241 | écarts {2: 118} | 0 |

Les 343 lignes supprimées sont toujours la dernière ligne non vide de leur page/enregistrement. Les numéros progressent de 2 en 2, ce qui correspond au corpus composé uniquement de pages impaires.

## Validation des frontières de pages

Frontières U+000C recomptées : Fondation=107, Fondation_et_empire=115, Seconde_Fondation=119, total=341.

`RS="\f"` fait traiter chaque page comme un enregistrement AWK indépendant. `RT` réémet ensuite exactement le séparateur lu. Les variables `previous`, `count` et les décisions de fusion sont réinitialisées à chaque enregistrement, donc aucune fusion avec espace ni aucun raccord avec tiret ne peut traverser U+000C dans ce code.

## Analyse des `(cid:n)`

Les 8 occurrences restantes sont toutes dans `Fondation_et_empire`. Elles appartiennent à trois pages PDF. Une vérification visuelle par rendu temporaire du PDF a permis d'identifier les passages au niveau phrase, mais aucune correction automatique n'a été appliquée : ces défauts viennent de l'extraction brute, pas d'une transformation du prétraitement.

| # | Page | Valeur | Contexte court extrait | Statut |
| ---: | ---: | --- | --- | --- |
| 1 | 1 | `(cid:17)` | `i\nétait sa destination. Il attHQGLW(cid:17)…` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |
| 2 | 1 | `(cid:3)` | `sa destination. Il attHQGLW(cid:17)(cid:3)/(…` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |
| 3 | 1 | `(cid:10)` | `nation. Il attHQGLW(cid:17)(cid:3)/(cid:10)°…` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |
| 4 | 35 | `(cid:3)` | `e pressaient sans\nfin jusqu'au-GHOj(cid:3) …` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |
| 5 | 35 | `(cid:3)` | `nt sans\nfin jusqu'au-GHOj(cid:3) GH(cid:3) …` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |
| 6 | 35 | `(cid:10)` | `in jusqu'au-GHOj(cid:3) GH(cid:3) O(cid:10)K…` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |
| 7 | 35 | `(cid:3)` | `j(cid:3) GH(cid:3) O(cid:10)KRUL]RQ(cid:3) O…` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |
| 8 | 90 | `(cid:3)` | `rs de calculs entre\ndeux bonds.\n,OV(cid:3)…` | RÉSOLU AVEC CERTITUDE, passage PDF lisible |

Preuves visuelles synthétiques : page 1, le passage est lisible comme une phrase contenant `L'œil`; page 35, le passage contient `au-delà de l'horizon`; page 90, le passage contient `Ils s'y mirent tous`. Les corrections nécessiteraient une étape dédiée de réparation des glyphes PDF, hors validation de la tâche 4.

## Analyse des `¶`

Les 8 `¶` restants ressemblent à des apostrophes mal extraites dans des séquences comme `O¶...`, `l¶...` ou `/¶...`, mais ils sont classés AMBIGU faute de preuve individuelle exhaustive dans le cadre du prétraitement.

| # | Roman | Page | Contexte court | Classement |
| ---: | --- | ---: | --- | --- |
| 1 | Fondation | 39 | `ile et la plus satisfaisante pour O¶amour-pro…` | AMBIGU |
| 2 | Fondation | 80 | `rs milliers de Korelliens cernait\nO¶astropor…` | AMBIGU |
| 3 | Fondation | 100 | ` attendant en silence,\ntandis que l¶équipage…` | AMBIGU |
| 4 | Fondation_et_empire | 11 | ` des actions individuelles.\nC'est O¶arrière-…` | AMBIGU |
| 5 | Fondation_et_empire | 35 | `GH(cid:3) O(cid:10)KRUL]RQ(cid:3) O¶étouffaie…` | AMBIGU |
| 6 | Fondation_et_empire | 90 | `culs entre\ndeux bonds.\n,OV(cid:3) V¶\ miren…` | AMBIGU |
| 7 | Fondation_et_empire | 110 | `ltés\nmentales... vous comprenez ? /¶Homo sap…` | AMBIGU |
| 8 | Fondation_et_empire | 110 | `t une nouvelle race dominante, et O¶Homo\nsap…` | AMBIGU |

## Analyse des `°`

Les 52 `°` ne doivent pas être supprimés globalement. Classement par contexte : usage probablement légitime=4, artefact probable=27, ambigu=21.

Regroupements observés : `1°`, `2°`, `3°` servent probablement à l'énumération dans 4 cas ; `°il` et `°uvre` indiquent probablement des défauts autour de `œ` ; plusieurs formes comme `F°ur`, `PDQ°...` ou `FRQWUHF°...` sont des artefacts probables ou ambigus liés à des mots plus largement corrompus. Aucune suppression globale n'est justifiée.

## Cas ambigus conservés

`cas_ambigus=6634` additionne des occasions conservées : transitions internes non structurelles sans ponctuation finale reconnue qui ne satisfont pas `continuation(a,b)`, plus des cas de tiret non autorisés. Ce compteur peut donc mélanger retours de ligne ordinaires, coupures possibles, ruptures de mise en page et vrais paragraphes. Il ne signifie pas 6634 erreurs.

## Impact des retours à la ligne

Les retours à la ligne conservés pourront créer du bruit si la future tokenisation traite chaque ligne comme une unité indépendante. En revanche, une tokenisation peut traiter les retours internes à une page comme de simples blancs pour les unigrammes, bigrammes et trigrammes, tout en gardant U+000C comme frontière absolue. Cela évitera les n-grammes artificiels entre pages impaires séparées par une page paire absente.

## Tests

`tests/test_preprocess.sh` contient 18 tests artificiels exacts. Ils prouvent que les règles unitaires principales fonctionnent : continuation autorisée, tiret autorisé, frontière U+000C, pagination finale, pagination interne conservée, dialogue, casse, accents, cas ambigu, titre, ligne vide, tiret inconnu et marqueurs PDF conservés.

Ils ne prouvent pas la justesse linguistique des 40 fusions réelles, ni que tous les paragraphes du PDF sont reconstruits, ni que les glyphes PDF suspects sont réparables. Résultat relancé : 18 tests, 18 réussis, 0 échoué.

## Invariant par page

L'invariant de `preprocess.sh` compare, page par page, les caractères non blancs avant/après après retrait de la seule pagination finale autorisée côté source. Il garantit qu'aucun caractère non blanc n'est perdu, ajouté ou déplacé vers une autre page, hors pagination. Il vérifie indirectement casse, accents, tirets et ponctuation conservés.

Il ne garantit pas qu'une fusion linguistique soit correcte : deux lignes incorrectement réunies peuvent conserver exactement les mêmes caractères non blancs dans la même page et donc satisfaire l'invariant.

## SHA-256

Les SHA-256 des trois sources extraites sont identiques avant/après pipeline :

- `Fondation.txt` : `b10a71e7705cc2da41cc7e41817d568aebaf65ea263ba59d745ffb1934f2e54c`
- `Fondation_et_empire.txt` : `547c7c3be6a7dcd362a3ad6b85f6dff41bf7609e9b5c54bb851b718fe73d2b2c`
- `Seconde_Fondation.txt` : `803011045188f19d2df09577390817fcdf74d56dac7c9bcd3b41549b13ba183e`

## UTF-8, casse et accents

Les entrées et sorties sont validées en UTF-8 strict par `iconv` dans `preprocess.sh`. Le test de démarrage GNU awk vérifie la longueur multioctet et la classification `[[:lower:]]` sous `LC_ALL=C.utf8`. Les tests conservent accents et ligatures de l'exemple. Le pipeline ne contient aucune conversion globale en minuscules, aucune normalisation d'accents et aucune suppression générale de ponctuation.

## Limites restantes

- Les glyphes `(cid:n)`, `¶` et plusieurs `°` restent des défauts du brut, non corrigés par la tâche 4.
- Les 66 tirets ambigus sont conservés.
- Les retours de ligne non fusionnés restent nombreux et devront être traités conceptuellement à la tokenisation.
- Les paragraphes originaux du PDF ne sont pas garantis, car l'extraction brute ne conserve pas toujours des lignes vides.

## Conclusion

Aucune transformation certainement incorrecte n'a été trouvée dans les 40 fusions ni dans les 10 raccords avec tiret. Les compteurs annoncés sont confirmés par relance réelle. Les sources extraites restent immuables. Le prétraitement conservateur de la tâche 4 est validable, avec les limites documentées ci-dessus.
