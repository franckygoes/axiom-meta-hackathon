# AXIOM | The Governed Hive

Prototype de revue de dossiers fictifs pour le Meta Global AI Developer Hackathon.
Le dossier contient un devis, une facture et un compte rendu d'installation.
Le modèle propose une extraction, une seconde requête recherche les problèmes,
puis des contrôles Python vérifient les preuves et les contradictions.
La décision métier reste **PENDING** : aucune approbation automatique.

## Démonstration gratuite, sans clé ni réseau

Depuis la racine du dépôt, avec Python 3.10 ou plus :

```sh
python3 -m unittest discover -s tests -v
python3 -m hive --mode fixture
open outputs/hive/report.html
```

Résultats attendus : coherent ALLOW, incomplete REVIEW, contradictory REVIEW.
Le mode `OFFLINE_FIXTURE` est un substitut déterministe, **pas une inférence IA**.
Les documents sont du texte fictif à champs explicitement étiquetés. Il ne s'agit
pas encore d'une extraction générale de PDF, scans ou documents libres.

## Essai Meta : seulement après réception des crédits

Activer l'environnement `.venv`, installer les dépendances existantes, puis définir
`MODEL_API_KEY` dans le terminal sans l'inscrire dans un fichier versionné.
Ne jamais partager cette clé dans GitHub, les rapports ou une capture.

```sh
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m hive --mode meta --case contradictory --output outputs/meta-trial
open outputs/meta-trial/report.html
```

Le client utilise `https://api.meta.ai/v1`, `muse-spark-1.3` et Responses API.
Deux requêtes maximum par exécution, sans retry automatique, chacune limitée à
6 000 tokens de sortie et 120 secondes de délai client. Ces bornes ne constituent
pas un plafond financier. `store=False` est envoyé ; cela ne constitue pas une
garantie générale de non-rétention du fournisseur. Les sources quittent la machine
uniquement en mode Meta. N'utiliser ici que les exemples fictifs.

Références : [Quickstart Meta](https://dev.meta.ai/docs/quickstart),
[Responses API](https://dev.meta.ai/docs/protocols/responses).
L'intégration est prête à tester mais **aucun appel réel n'a été validé** à ce stade.

## Contrat de validation

- Chaque citation doit correspondre exactement à une ligne d'un document fourni.
- La valeur extraite doit correspondre au champ étiqueté de cette ligne.
- Un champ inconnu, un document absent ou une contradiction impose REVIEW.
- Une preuve invalide, un document vide/trop grand ou une erreur impose BLOCK.
- La seconde lecture peut signaler un problème ; elle ne peut annuler un contrôle local.
- ALLOW signifie uniquement que les contrôles listés sont passés.
- Les rapports incluent les sources, SHA-256, citations et métadonnées de requête.

La seconde lecture utilise le même modèle dans une requête indépendante : ce
n'est ni un vote de modèles distincts ni une garantie de détection exhaustive.
Les citations prouvent la présence du texte, pas sa véracité. Les consignes dans
les documents sont traitées comme des données, mais la résistance du modèle aux
injections devra être évaluée lors des essais réels.

Les sorties restent dans `outputs/`, exclu de Git. Les rapports ne sont pas un
journal inviolable. L'enregistrement d'une décision humaine n'est pas implémenté.

## Contributions et suite

`axiom_hackathon_v01/` conserve le premier moteur hors ligne JSON. `hive/` ajoute
le parcours à deux étapes, les documents texte, les preuves contrôlées et le
rapport ; `tests/` vérifie les barrières sans API. Aucun ancien noyau AXIOM n'est
importé. Ce prototype a été construit pendant le hackathon avec assistance Codex.

À terminer avant la soumission : essai Meta documenté après crédits, évaluation
des sorties réelles, vidéo de démonstration de 3 minutes, vérification des règles
et accès public au dépôt demandé par les organisateurs.
