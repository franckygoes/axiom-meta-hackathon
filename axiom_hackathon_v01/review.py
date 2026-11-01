"""AXIOM hackathon v0.1: deterministic offline baseline, no AI calls."""
import argparse
import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def review(folder):
    evidence, findings, docs = [], [], {}
    for role in ('quote', 'invoice', 'installation'):
        path = folder / (role + '.json')
        if not path.is_file():
            findings.append({'rule': 'R01', 'status': 'REVIEW', 'detail': 'Missing required document: ' + role, 'sources': []})
            continue
        raw = path.read_bytes()
        evidence.append({'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest()})
        try:
            doc = json.loads(raw)
            if not isinstance(doc, dict):
                raise ValueError('Expected an object')
            if not isinstance(doc.get('case_id'), str) or not doc['case_id'].strip():
                raise ValueError('Invalid case_id')
            if not isinstance(doc.get('item'), str) or not doc['item'].strip():
                raise ValueError('Invalid item')
            if type(doc.get('quantity')) is not int or doc['quantity'] <= 0:
                raise ValueError('quantity must be a positive integer')
            docs[role] = doc
        except (ValueError, UnicodeError) as exc:
            findings.append({'rule': 'R02', 'status': 'BLOCK', 'detail': role + ': ' + str(exc), 'sources': [path.name]})
    for field, rule in [('case_id', 'R03'), ('item', 'R04'), ('quantity', 'R05')]:
        values = {role: doc[field] for role, doc in docs.items()}
        if len(set(values.values())) > 1:
            findings.append({'rule': rule, 'status': 'REVIEW', 'detail': 'Conflicting ' + field + ': ' + json.dumps(values), 'sources': [role + '.json#/' + field for role in values]})
    status = 'BLOCK' if any(f['status'] == 'BLOCK' for f in findings) else ('REVIEW' if findings else 'ALLOW')
    return {'case': folder.name, 'mode': 'OFFLINE_DETERMINISTIC', 'meta_called': False, 'created_utc': datetime.now(timezone.utc).isoformat(), 'status': status, 'meaning': 'ALLOW means listed automated checks passed; it is not business approval.', 'human_decision': 'PENDING', 'findings': findings, 'evidence': evidence}

def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=['coherent', 'incomplete', 'contradictory', 'all'], default='all')
    args = parser.parse_args()
    cases = ['coherent', 'incomplete', 'contradictory'] if args.case == 'all' else [args.case]
    out = ROOT / 'outputs'
    out.mkdir(exist_ok=True)
    reports = [review(ROOT / 'fixtures' / case) for case in cases]
    cards = []
    for report in reports:
        (out / (report['case'] + '.json')).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        print(report['case'] + ': ' + report['status'])
        cards.append('<article><h2>' + html.escape(report['case']) + ' <span>' + report['status'] + '</span></h2><p>Human decision: PENDING</p><pre>' + html.escape(json.dumps(report, indent=2)) + '</pre></article>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>AXIOM | Offline baseline</title><style>body{background:#0c1525;color:#e8effb;font:16px system-ui;max-width:1050px;margin:40px auto;padding:0 20px}h1{font-size:38px}p{line-height:1.6;color:#b7c7e0}article{background:#15233a;border:1px solid #314462;border-radius:12px;padding:24px;margin:20px 0}span{color:#82bdff;font-size:18px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}</style><h1>AXIOM | The Governed Hive</h1><p>Offline baseline v0.1 - fictional structured documents. No AI inference, no Meta API calls. Explicit checks and source hashes only.</p><p>ALLOW: listed checks passed. REVIEW: human review required. BLOCK: invalid input prevents validation. All business decisions remain pending.</p>''' + ''.join(cards) + '</html>'
    (out / 'report.html').write_text(page, encoding='utf-8')
    print('Report: ' + str(out / 'report.html'))

if __name__ == '__main__':
    run()
