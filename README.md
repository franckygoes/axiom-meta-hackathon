# AXIOM | The Governed Hive — v0.3.0

Prototype de revue de dossiers fictifs pour le Meta Global AI Developer Hackathon.
Le dossier contient un devis, une facture et un compte rendu d'installation.
Le modèle propose une extraction, une seconde requête recherche les problèmes,
puis des contrôles Python vérifient les preuves et les contradictions.
La décision métier reste **PENDING** tant que l'apiculteur ne l'a pas enregistrée
séparément avec une justification. Aucune approbation automatique.

## Démonstration gratuite, sans clé ni réseau

Depuis la racine du dépôt, avec Python 3.10 ou plus :

```sh
python3 -m unittest discover -s tests -v
python3 -m hive --mode fixture
open outputs/hive/report.html
```

Résultats hors ligne : coherent ALLOW, incomplete REVIEW, contradictory REVIEW.
Les nouveaux semantic_conflict et semantic_clear donnent ALLOW hors ligne : les
champs concordent, mais leur sens n’est pas évalué par le substitut déterministe.
Le mode `OFFLINE_FIXTURE` est un substitut déterministe, **pas une inférence IA**.
Les documents sont du texte fictif à champs explicitement étiquetés. Il ne s'agit
pas encore d'une extraction générale de PDF, scans ou documents libres.

## Essai Meta : crédits disponibles ou facturation acceptée

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
Le 2 novembre 2026, les sorties Terminal partagées par Franck montrent des essais
META_LIVE : coherent ALLOW, contradictory REVIEW, incomplete BLOCK puis REVIEW.
Le premier essai contradictoire dispose de deux réponses completed dans l'audit
partagé. Les quatre rapports ont ensuite été examinés : voir [revue des preuves](docs/EVIDENCE_REVIEW.md).
Les deux essais sémantiques v0.3 ont ensuite été examinés : semantic_conflict
REVIEW avec deux constats R04, semantic_clear ALLOW sans constat supplémentaire.
Franck a enregistré REQUEST_CHANGES sur le conflit. Les six essais, dont le
premier BLOCK, sont conservés. Ces quelques essais ne mesurent pas la fiabilité générale.

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
journal inviolable. Une décision humaine peut être enregistrée avec `python -m hive.decision`.
Elle est liée à une copie du rapport par SHA-256, sans signature ni authentification.
APPROVE exige ALLOW ; les états REVIEW/BLOCK ne peuvent être approuvés.
Une décision n'exécute aucun paiement ni action externe.

## Contributions et suite

`axiom_hackathon_v01/` conserve le premier moteur hors ligne JSON. `hive/` ajoute
le parcours à deux étapes, les documents texte, les preuves contrôlées et le
rapport ; `tests/` vérifie les barrières sans API. Aucun ancien noyau AXIOM n'est
importé. Ce prototype a été construit pendant le hackathon avec assistance Codex.

À terminer avant la soumission : vidéo de démonstration de trois minutes,
vérification des règles et du formulaire, puis accès au dépôt conforme aux exigences
des organisateurs. Les essais réels et la décision humaine sont documentés.

## Conserver les essais et préparer la démonstration

```sh
python -m hive.evidence
```

Cette commande lit les quatre essais initiaux et les deux essais sémantiques présents,
collecte les décisions liées aux rapports, préserve les JSON
originaux (y compris le premier BLOCK), et crée un ZIP daté, un manifeste avec
empreintes et un rapport combiné sous `outputs/evidence/`. Aucun appel réseau.
Les fichiers absents sont signalés. Aucun fichier de clé ou environnement n'est
collecté. Les rapports contiennent leurs sources et les identifiants de réponse :
inspecter l'archive avant de la partager. Les sorties restent exclues de Git.

Le [scénario de démonstration](docs/DEMO.md) fournit un déroulé anglais de trois
minutes et distingue les rôles du modèle, du validateur et de l'apiculteur.

## Reprise guidée

Voir [la séance de reprise](docs/RETURN_SESSION.md) pour les commandes exactes,
les hypothèses des deux essais sémantiques et la décision de l’apiculteur.
La v0.3 consigne sa version et les empreintes des prompts dans chaque rapport.
