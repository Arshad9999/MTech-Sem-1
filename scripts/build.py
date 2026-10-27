import json, re, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'assets/course-data.json').read_text())['courses']

def readme(c):
    credit_value=str(c['credits']) if isinstance(c['credits'],int) else "Not stated in the supplied syllabus"
    lines=[f"# {c['code']} - {c['title']}","",f"**Credits:** {credit_value}","",c['tagline'],"","> This guide expands only the topics named in the supplied syllabus. Confirm assessment rules and recommended readings with your institution.","","## Course map",""]
    for i,m in enumerate(c['modules'],1): lines.append(f"{i}. **{m['title']}** - "+", ".join(m['topics']))
    lines += ["","## Learning notes",""]
    for i,m in enumerate(c['modules'],1):
        lines += [f"### {i}. {m['title']}","",f"**Syllabus topics:** {', '.join(m['topics'])}","",m['definition'],"",f"**Key equation or relation:** `{m['equation']}`","",f"**Worked example:** {m['example']}","",f"**Must understand:** {m['checkpoint']}",""]
    lines += ["## Files","",f"- [Interactive course page](./index.html)",f"- [Detailed PDF handbook](./{c['code']}-{c['slug']}.pdf)","- [Semester home](../index.html)","","## Study method","","1. Define the terms without notes.","2. Reproduce the equation and state its assumptions.","3. Solve or trace the worked example.","4. Explain when the method should not be used.","","## Scope and accuracy","","This resource is based on the syllabus supplied for this repository. Explanations and examples clarify listed topics; they do not add official units, assessment weights, or institutional policies.",""]
    return "\n".join(lines)

html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="MTech Semester I course guide"><title>Course guide</title><link rel="stylesheet" href="../assets/styles.css"><link rel="stylesheet" href="../assets/mastery.css"></head><body data-page="course" data-depth="../" data-course="{slug}"><a class="skip" href="#main">Skip to content</a><div id="nav"></div><main id="main"><section class="course-hero shell" id="courseHero"></section><div class="content-layout shell"><aside class="toc" id="toc" aria-label="Course contents"></aside><article id="modules"></article></div></main><div id="foot"></div><script src="../assets/app.js?v=20261027-4"></script></body></html>'''
for c in DATA:
    p=ROOT/c['slug'];p.mkdir(exist_ok=True)
    (p/'README.md').write_text(readme(c))
    (p/'index.html').write_text(html.format(slug=c['slug']))

root=["# MTech Semester I - Learning Portal","","A syllabus-faithful educational website covering five MTech Semester I courses. Every course directory contains a dedicated webpage, detailed README, concept diagram, worked examples, equations, revision checkpoints, and printable PDF.","","## Deep-learning features","","Each course webpage includes eight mastery sections: learning objectives, an expandable glossary, syllabus-relevant type classifications, a formula and relationship sheet, comparison tables, common mistakes, practice questions with progressive hints, and applied exercises.","","## Courses",""]
for c in DATA:
    credit_label=f"{c['credits']} credits" if isinstance(c['credits'],int) else "credit not stated"
    root.append(f"- [{c['code']} - {c['title']}](./{c['slug']}/) - {credit_label}")
root += ["","## Run locally","","```bash","python3 -m http.server 8000","```","","Open `http://localhost:8000`. A web server is required because the pages load the shared course data with `fetch`.","","## Repository structure","","```text",".","├── index.html","├── assets/","├── discrete-mathematics-and-graph-theory/","├── advanced-computer-networks-and-communication/","├── probability-and-statistics/","├── pattern-recognition/","└── research-methodology/","```","","## Validation","","Run `python3 scripts/validate.py`. It checks course counts, required files, internal links, PDF page counts, and README topic coverage.","","## Academic scope","","The content is derived from the supplied syllabus. It deliberately avoids invented unit numbering, assessment schemes, learning outcomes, or institutional rules. Examples are instructional illustrations, not additional syllabus requirements.","","## License","","Educational content and source code are available under the MIT License unless a referenced asset states otherwise.",""]
(ROOT/'README.md').write_text("\n".join(root))
