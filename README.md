# AAD Corpus — AI-Assisted Development Patterns

A community corpus of AI-assisted development patterns, collected via git archaeology and contributed by the community.

The corpus captures *how* software gets built — not just the end state. Each project contributes aggregate metrics: commit velocity, fix/feat ratios, test coverage trajectories, gap patterns, and LOC growth arcs.

**What the analysis collects:** counts, ratios, and durations — nothing else.  
**What it never collects:** source code, file paths, commit message text, or contributor identities (emails are replaced with anonymous handles automatically).

---

## Quick Start

Run [AAD_ANALYZE_PROMPT.md](./AAD_ANALYZE_PROMPT.md) in any git repo with Claude Code to generate your `evolution-meta.json`:

1. **Check your history first:** `git log --all -S "password\|token\|secret" --oneline | head -20` — address anything that appears
2. Open Claude Code at the root of any git repository
3. Paste the full contents of `AAD_ANALYZE_PROMPT.md`
4. Claude analyzes your commit history and writes `.archive/evolution-report/evolution-meta.json`

That JSON file is your contribution. It contains aggregate statistics only — no code, paths, messages, or identities.

---

## How to Contribute

**3 steps:**

1. **Analyze** — paste [AAD_ANALYZE_PROMPT.md](./AAD_ANALYZE_PROMPT.md) into a Claude Code session at your repo root
2. **Review** — open `.archive/evolution-report/evolution-meta.json` and confirm it contains nothing you don't want to share (see [CONTRIBUTE.md](./CONTRIBUTE.md#privacy-summary))
3. **Submit** — validate with `python3 schema/validate.py .archive/evolution-report/evolution-meta.json`, copy to `corpus/projects/your-project-name.json`, open a PR

Full details in [CONTRIBUTE.md](./CONTRIBUTE.md).

---

## What's in the Corpus

**11 seed projects** across 6 languages, all contributed by the same author to establish the baseline corpus. All project names are anonymized codenames.

| Project | Language | Commits | Category |
|---------|----------|---------|----------|
| Booth | TypeScript | 83 | weekend-sprint |
| Coach | TypeScript | 416 | sustained |
| Buzzer | JavaScript/JSX | 109 | sustained |
| Orchestra | TypeScript | 2 | multi-week |
| Pipeline | JavaScript | 315 | sustained |
| Bastion | YAML/Shell/XML | 88 | sustained |
| Prism | TypeScript | 254 | multi-week |
| Forge | TypeScript | 293 | sustained |
| Helm | TypeScript | 158 | multi-week |
| Warden | YAML/Shell | 132 | weekend-sprint |
| Harvest | Python | 50 | multi-week |

See [corpus/README.md](./corpus/README.md) for the full summary table with LOC, test ratios, and fix/feat ratios.

---

## Explore the Data

**[View the interactive dashboard](./docs/index.html)** — open in any browser, no server required.

The dashboard shows:
- Project scale vs. duration (bubble chart)
- Fix/feat ratios by project
- Test coverage trajectories
- Commit gap patterns
- First-half vs. second-half rework comparison
- Sortable full data table

---

## Repository Layout

```
aad-analysis/
├── README.md                    # This file
├── AAD_ANALYZE_PROMPT.md        # Paste into Claude Code to analyze your repo
├── CONTRIBUTE.md                # How to submit a contribution
├── schema/
│   ├── evolution-meta.schema.json   # JSON Schema draft-07
│   └── validate.py                  # CLI validator (auto-installs jsonschema)
├── scripts/
│   └── collect_metrics.py       # Deterministic git metrics extractor (optional)
├── corpus/
│   ├── README.md                # Summary table + stats
│   └── projects/                # One JSON per project
│       └── *.json
└── docs/
    └── index.html               # Self-contained single-file dashboard
```

---

## Schema

All corpus files conform to [schema/evolution-meta.schema.json](./schema/evolution-meta.schema.json) (JSON Schema draft-07).

Required fields include: `project_name`, `primary_language`, `framework`, `ai_assisted` (yes/partial/unknown/no), `total_commits`, `date_range_days`, `fix_feat_ratio_first_half`, `fix_feat_ratio_second_half`, `loc_first`, `loc_last`, `test_ratio_first`, `test_ratio_last`, `max_gap_hours`, and more.

Optional fields for contributors: `contributor` (handle), `submitted_date`, `category`, `notes`.

---

## License

MIT — see [LICENSE](./LICENSE) if present, otherwise: free to use, share, and build on with attribution.

Corpus data is contributed under the same license. Project names that have been anonymized should remain anonymized in any derivative work.
