"""Record a self-declared human decision tied to an immutable report snapshot."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .review import render

DECISIONS = ('APPROVE', 'REQUEST_CHANGES', 'REJECT')


def record(report_path, decision, actor, reason):
    if decision not in DECISIONS or not actor.strip() or not reason.strip():
        raise ValueError('Decision, actor and justification are required')
    if len(actor) > 200 or len(reason) > 4000:
        raise ValueError('Actor or justification too long')
    raw = report_path.read_bytes()
    report = json.loads(raw)
    if report.get('status') not in ('ALLOW', 'REVIEW', 'BLOCK'):
        raise ValueError('Invalid automated status')
    if report.get('human_decision') != 'PENDING':
        raise ValueError('Use the original pending report')
    if decision == 'APPROVE' and report['status'] != 'ALLOW':
        raise ValueError('Approval requires ALLOW; unresolved REVIEW/BLOCK cannot be overridden')
    stamp = datetime.now(timezone.utc)
    digest = hashlib.sha256(raw).hexdigest()
    event = {'created_utc': stamp.isoformat(), 'report_sha256': digest,
             'automated_status': report['status'], 'mode': report['mode'],
             'decision': decision, 'actor': actor.strip(), 'reason': reason.strip(),
             'identity': 'self-declared; not authenticated',
             'effect': 'local review record only; no payment or external action'}
    parent = report_path.parent / 'decisions'
    parent.mkdir(exist_ok=True)
    folder = parent / (stamp.strftime('%Y%m%dT%H%M%S%fZ') + '-' + digest[:12])
    folder.mkdir(exist_ok=False)
    (folder / 'source-report.json').write_bytes(raw)
    (folder / 'decision.json').write_text(json.dumps(event, indent=2) + '\n', encoding='utf-8')
    combined = dict(report, human_decision=decision, human_record=event)
    (folder / 'report.html').write_text(render([combined]), encoding='utf-8')
    return folder


def verify(folder):
    raw = (folder / 'source-report.json').read_bytes()
    event = json.loads((folder / 'decision.json').read_text())
    source = json.loads(raw)
    if hashlib.sha256(raw).hexdigest() != event['report_sha256']:
        raise ValueError('Report hash mismatch')
    if event['automated_status'] != source['status'] or event['mode'] != source['mode']:
        raise ValueError('Decision metadata does not match source')
    if event['decision'] not in DECISIONS or not event['actor'].strip() or not event['reason'].strip():
        raise ValueError('Invalid decision record')
    if event['decision'] == 'APPROVE' and source['status'] != 'ALLOW':
        raise ValueError('Approval of unresolved dossier is prohibited')
    return event


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    save = commands.add_parser('record')
    save.add_argument('report', type=Path)
    save.add_argument('--decision', required=True, choices=DECISIONS)
    save.add_argument('--actor', required=True)
    save.add_argument('--reason', required=True)
    check = commands.add_parser('verify')
    check.add_argument('folder', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'record':
            folder = record(args.report, args.decision, args.actor, args.reason)
            print('Decision saved:', folder)
            print('Report:', folder / 'report.html')
        else:
            event = verify(args.folder)
            print('Snapshot matches record:', event['decision'])
            print('This verifies local consistency, not identity or authenticity.')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, 'Decision failed: ' + str(exc) + '\n')


if __name__ == '__main__':
    main()
