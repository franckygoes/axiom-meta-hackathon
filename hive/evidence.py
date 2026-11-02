"""Collect existing local reports without importing an API client or making calls."""
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from .review import render

RUNS = (
    ('meta-first', 'contradictory'),
    ('meta-coherent', 'coherent'),
    ('meta-incomplete', 'incomplete'),
    ('meta-incomplete-diagnostic', 'incomplete'),
)


def collect(root):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    destination = root / 'outputs' / 'evidence' / stamp
    records, reports, files, missing = [], [], {}, []
    for folder, case in RUNS:
        path = root / 'outputs' / folder / (case + '.json')
        if not path.is_file():
            missing.append(str(path.relative_to(root)))
            continue
        raw = path.read_bytes()
        report = json.loads(raw)
        if report.get('case') != case or report.get('mode') != 'META_LIVE':
            raise ValueError(f'Unexpected case or mode in {path}')
        if report.get('meta_called') is not True:
            raise ValueError(f'No recorded Meta call in {path}')
        if report.get('status') not in ('ALLOW', 'REVIEW', 'BLOCK'):
            raise ValueError(f'Invalid status in {path}')
        audit = report.get('audit')
        if not isinstance(audit, list) or not audit:
            raise ValueError(f'No response audit in {path}')
        tokens_in = sum(a['usage']['input_tokens'] for a in audit)
        tokens_out = sum(a['usage']['output_tokens'] for a in audit)
        records.append({'run': folder, 'case': case, 'status': report['status'],
                        'report_created_utc': report.get('created_utc'),
                        'sha256': hashlib.sha256(raw).hexdigest(),
                        'responses': len(audit), 'input_tokens': tokens_in,
                        'output_tokens': tokens_out,
                        'response_statuses': [a.get('status') for a in audit]})
        files[folder + '/' + case + '.json'] = raw
        page = path.with_name('report.html')
        if page.is_file():
            files[folder + '/report.html'] = page.read_bytes()
        display = dict(report, case=folder + ' / ' + case)
        reports.append(display)
    if not records:
        raise ValueError('No existing live reports found. No API calls were made.')
    manifest = {'collected_utc': stamp, 'complete': not missing,
                'note': 'Local report archive, not independent provider attestation. '
                        'Hashes detect later changes relative to this manifest, not authenticity. '
                        'Collection creates no API calls. Repeated trials are retained.',
                'runs': records, 'missing': missing}
    files['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    files['report.html'] = render(reports).encode()
    destination.mkdir(parents=True, exist_ok=False)
    for name, raw in files.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    archive = destination.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, raw in files.items():
            bundle.writestr(name, raw)
    return destination, archive, manifest


def main():
    root = Path(__file__).resolve().parent.parent
    try:
        destination, archive, manifest = collect(root)
    except (ValueError, KeyError, TypeError, OSError) as exc:
        raise SystemExit('Collection failed: ' + str(exc))
    for run in manifest['runs']:
        print(f"{run['run']}: {run['status']} | {run['responses']} responses | "
              f"{run['input_tokens']} input / {run['output_tokens']} output tokens")
    print('Complete archive:', manifest['complete'])
    for missing in manifest['missing']:
        print('Missing:', missing)
    print('Report:', destination / 'report.html')
    print('ZIP:', archive)
    print('No API calls. Archive contains only the listed reports and manifest.')


if __name__ == '__main__':
    main()
