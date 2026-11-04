# AXIOM — final recording script

Target: under three minutes, approximately 330 spoken words. Rehearse once.
This is a replay of recorded Meta API runs on fictional, labeled text documents.
Opening these reports makes no API calls. Keep API keys and billing off screen.

## Prepare the three browser tabs (Mac)

```sh
cd ~/dev/axiom-meta-hackathon
open outputs/meta-semantic-conflict/report.html
open outputs/meta-semantic-clear/report.html
open outputs/meta-semantic-conflict/decisions/20261102T153132723844Z-92396514a2ee/report.html
```

Use the first tab for the problem and citations, second for the resolved control,
third for the human decision. The recording shows existing evidence, not a new run.

## 0:00–0:25 — Problem and introduction

“I'm Franck Melka, and this is AXIOM, the Governed Hive. A quotation, an invoice
and an installation report can agree on quantities while disagreeing on whether
the work is complete. AXIOM helps a human reviewer investigate that gap.
These are fictional documents and recorded Meta API results.”

## 0:25–0:55 — Architecture

“The Analyst uses Meta Muse Spark to extract labeled fields with source citations.
A second request to the same model, the Contradictor, examines the original text.
Python validates exact citations, extracted values and local consistency rules.
The beekeeper, the human reviewer, retains the business decision.
Two model requests maximum, with no automatic retries.”

Show the four stages and expand Accepted extraction briefly.

## 0:55–1:35 — The semantic conflict

“Here, all three documents report one hundred units. Quantity checks alone pass.
But the invoice says commissioning is complete, while the installation report
says circuits remain disconnected and a return visit is required.
The Contradictor raised two concerns. These highlighted quotations link each
concern to the source text. The result is REVIEW: a person must investigate.
Exact citations establish what the document says, not whether it is true.”

Show both R04 findings and their citations slowly.

## 1:35–1:55 — Control case

“In this second dossier, an earlier reservation was explicitly resolved before
handover. This recorded run raised no additional concern and returned ALLOW.
ALLOW means the listed checks passed. It never authorizes payment.”

Switch to semantic_clear, show result and source resolution.

## 1:55–2:30 — Human decision

“I reviewed the conflict and recorded REQUEST_CHANGES, asking for evidence of
resolution and clarification of the invoice before approval.
The decision is stored separately, with my reason and a hash linking it to this
exact report snapshot. The original REVIEW remains unchanged.
This is a local, self-declared reviewer record, not authenticated signing.”

Switch to the decision tab; show Recorded human decision and justification.

## 2:30–2:55 — Evidence and limits

“We preserved all six trials, including an initial extraction failure that was
blocked. Twenty-eight offline tests check the software safeguards; they do not
measure model accuracy. Next steps are broader evaluation and reviewer authentication.
AXIOM makes proposals inspectable and keeps business authority with the beekeeper.”

End on the human decision. Leave a few seconds of margin.

## Remaining delivery steps

Record and inspect audio, legibility and duration. Check current event requirements
and submission fields before publication. Repository publication, PR merge and final
submission are separate actions. Do not repeat API calls solely to record the video.
