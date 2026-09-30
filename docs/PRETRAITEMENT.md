# Prétraitement du corpus

## Objectif

Tâche 4 : retirer uniquement les artefacts suffisamment certains et effectuer quelques raccords internes prudents. Les cas ambigus restent inchangés. Aucun texte manquant n’est inventé. Aucune tokenisation, aucun n-gramme et aucune liste L/LP/LL ne sont produits.

Ces règles répondent au prompt de réalisation validé par l’étudiant. Ce sont nos choix techniques conservateurs, et non des obligations algorithmiques attribuées au professeur. L’audit historique décrit les TXT bruts et reste inchangé.

## Pourquoi Bash + AWK

Bash orchestre les fichiers et contrôles ; GNU awk traite les pages puis leurs lignes. Aucun prétraitement n’est implémenté en Python. Environnement vérifié : Git Bash sous Windows, GNU Awk 5.3.2, locale `C.utf8`. Un test réel de longueur et de classification des caractères accentués est effectué au démarrage. `iconv` vérifie l’encodage UTF-8 des entrées et sorties.

## Entrées

Les trois fichiers `Fondation.txt`, `Fondation_et_empire.txt`, `Seconde_Fondation.txt` dans `results/extracted/`. Liste fixe, sans recherche de tous les TXT du dossier. SHA-256 calculés avant et après ; ces sources sont immuables. Les PDF ne sont pas ouverts par ce traitement.

## Sorties

Les trois mêmes noms dans `results/processed/`, en UTF-8. Ce dossier est ignoré par Git car il contient toujours le texte des romans. Une relance régénère les sorties. `results/preprocessing_report.txt` ne contient que des statistiques, informations techniques et empreintes ; il est versionnable.

## Architecture Bash/AWK

- `scripts/preprocess.sh` : racine relative au script, dépendances, locale, sources, SHA-256, appels AWK, validation UTF-8 et invariants par page, publication des sorties et agrégation du rapport. Les sorties sont préparées dans des fichiers temporaires avant remplacement individuel. En cas d’erreur sur un roman, le code retour est non nul ; les sorties des romans précédents peuvent déjà avoir été régénérées.
- `scripts/preprocess.awk` : pagination, jonctions internes, frontières et compteurs. `RS="\f"` délimite une page ; `RT` reproduit la frontière reçue. Les lignes sont traitées en mémoire à l’intérieur de cette seule page.
- `tests/test_preprocess.sh` : petits exemples artificiels, comparaisons exactes d’octets.

Depuis Git Bash à la racine :

```bash
bash tests/test_preprocess.sh
bash scripts/preprocess.sh
```

Depuis PowerShell, avec Git installé à l’emplacement de cette machine :

```powershell
& 'C:\Program Files\Git\bin\bash.exe' scripts/preprocess.sh
```

Depuis un autre dossier, donner le chemin absolu de `preprocess.sh`. Outils requis : Bash, GNU awk, iconv, sha256sum et utilitaires usuels de Git Bash/coreutils. Aucun ajout aux dépendances Python.

## Frontières de pages

U+000C (`\f`) est conservé exactement, sans fusion ni état de raccord partagé entre pages. Il signale une discontinuité : une page paire manque entre deux pages impaires. Les 107, 115 et 119 frontières sont conservées. Les futures étapes devront respecter cette séparation ; aucun n-gramme ne devra être créé artificiellement à travers elle.

## Pagination

Suppression uniquement de la dernière ligne non vide d’une page correspondant intégralement à `± entier ±` ou `- entier -`, avec espaces/tabulations facultatifs. Les nombres narratifs et les lignes de même forme à l’intérieur d’une page sont conservés. Aucune suppression générale de `±`, des nombres ou des tirets.

Revue des données : les 343 lignes supprimées correspondent toutes à la séquence de pagination attendue `2 × indice_page_PDF + 1` (indices à partir de 1). Cette vérification indépendante renforce le diagnostic ; la règle de transformation repose sur le format et la position, pas sur une liste de numéros codée en dur.

## Retours à la ligne

Fusion avec un espace seulement si la ligne précédente originale comporte au moins 25 caractères, finit par une préposition parmi `par, dans, avec, sans, sous, chez, vers, entre`, et si la suivante commence par un déterminant parmi `le, la, les, un, une, des, du, de, ce, cette, ces, son, sa, ses, leur, leurs` suivi d’un espace.

Les lignes vides, indentées, commençant par un marqueur de dialogue/citation, ou entièrement composées de majuscules/chiffres et ponctuation de titre sont exclues. La longueur est celle de la ligne originale, jamais celle d’un bloc déjà fusionné. Il s’agit d’un critère de continuation probable très limité, pas d’une analyse syntaxique ni d’une preuve absolue.

## Paragraphes

Les lignes vides et les autres ruptures structurelles reconnues sont conservées. L’extraction brute ne contient aucune ligne vide : elle ne permet donc pas de garantir la récupération des paragraphes du PDF. Aucun nouveau paragraphe n’est inventé. Une rupture non suffisamment justifiée reste présente.

## Dialogues

Les tirets de dialogue sont préservés. La règle de continuation avec espace exclut les lignes commençant par `-`, `–`, `—`, `«`, guillemet droit ou apostrophe droite. La réunion d’un composé au sein d’un dialogue peut conserver sa structure et son tiret ; aucune nouvelle réplique n’est absorbée.

