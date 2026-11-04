# Reprise — v0.3.0

## 1. Mettre à jour et vérifier sans dépense

```sh
cd ~/dev/axiom-meta-hackathon
git switch codex/hive-v02
git pull --ff-only
source .venv/bin/activate
python -m unittest discover -s tests -v
python -m hive --mode fixture --output outputs/v03-offline
open outputs/v03-offline/report.html
```

Les deux nouveaux cas `semantic_conflict` et `semantic_clear` affichent ALLOW
en mode fixture : les champs structurés concordent et aucune analyse sémantique
n'est effectuée hors ligne. Ce résultat est attendu pour le témoin déterministe,
et ne démontre pas la cohérence de leur texte. Les tests utilisent des doublures
pour vérifier les contrôles de citations, pas pour prouver une capacité du modèle.

## 2. Deux essais Meta, chacun une seule fois

Ces deux commandes font au maximum quatre appels payants au total. Dans une
nouvelle fenêtre Terminal, saisir d'abord la clé (zsh sur le Mac) :

```sh
read -s "MODEL_API_KEY?Colle ta cle Meta puis appuie sur Entree : "
export MODEL_API_KEY
printf '\n'
```

Puis :

```sh
python -m hive --mode meta --case semantic_conflict --output outputs/meta-semantic-conflict
python -m hive --mode meta --case semantic_clear --output outputs/meta-semantic-clear
```

Hypothèses définies avant les essais :

| Cas | Quantités | Sens du texte | Résultat recherché |
|---|---|---|---|
| semantic_conflict | 100 partout | Facture : tout fonctionne. Chantier : circuits encore déconnectés. | REVIEW avec R04 et citations des deux affirmations |
| semantic_clear | 100 partout | Ancienne réserve explicitement résolue avant remise finale. | ALLOW, sans réserve inventée |

Un BLOCK reste un échec de validation à diagnostiquer, pas une réussite du
Contradicteur. Un ALLOW sur le conflit indique que l'analyse sémantique a manqué
ce cas. Un REVIEW sur le témoin doit être examiné pour un faux positif.
Conserver tous les essais, ne pas répéter jusqu'à obtenir le résultat voulu.
La v0.3 modifie le prompt du Contradicteur et le format des citations : elle doit
être évaluée séparément des sept réponses enregistrées avec les versions antérieures.

## 3. Enregistrer la décision de l'apiculteur

Lire d'abord le rapport. Exemple de demande de correction du dossier contradictoire,
à exécuter uniquement si cette décision reflète ton examen :

```sh
python -m hive.decision record outputs/meta-first/contradictory.json --decision REQUEST_CHANGES --actor "Franck Melka" --reason "Clarifier l'ecart entre 100 unites facturees et 60 installees avant toute decision."
```

La commande imprime un dossier daté et le chemin du nouveau rapport HTML.
Le rapport d'origine reste inchangé ; le statut automatique ne devient pas ALLOW.
APPROVE est possible uniquement pour un statut ALLOW, avec auteur et justification.
REJECT et REQUEST_CHANGES sont possibles sur les trois statuts.
Ce sont des décisions de démonstration sur des documents fictifs, sans action externe.

Pour contrôler le lien entre décision et instantané :

```sh
python -m hive.decision verify CHEMIN_DU_DOSSIER_DE_DECISION
```

Remplacer le dernier argument par le dossier indiqué. L'identité est déclarative,
les fichiers restent modifiables sur disque : aucune signature ni inviolabilité
n'est revendiquée. Des décisions successives sont gardées séparément, sans mécanisme
de révocation ou de « dernière décision faisant autorité ».

## 4. Rassembler les preuves

```sh
python -m hive.evidence
open outputs/evidence
```

L'archive inclut les essais sémantiques s'ils existent et les décisions dont
l'empreinte correspond exactement au rapport collecté. Partager le nouveau ZIP
pour examiner résultats, citations et consommation.

## Critères avant vidéo et soumission

- Tests hors ligne réussis ; deux essais sémantiques relus, y compris échecs éventuels.
- Décision réellement saisie par Franck et liée à son rapport.
- Vidéo présentant les capacités observées, pas les capacités espérées.
- Revue finale du dépôt, des instructions de l'événement et du formulaire.
- Publication du dépôt, fusion et soumission restent des étapes séparées.
