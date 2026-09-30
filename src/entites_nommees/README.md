# Développement du TP Entités Nommées

`corpus_reader.py` réalise uniquement l’inspection technique des trois PDF explicitement retenus. Chaque phase suivante sera testée avant de passer à la suivante, sur demande explicite.

L’option `--export` ajoute l’écriture des trois TXT bruts UTF-8 dans `results/extracted/`, sans dupliquer l’extraction. Les noms sont `Fondation.txt`, `Fondation_et_empire.txt` et `Seconde_Fondation.txt`. Ce dossier reste local, ignoré par Git ; aucun texte n’est nettoyé. Une relance régénère ces fichiers.

Chaque TXT contient les chaînes extraites dans l’ordre, séparées par un unique caractère `\f` (U+000C), sans séparateur final. Ce caractère est ajouté par le programme et ne vient pas du roman. Une collision avec le texte source provoque une erreur explicite. Les retours de ligne ne sont pas convertis à l’écriture. La relecture UTF-8 stricte vérifie l’égalité complète avec le texte en mémoire et avec chaque page. Les caractères du fichier incluent les N−1 séparateurs ; les statistiques de caractères extraits les excluent. Les lignes restent comptées page par page pour être comparables à la tâche 1. `split()` reste un comptage brut, pas une tokenisation NLP.

## Inspection technique

Commande depuis la racine : `python src/entites_nommees/corpus_reader.py`.
Dépendance : `pdfplumber==0.11.9`, déjà présente dans l’environnement de validation et déclarée dans `requirements.txt`.

Les textes sont extraits page par page sans OCR, nettoyage ni normalisation explicite, et restent en mémoire. Un saut de page `\f` est ajouté entre pages pour empêcher de fusionner leurs mots. Les caractères sont comptés sur les chaînes originales retournées par la bibliothèque, sans ces séparateurs ajoutés ; les lignes sont la somme des `splitlines()` par page. Les pages contenant uniquement des blancs sont considérées sans texte. Le compte `split()` sépare sur les blancs (espaces, sauts de ligne, etc.) : c’est une estimation brute, pas une tokenisation NLP. L’aperçu est limité aux 350 premiers caractères de la première page contenant du texte.

Le programme poursuit l’inspection des autres romans en cas d’erreur, affiche la cause et termine avec un code non nul si un fichier échoue ou ne contient aucun texte. Un bilan partiel est explicitement signalé. Les PDF originaux ne sont jamais écrits ; seuls les TXT intermédiaires sont écrits avec `--export`.

1. **Lecture et compréhension du corpus** : parcourir les fichiers, prévoir une lecture UTF-8, vérifier les formats et gérer proprement les erreurs, sans modifier les originaux.
2. **Statistiques initiales** : compter les fichiers, caractères et lignes ; compléter après définition de la tokenisation. Les statistiques finales dépendront des consignes et des besoins du rapport.
3. **Prétraitement** : étudier ponctuation, caractères spéciaux, apostrophes, traits d’union, casse, accents et mots potentiellement coupés avant de décider. Ne pas supprimer automatiquement toute la ponctuation.
4. **Tokenisation** : définir une stratégie, l’implémenter, la tester et vérifier les cas particuliers.
5. **N-grammes** : générer les unigrammes (n=1), bigrammes (n=2) et trigrammes (n=3).
6. **Fréquences / modèle de langue** : compter les occurrences, créer les structures nécessaires, étudier les régularités et éventuellement les co-occurrences si pertinentes.
7. **Analyse du bruit** : observer les n-grammes réellement obtenus avant de fixer les heuristiques.
8. **Heuristiques pour les candidats** : étudier capitalisation, fréquence, structure des n-grammes, regex, antidictionnaire, informations POS et autres critères justifiables. Une majuscule n’est pas une preuve d’entité nommée.
9. **Production de L** : produire la liste générale des candidats.
10. **Raffinement L → LP** : identifier les personnes/personnages par raffinements et heuristiques.
11. **Production de LL** : identifier les lieux/catégories du sujet à partir de L, LP et des informations disponibles.
12. **Évaluation** : étudier faux positifs, faux négatifs, bruit restant, entités manquantes et limites de la méthode.
13. **Résultats finaux** : produire les fichiers nécessaires en UTF-8.

Le [plan de réalisation](../../docs/PLAN_REALISATION.md) suit ces étapes ; les choix seront consignés dans [les décisions](../../docs/DECISIONS.md).
