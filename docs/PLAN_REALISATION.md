# Plan de réalisation

L’architecture et la première inspection technique sont réalisées : ouverture des trois PDF, extraction en mémoire, aperçus et statistiques brutes. Les phases 1 et 2 ont ainsi un premier bilan technique, sans prétraitement ni statistiques NLP. Toutes les étapes suivantes attendent une autorisation explicite. Tester et documenter chaque phase avant la suivante.

Les documents du professeur sont maintenant archivés dans `docs/` et résumés dans [CONSIGNES_PROF.md](CONSIGNES_PROF.md). Le rendu confirmé est un rapport de 2 à 3 pages sur les algorithmes, les listes L/LP/LL et les statistiques du corpus. Le périmètre est confirmé : Fondation, Fondation et empire et Seconde Fondation uniquement, soit les trois PDF conservés dans `corpus/`. La phase 1 devra étudier l’extraction PDF vers texte UTF-8, en préservant les originaux et les ruptures dues aux pages manquantes. Les supports Enertex/Artex n’ajoutent pas automatiquement des phases obligatoires au TP actuel.

| Phase | Travail prévu | Point à vérifier |
| --- | --- | --- |
| 1. Lecture et compréhension | Parcourir les fichiers, lire en UTF-8, vérifier les formats, gérer les erreurs. | Originaux inchangés ; problèmes d’encodage ou textes coupés identifiés. |
| 2. Statistiques initiales | Nombre de fichiers, caractères et lignes ; compléter après tokenisation. | Définition des mesures ; liste finale adaptée aux consignes et au rapport. |
| 3. Prétraitement | Étudier ponctuation, caractères spéciaux, apostrophes, traits d’union, casse, accents et mots coupés. | Choix justifiés ; aucune suppression automatique de toute la ponctuation. |
| 4. Tokenisation | Définir, implémenter et tester une stratégie. | Cas particuliers vérifiés. |
| 5. N-grammes | Générer unigrammes (n=1), bigrammes (n=2), trigrammes (n=3). | Cohérence avec la tokenisation retenue. |
| 6. Fréquences / modèle de langue | Compter les occurrences, préparer les structures, étudier les régularités ; co-occurrences si pertinentes. | Comptages vérifiés et choix expliqués. |
| 7. Analyse du bruit | Observer les n-grammes réellement obtenus. | Bruit décrit avant de fixer les heuristiques. |
| 8. Heuristiques des candidats | Étudier capitalisation, fréquence, structure, regex, antidictionnaire, POS et autres critères justifiables. | Une majuscule seule ne prouve pas une entité nommée. |
| 9. L | Produire la liste générale des candidats. | Aucun résultat inventé ; méthode documentée. |
| 10. LP | Raffiner L pour identifier les personnes/personnages. | Heuristiques explicables et vérifiées. |
| 11. LL | Identifier cités, organisations, universités, villes et planètes en exploitant L, LP et les informations disponibles. | Catégories conformes au sujet ; méthode documentée. |
| 12. Évaluation | Examiner faux positifs, faux négatifs, bruit restant, entités manquantes et limites. | Protocole et observations documentés. |
| 13. Résultats finaux | Générer les fichiers nécessaires en UTF-8. | Résultats réels, vérifiés, sans redistribution du corpus. |

Tenir à jour [DECISIONS.md](DECISIONS.md), le rapport et [CONTEXTE_PROJET.md](../CONTEXTE_PROJET.md) au fil du travail. Si une consigne manque, demander le document correspondant.
