# AXIOM Hackathon - Offline baseline v0.1

Author/project owner: Franck Melka. Code prepared with AI assistance on 2026-11-01.
This new standalone baseline does NOT import the pre-existing AXIOM kernel.
It is not yet a Meta-powered or hackathon-ready submission.

## Run
Python standard library only. No installation or credentials required.

    python review.py
    open outputs/report.html

## Scope
Three fictional, structured JSON dossiers (quote, invoice, installation).
R01: missing required document -> REVIEW.
R02: malformed JSON or invalid required fields -> BLOCK.
R03/R04/R05: case ID, item or quantity disagree -> REVIEW.
BLOCK takes precedence over REVIEW. Otherwise ALLOW for these checks only.
Human business decision stays PENDING; no approval action is implemented.
Hashes record the exact source bytes, not their truth or authenticity.
This does not detect fraud or establish regulatory compliance.

## Expected outcomes
coherent: ALLOW; incomplete: REVIEW; contradictory: REVIEW.
No AI analysis is simulated or claimed. No network calls are made.

## Next increment
Actual Meta extraction and contradiction review, validated output schemas,
evidence references, bounded calls and a recorded human review action.
Only after successful real API tests can this be presented as using Meta.

## Installation
Place this folder inside ~/dev/axiom-meta-hackathon.
It does not replace .gitignore, requirements.txt, .venv or existing AXIOM code.
Outputs are generated locally and should remain excluded from Git.
