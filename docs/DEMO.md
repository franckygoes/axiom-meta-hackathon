# AXIOM — demonstration rehearsal

Target duration: 3 minutes. Speak in English for an international audience.
Show existing META_LIVE reports; explicitly identify this as a replay of recorded
runs, not a new live inference. Do not show the API key or billing information.

## 0:00–0:25 — The problem

“A quotation and an invoice can agree while the installation record tells a
different story. AXIOM helps a reviewer compare that evidence. I am Franck Melka,
and I call this approach the Governed Hive: specialized bees work within explicit
rules, while the beekeeper keeps authority over the final decision.”

## 0:25–0:55 — What actually runs

“The Analyst uses Meta Muse Spark to extract fields and cite source lines. The
Contradictor is a second, independent request to the same model, looking for
unsupported claims or contradictions. Python checks the citations, field values
and cross-document consistency. These are two model stages and a deterministic
validator, not a swarm of independently deployed agents.”

Show source text and one extraction citation. Documents are fictional, explicitly
labeled text; do not describe this version as general PDF understanding.

## 0:55–1:35 — Three scenarios

“These are recorded API runs. The coherent dossier passed the listed checks.
The contradictory dossier had 100 units quoted and invoiced, but only 60 installed.
The local validator flagged the discrepancy. A missing installation document also
requires human review. ALLOW means checks passed; it does not authorize payment.”

Show coherent, contradictory and the latest incomplete report. Do not claim
that the Contradictor detected the quantity discrepancy unless its R04 findings
actually demonstrate that; the observed first report has an R03 local finding.

## 1:35–2:15 — The failure is part of the evidence

“The first incomplete-dossier run was blocked because an extracted value did not
match its cited source. We retained that failure. We then improved diagnostic
detail without relaxing acceptance rules. A subsequent run passed validation
and remained under review because the document was missing. That success does
not explain the original mismatch or establish reliability across future runs.”

Show the first BLOCK alongside the subsequent REVIEW. The rejected value from
the first run was not saved; never invent it or attribute a precise cause.

## 2:15–2:45 — Governance and limits

“Each run is bounded to two API calls, with no automatic retries. Reports include
source hashes and response usage. Hashes do not establish that a document is
true. The model can miss concerns. The final business decision stays pending:
human decision recording is still a next step.”

## 2:45–3:00 — Close

“AXIOM turns model proposals into reviewable evidence, with explicit checks and
visible failures. Next we will broaden evaluation and add recorded human review.
The beekeeper stays responsible for the Hive.”

## Before recording

- Run `python -m hive.evidence` to preserve all four existing runs without API use.
- Inspect the resulting combined report and manifest; keep the original BLOCK.
- Distinguish user-observed live results from automated offline tests.
- Check current submission requirements on the event platform before submission.
- The repository remains private; publication, PR merge and submission are separate actions.