## Tirets

Réunion sans espace et sans supprimer le tiret uniquement pour les paires explicitement reconnues : `années-lumière`, `vous-même`, `vous-mêmes`, `Dites-moi`, `dites-moi`, `eux-mêmes`, `au-dessus`, `au-dessous`, `diriez-vous`. Le mot final avant le retour et le premier mot suivant doivent former exactement une de ces graphies.

Cette liste étroite est issue des formes discutées dans le cadrage et l’audit. Elle ne constitue ni un lexique d’entités ni une correction orthographique générale. Les autres formes restent séparées, même lorsqu’une correction paraît plausible. Aucun raccord à travers U+000C.

## Apostrophes

Conservées telles quelles ; aucune normalisation. Le corpus observé emploie des apostrophes ASCII.

## Casse

Conservée intégralement. Aucune conversion générale ou locale en minuscules.

## Accents

Conservés ; aucune normalisation Unicode ni substitution. Le traitement multioctet de GNU awk est vérifié, ainsi que l’UTF-8 strict via iconv. Les tests comprennent `é è ê à ù ç œ Œ`.

## Ponctuation

Conservation générale, y compris tirets, apostrophes et frontières de phrases. Seuls les signes appartenant à une ligne de pagination supprimée disparaissent. La politique linguistique de tokenisation reste à décider.

## Artefacts PDF

Les paginations sont les seuls artefacts supprimés. `¶`, `(cid:n)` et `°` restent en place : leur caractère d’origine n’est pas deviné. Un signe degré peut être légitime. Les compteurs de marqueurs laissés ne représentent donc pas un nombre certain d’erreurs.

## Cas ambigus

`tirets_ambigus` compte les jonctions internes lettres-tiret/lettres non reconnues par la liste. `cas_ambigus` inclut ces cas ainsi que les transitions internes non structurelles sans ponctuation finale reconnue qui ne satisfont pas la règle de fusion. C’est un compteur d’occasions conservées, pas un décompte exhaustif des anomalies.

`lignes_fusionnees` compte les retours remplacés par un espace ; `tirets_reunis` compte séparément les retours supprimés sans espace. `lignes_conservees` est le nombre de lignes de sortie, blocs fusionnés inclus. `artefacts_certains_traites` compte les lignes de pagination : il ne faut pas l’additionner à `pagination_supprimee`.

## Tests

18 tests artificiels réussis : continuation autorisée, composé avec tiret, frontières simples et devant tiret/continuation, pagination finale, pagination interne conservée, symbole narratif, dialogue et sa continuation conservée, casse, accents/ligatures, ambiguïté, titre, ligne vide, tiret inconnu et marqueurs PDF.

Sur les romans : UTF-8 valide ; SHA-256 bruts identiques avant/après ; même séquence de caractères non blancs dans chaque page après exclusion de la seule pagination autorisée. Ce dernier contrôle vérifie notamment casse, accents, tirets, ponctuation conservée et absence de déplacement de texte entre pages. Il ne prouve pas que chaque fusion linguistique est correcte.

Revue limitée de transformations : composés `années-lumière`, `eux-mêmes`, `au-dessus` et continuations internes observées sans corruption visible. Aucun faux positif de pagination trouvé dans les 343 positions contrôlées. Les frontières restent une barrière absolue ; les paragraphes demandent une revue linguistique complémentaire.

| Mesure | Fondation | Fondation et Empire | Seconde Fondation | Total |
| --- | ---: | ---: | ---: | ---: |
| Caractères avant, hors U+000C | 205057 | 226390 | 237404 | 668851 |
| Caractères après, hors U+000C | 204243 | 225511 | 236500 | 666254 |
| Lignes avant | 3989 | 4361 | 4407 | 12757 |
| Lignes après | 3868 | 4228 | 4268 | 12364 |
| Pagination supprimée | 108 | 116 | 119 | 343 |
| Jonctions avec espace | 10 | 13 | 17 | 40 |
| Tirets réunis | 3 | 4 | 3 | 10 |
| Tirets ambigus conservés | 14 | 20 | 32 | 66 |
| Marqueurs laissés | 23 | 40 | 5 | 68 |
| Cas ambigus conservés | 2014 | 2166 | 2454 | 6634 |

Les 68 marqueurs restants comprennent 8 `(cid:n)`, 8 `¶` et 52 `°`. Les 448 signes `±` ont disparu uniquement avec leurs lignes de pagination. Les statistiques exactes et empreintes figurent dans `results/preprocessing_report.txt`.

## Limites

Le résultat n’est pas un texte parfait : 66 coupures avec tiret restent ambiguës, de nombreux retours typographiques sont conservés et certains glyphes restent défectueux. Les pages absentes ne peuvent pas être reconstituées. La règle de continuation est prudente mais reste heuristique ; sa pertinence et les frontières de paragraphes doivent être validées avant tokenisation.

Aucune tâche 5 n’est commencée. Points à valider : qualité des 40 fusions, éventuelle extension de la liste des composés, comparaison des glyphes suspects aux PDF, statut des paragraphes et respect des frontières de pages dans les étapes futures.
