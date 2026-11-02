# Revue des essais du 2 novembre 2026

Source examinée : archive fournie par Franck,
`20261102T090527963351Z.zip`. Il s'agit de rapports locaux et de métadonnées
enregistrées par le client, pas d'une attestation indépendante du fournisseur.

| Dossier / essai | Statut | Réponses | Entrée | Sortie |
|---|---|---:|---:|---:|
| Contradictoire | REVIEW | 2 | 1026 | 3197 |
| Cohérent | ALLOW | 2 | 1026 | 3518 |
| Incomplet initial | BLOCK | 1 | 326 | 2766 |
| Incomplet après diagnostic | REVIEW | 2 | 776 | 2714 |

Vérifications réalisées sans API : quatre empreintes de rapports égales au manifeste,
dix empreintes de textes sources vérifiées, vingt-quatre champs acceptés conformes
à leurs citations et trois citations du constat de quantité valides. Sept identifiants
de réponse distincts, tous avec statut completed. Total : 3154 tokens d'entrée,
12195 tokens de sortie. Les tokens de raisonnement sont inclus dans la sortie.

Les constats sont issus des règles locales R01, R03 et R00. Aucun R04 n'a été
enregistré : ces essais ne démontrent donc aucune détection supplémentaire par
le Contradicteur. Les décisions humaines sont toutes PENDING dans cette archive.

Le premier BLOCK rejette une valeur non conforme à la source. La valeur rejetée
n'étant pas conservée dans cette version, la cause précise reste inconnue.
Le nouvel essai REVIEW après ajout de diagnostic ne prouve pas une correction
du comportement du modèle. Tous les résultats, y compris cet échec, sont conservés.

La v0.3 introduit un prompt de Contradicteur révisé, des citations multiples,
deux dossiers sémantiques et des décisions humaines séparées. Ces ajouts n'ont
pas encore été évalués par des appels Meta réels lors de leur préparation.
