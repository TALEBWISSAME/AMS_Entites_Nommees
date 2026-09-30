# Décisions techniques

Ce registre distingue les choix validés des choix restant à étudier. Le prétraitement conservateur de la tâche 4 est implémenté et testé ; les choix NLP ultérieurs restent ouverts.

## Contraintes fixées

- Python simple et lisible ; dépendances à définir au début du développement.
- Corpus local dans `corpus/`, ignoré par Git, jamais publié ni modifié.
- Ressources textuelles produites en UTF-8.
- Développement progressif, avec vérification de chaque étape.

## Choix à étudier

| Choix | Statut | Justification / observations |
| --- | --- | --- |
| Périmètre des romans | Confirmé le 30 septembre 2026 | Fondation, Fondation et empire et Seconde Fondation uniquement, sur confirmation de l’étudiant. Les deux PDF supplémentaires ont été retirés de `corpus/`. |
| Extraction technique PDF | Décidé le 30 septembre 2026 | `pdfplumber==0.11.9`, déjà installé, extraction page par page sans OCR ni correction. Dépendance déclarée dans requirements.txt. |
| Localisation du corpus | Décidé le 30 septembre 2026 | Racine issue de `Path(__file__).resolve().parents[2]` et liste explicite des trois noms, indépendante du dossier courant. |
| Format intermédiaire brut | VALIDÉ | TXT UTF-8 sans BOM dans `results/extracted/`, local et ignoré par Git car il contient le texte des romans. Aucun nettoyage. |
| Frontières des pages | VALIDÉ | Un caractère technique U+000C (`\f`) entre deux pages, sans séparateur final. Absent des pages sources (vérifié), il pourra être traité ultérieurement. |
| Vérification des exports | VALIDÉ | Relecture UTF-8 stricte, comparaison intégrale avec les pages en mémoire, contrôle de taille et de caractères hors séparateurs. Retours de ligne conservés sans conversion. |
| Mesures techniques provisoires | Décidé le 30 septembre 2026 | Caractères sans séparateurs ajoutés, lignes par page, estimation des mots par split() sur les blancs ; aucune tokenisation NLP. |
| Méthode de tokenisation | À décider | À renseigner après étude du corpus et du sujet. |
| Prétraitement Bash + GNU awk | VALIDÉ pour la tâche 4 | Bash orchestre, GNU awk 5.3.2 traite sous C.utf8. Voir PRETRAITEMENT.md. |
| Pagination | VALIDÉ pour la tâche 4 | Ligne entière au format ± entier ± ou - entier -, en fin de page uniquement. |
| Frontières pendant le prétraitement | VALIDÉ | U+000C préservé ; aucune fusion à travers les pages manquantes. |
| Retours de ligne | VALIDÉ pour la tâche 4 | Continuations ciblées préposition/déterminant ; cas ambigus conservés. Limites détaillées dans PRETRAITEMENT.md. |
| Traitement de la ponctuation | Conservation validée au prétraitement | Aucune suppression générale ; politique de tokenisation à décider. |
| Caractères spéciaux et apostrophes | Conservation validée au prétraitement | Pas de normalisation ; glyphes ambigus conservés. |
| Gestion de la casse | Conservation validée | Une majuscule n’est pas une preuve d’entité nommée. |
| Gestion des accents | Conservation validée | Aucune substitution ni suppression. |
| Gestion des mots coupés | Politique conservatrice validée | Liste restreinte de formes réunies sans supprimer le tiret ; autres cas conservés. Aucun raccord interpage. |
| Statistiques finales | À décider | Selon les consignes et les besoins du rapport. |
| Fréquences et modèle de langue | À décider | Structures et méthode à justifier. |
| Règles de construction de L | À décider | Après observation du bruit réel. |
| Heuristiques de raffinement vers LP | À décider | À évaluer sur les résultats réels. |
| Méthode de construction de LL | À décider | Selon les catégories du sujet. |
| Regex, antidictionnaire et informations POS | À décider | Pertinence à vérifier. |
| FreeLing / NLTK ou aucun des deux | À décider | Selon les besoins et la compatibilité avec les consignes. |
| Utilisation des co-occurrences et taille de fenêtre | À décider | Seulement si pertinent. |
| Protocole d’évaluation | À décider | Selon les consignes et les données disponibles. |

Lorsqu’un choix sera validé, noter sa date, sa justification, les observations et les vérifications qui le soutiennent.
