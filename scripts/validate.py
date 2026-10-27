import json,re,sys
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'assets/course-data.json').read_text())['courses']
errors=[]
if len(data)!=5: errors.append(f'Expected 5 courses, found {len(data)}')
for c in data:
    d=ROOT/c['slug'];required=[d/'index.html',d/'README.md',d/f"{c['code']}-{c['slug']}.pdf",ROOT/'assets'/c['diagram']]
    for p in required:
        if not p.exists() or p.stat().st_size==0: errors.append(f'Missing or empty: {p.relative_to(ROOT)}')
    md=(d/'README.md').read_text() if (d/'README.md').exists() else ''
    for m in c['modules']:
        for topic in m['topics']:
            if topic not in md: errors.append(f"README missing topic '{topic}' in {c['code']}")
    pdf=d/f"{c['code']}-{c['slug']}.pdf"
    if pdf.exists():
        pages=len(PdfReader(str(pdf)).pages)
        if pages < len(c['modules'])+2: errors.append(f'{pdf.name} too short: {pages} pages')
for html in ROOT.rglob('*.html'):
    text=html.read_text()
    for ref in re.findall(r'(?:href|src)="([^"]+)"',text):
        if ref.startswith(('http:','https:','#')): continue
        target=(html.parent/ref.split('#')[0]).resolve()
        if not target.exists(): errors.append(f'Broken link in {html.relative_to(ROOT)}: {ref}')
if errors:
    print('\n'.join('ERROR: '+e for e in errors));sys.exit(1)
print(f'Validated {len(data)} courses, {sum(len(c["modules"]) for c in data)} study blocks, all required files, topic coverage, PDF lengths, and local links.')
