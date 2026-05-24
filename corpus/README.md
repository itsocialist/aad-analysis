# AAD Corpus

**11 projects** | 6 languages | Median commits: 132 | Median final test ratio: 2.0% | 10/11 AI-assisted

This directory contains one JSON file per project. Each file conforms to the [evolution-meta schema](../schema/evolution-meta.schema.json) and was validated with [schema/validate.py](../schema/validate.py).

---

## Projects

| Project | Language | Category | Commits | LOC (start→end) | Test Ratio (final) | Fix/Feat (2nd half) | AI-Assisted |
|---------|----------|----------|---------|-----------------|-------------------|---------------------|-------------|
| Booth | TypeScript | weekend-sprint | 83 | 5,475 → 18,656 | 13.5% | 0.55 | yes |
| Coach | TypeScript | sustained | 416 | 3,550 → 41,029 | 4.9% | 1.69 | yes |
| Buzzer | JavaScript/JSX | sustained | 109 | 3,600 → 9,763 | 2.5% | 0.55 | yes |
| Orchestra | TypeScript | multi-week | 2 | 21,050 → 21,050 | 55.0% | 0.00 | yes |
| Pipeline | JavaScript | sustained | 315 | 0 → 42,398 | 4.5% | 0.51 | yes |
| Bastion | YAML/Shell/XML | sustained | 88 | 462,301 → 474,595 | 1.1% | 1.00 | yes |
| Prism | TypeScript | multi-week | 254 | 2,750 → 50,687 | 1.2% | 0.51 | yes |
| Forge | TypeScript | sustained | 293 | 0 → 44,947 | 1.4% | 0.85 | yes |
| Helm | TypeScript | multi-week | 158 | 0 → 24,835 | 2.0% | 0.85 | yes |
| Warden | YAML/Shell | weekend-sprint | 132 | 6,860 → 18,500 | 2.0% | 0.60 | partial |
| Harvest | Python | multi-week | 50 | 3,695 → 6,836 | 25.2% | 0.30 | yes |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total projects | 11 |
| Languages represented | TypeScript, JavaScript/JSX, Python, YAML/Shell, YAML/Shell/XML |
| AI-assisted (yes) | 10/11 (91%) |
| AI-assisted (partial) | 1/11 (9%) |
| Median commits | 132 |
| Median date range | 53 days |
| Median final LOC | 24,835 |
| Median final test ratio | 2.0% |
| Median fix/feat ratio (2nd half) | 0.60 |
| Median max gap | 705 hours |
| Categories | weekend-sprint: 2, multi-week: 4, sustained: 5 |

**Note:** All project names in this corpus are anonymized codenames. The private mapping is not committed to this repository.

---

## Schema

All files are validated against [../schema/evolution-meta.schema.json](../schema/evolution-meta.schema.json) (JSON Schema draft-07).

To validate a single file:
```bash
python3 ../schema/validate.py projects/muster.json
```

To validate all files:
```bash
python3 ../schema/validate.py --all projects/
```
