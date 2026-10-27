# MTech Semester I - Learning Portal

A syllabus-faithful educational website covering five MTech Semester I courses. Every course directory contains a dedicated webpage, detailed README, concept diagram, worked examples, equations, revision checkpoints, and printable PDF.

## Courses

- [MCSC-105 - Discrete Mathematics and Graph Theory](./discrete-mathematics-and-graph-theory/) - 4 credits
- [MCSC-103 - Advanced Computer Networks and Communication](./advanced-computer-networks-and-communication/) - 4 credits
- [MCSC-202 - Probability and Statistics](./probability-and-statistics/) - 3 credits
- [MCSC-106 - Pattern Recognition](./pattern-recognition/) - 3 credits
- [MCSC-201 - Research Methodology](./research-methodology/) - 3 credits

## Run locally

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`. A web server is required because the pages load the shared course data with `fetch`.

## Repository structure

```text
.
├── index.html
├── assets/
├── discrete-mathematics-and-graph-theory/
├── advanced-computer-networks-and-communication/
├── probability-and-statistics/
├── pattern-recognition/
└── research-methodology/
```

## Validation

Run `python3 scripts/validate.py`. It checks course counts, required files, internal links, PDF page counts, and README topic coverage.

## Academic scope

The content is derived from the supplied syllabus. It deliberately avoids invented unit numbering, assessment schemes, learning outcomes, or institutional rules. Examples are instructional illustrations, not additional syllabus requirements.

## License

Educational content and source code are available under the MIT License unless a referenced asset states otherwise.
