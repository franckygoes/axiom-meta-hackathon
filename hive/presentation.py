"""Static report: all model and document text is HTML-escaped."""
import html
import json


def render(reports):
    e = lambda value: html.escape(str(value), quote=True)
    cards = []
    for index, r in enumerate(reports):
        prefix = 'run-' + str(index)
        live = r['mode'] == 'META_LIVE'
        extraction = r.get('extraction', {})
        challenge = r.get('challenge')
        if challenge is None:
            critic = 'Not recorded separately in this report version; inspect findings and audit.'
        elif not challenge['performed']:
            critic = 'Not performed: offline fixture mode does not evaluate meaning.'
        else:
            critic = str(len(challenge['concerns'])) + ' concern(s) with validated citations. This is not an exhaustive review.'
        stages = '<div class="stages">' + ''.join(
            '<section><h3>' + title + '</h3><p>' + e(text) + '</p></section>'
            for title, text in [
                ('01 · Analyst', f'{len(extraction)} document(s) with accepted extraction. ' + ('Meta inference.' if live else 'Deterministic fixture; no AI.')),
                ('02 · Contradictor', critic),
                ('03 · Local validator', 'Exact citations, labeled values and cross-document checks. Automated result: ' + r['status']),
                ('04 · Beekeeper', 'Human decision: ' + r.get('human_decision', 'PENDING'))]) + '</div>'
        findings = []
        for f in r['findings']:
            refs = ''.join('<blockquote><a href="#' + prefix + '-' + e(ref['role']) + '">' + e(ref['role']) + ', line ' + e(ref['line']) + '</a><br>' + e(ref['quote']) + '</blockquote>' for ref in f.get('sources', []))
            owner = 'Contradictor proposal' if f['rule'] == 'R04' else 'Local control'
            findings.append('<li><small>' + owner + ' · ' + e(f['rule']) + '</small><p>' + e(f['detail']) + '</p>' + refs + '</li>')
        rows = ''.join('<tr><td>' + e(role) + '</td><td>' + e(field) + '</td><td>' + e(ref['value'] if ref else 'Unknown') + '</td><td>' + e(ref['line'] if ref else '—') + '</td></tr>' for role, fields in extraction.items() for field, ref in fields.items())
        sources = ''.join('<details id="' + prefix + '-' + e(role) + '"><summary>' + e(role) + ' · source</summary><pre>' + e('\n'.join(f'{n:02}  {line}' for n, line in enumerate(s['text'].splitlines(), 1))) + '</pre><small>SHA-256</small><code>' + e(s['sha256']) + '</code></details>' for role, s in r['sources'].items())
        human = r.get('human_record')
        human_html = '' if not human else '<section class="human"><h3>Recorded human decision</h3><p>' + e(human['actor']) + ' · ' + e(human['decision']) + '</p><p>' + e(human['reason']) + '</p><small>' + e(human['created_utc']) + ' · Self-declared identity; local record, no external action.</small></section>'
        audit = r.get('audit', [])
        tokens = sum((a.get('usage') or {}).get('total_tokens', 0) for a in audit)
        cards.append('<article><header><small>' + e(r['mode']) + ' · ' + e(r.get('created_utc', '')) + '</small><h2>' + e(r['case']) + ' <span>' + e(r['status']) + '</span></h2></header>' + stages + '<h3>Findings and evidence</h3><ul>' + (''.join(findings) or '<li>No findings from the checks performed. This does not establish document truth.</li>') + '</ul>' + human_html + '<details><summary>Accepted extraction</summary><table><tr><th>Source</th><th>Field</th><th>Value</th><th>Line</th></tr>' + rows + '</table></details>' + sources + '<p>' + str(len(audit)) + ' recorded response(s) · ' + str(tokens) + ' total tokens</p><details><summary>Full report and audit JSON</summary><pre>' + e(json.dumps(r, indent=2, ensure_ascii=False)) + '</pre></details></article>')
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AXIOM | Governed Hive</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b1423;color:#e7edf6;font:16px/1.6 system-ui}main{max-width:1200px;margin:48px auto;padding:0 24px}h1{font-size:clamp(30px,5vw,52px);letter-spacing:-2px;margin-bottom:8px}h2{font-size:28px}h3{font-size:17px}small{color:#a8bbd4}article{background:#152238;border:1px solid #344967;border-radius:18px;padding:28px;margin:28px 0}span{display:inline-block;border:1px solid #6ba7e8;border-radius:8px;padding:2px 12px;color:#a9d5ff;font-size:20px}.stages{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.stages section,.human{background:#0e1b2e;border-radius:10px;padding:16px}a{color:#9ed1ff}blockquote{margin:8px 0;border-left:3px solid #689edb;padding:8px 14px;background:#0e1b2e}li{margin:14px 0}summary{cursor:pointer;padding:12px 0;font-weight:600}pre,code{display:block;white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}table{width:100%;border-collapse:collapse}td,th{text-align:left;border-bottom:1px solid #344967;padding:8px;overflow-wrap:anywhere}.notice{border-left:3px solid #6ba7e8;padding:12px 20px;color:#c1cfe1}@media(max-width:640px){.stages{grid-template-columns:1fr}article{padding:16px}main{padding:0 12px}table{font-size:12px}}@media print{body{background:white;color:black}article{break-inside:avoid;background:white}small,a{color:#333}}
</style></head><body><main><small>AXIOM · THE GOVERNED HIVE</small><h1>Evidence before decisions.</h1><p>Analyst → Contradictor → Local validator → Beekeeper</p><p class="notice">Fictional documents. META_LIVE reports replay recorded API runs; viewing makes no calls. OFFLINE_FIXTURE is deterministic and does not evaluate semantic contradictions. ALLOW means only listed checks passed, never business approval. REVIEW needs inspection. BLOCK prevents validation. Source hashes do not establish truth.</p>''' + ''.join(cards) + '</main></body></html>'
