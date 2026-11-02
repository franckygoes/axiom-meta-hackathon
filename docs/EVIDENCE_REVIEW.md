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

## Évaluation v0.3 et décision humaine

Archives complémentaires examinées : `20261102T152810056108Z.zip`, puis
`20261102T153219871620Z.zip` incluant la décision de Franck et les six essais.

| Dossier / essai | Statut | Réponses | Entrée | Sortie |
|---|---|---:|---:|---:|
| semantic_conflict | REVIEW | 2 | 1279 | 5542 |
| semantic_clear | ALLOW | 2 | 1309 | 4079 |

Sur le conflit, deux constats R04 citent les affirmations incompatibles : facture
annonçant une mise en service complète, installation mentionnant des circuits
encore déconnectés et une visite supplémentaire nécessaire. Les cinq citations
de ces constats correspondent exactement aux lignes sources. Sur le témoin,
la réserve explicitement résolue n'a produit aucun constat supplémentaire.
Ces deux observations ne constituent pas un benchmark de précision.

Total des six essais : 11 réponses enregistrées, 5742 tokens d'entrée et 21816
 tokens de sortie, raisonnement inclus. L'échec initial demeure dans l'archive.

Franck Melka a enregistré REQUEST_CHANGES le 2 novembre 2026 à 15:31:32 UTC,
avec une justification demandant résolution et clarification avant approbation.
Le SHA-256 de l'instantané correspond à la décision et au rapport original
archivé. Le statut automatique reste REVIEW et le rapport original est inchangé.
L'identité est déclarative ; ce lien ne constitue ni signature, ni journal
inviolable, ni action externe. La capture fournie montre les citations et la
décision humaine lisibles dans le navigateur.
