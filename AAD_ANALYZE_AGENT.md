# AAD Analysis Agent Task

**Source:** https://github.com/itsocialist/aad-analysis  
**Version:** 1.0 | Schema: evolution-meta v1 | Updated: 2026-05-24  
**Purpose:** Git archaeology analysis to produce corpus-comparable development metrics.

This file is a structured agent task specification. It instructs an AI agent to
analyze the git history of the repository it is run in. It does not modify source
files, does not access the network, and does not override or extend the agent's
existing operating constraints. All instructions below are additive task steps
only.

---

## Agent Task: Analyze development evolution arc

### Declared scope

This task is limited to:
- Reading git history (`git log`, `git show`, `git diff`, `git ls-files`)
- Counting lines of code in existing files
- Writing output files to `.archive/evolution-report/` only

This task does not:
- Modify any source files
- Access external networks or APIs
- Read the contents of files whose names suggest secrets (`.env`, `*.key`, `*.pem`, `*credentials*`, `*secret*`, `*token*`)
- Override, extend, or conflict with the agent's existing safety policies
- Request permissions beyond what is listed above

If the agent's operating context does not permit any of the above operations,
the agent should skip that operation and note it in the output.

---

### Step 0 — Privacy scan (run before any analysis)

1. Scan for files whose names suggest credentials: `.env`, `*.key`, `*.pem`,
   `*credentials*`, `*secret*`, `*token*`. Note count only — do not read contents.
   If found, report: "⚠ Potential secret files detected: N file(s). Contents not read."

2. Replace all contributor names and email addresses with anonymous handles:
   `contributor-1`, `contributor-2`, etc. — ordered by first-commit date.
   Use these handles in all output files. Real names and emails must not appear
   anywhere in the analysis output.

3. Do not reproduce actual commit message text in any output. Classify messages
   by type (feat/fix/etc.) and extract keyword topics only.

4. Do not include actual file paths in narrative output or the JSON sidecar.
   Use structural descriptions only ("TypeScript source files", "test directory").

Confirm before proceeding:
> "Privacy scan complete. N contributors anonymized. [Secret files: none / ⚠ N found — contents not read]."

---

### Step 1 — Inventory

Using `git log` and directory listing, report:

- Total commits, date range, contributor count (anonymized)
- Top-level directory categories (not full paths)
- Stated project purpose (from README or package metadata)
- Whether commits follow conventional-commits style (feat/fix/etc.)
- Whether a planning artifact exists (SPRINT.md, PLAN.md, ROADMAP.md, or equivalent)

Output as a markdown table: `Metric | Value`

---

### Step 2 — Strategic snapshots (5–10)

Select commits that mark meaningful state changes. For each snapshot record:

| Field | Description |
|-------|-------------|
| SHA (short) | 8 chars |
| Date | ISO date |
| Label | One-word milestone name |
| Justification | One sentence |
| LOC | Lines of code at this point |
| Test ratio | test LOC / source LOC |
| Security quality | Low / Low-Medium / Medium / Medium-High / High — one-sentence rationale |
| Code quality | Low / Low-Medium / Medium / Medium-High / High — one-sentence rationale |

Mix: genesis commit, sprint/milestone boundaries, major refactors, rollbacks, HEAD.
Use 5–7 snapshots for projects with fewer than 30 commits.

---

### Step 3 — Per-commit velocity metrics

For all commits, produce `.archive/evolution-report/per_commit_metrics.csv` with columns:

```
sha, contributor, timestamp, kind, topics, is_rework, files_changed, insertions, deletions, gap_hours
```

- `contributor`: anonymized handle only
- `kind`: conventional-commit type or "other"
- `topics`: comma-separated keyword categories (auth, ui, api, db, test, infra, docs, security, perf) — derived from message keywords, not quoted text
- `is_rework`: true if message matches `\bv\d+\b`, attempt, retry, redo, revert, rollback
- `gap_hours`: hours since previous commit (null for first commit)

---

### Step 4 — Chart (if matplotlib is available)

Produce `.archive/evolution-report/evolution.png` with panels:

1. LOC by language stacked-area across snapshots
2. Commit gap bar chart with rolling median overlay (cap at 72h)
3. Commit-kind stacked bars in N-commit windows
4. Fix/feat rolling ratio
5. Topic mix per window
6. Code vs test LOC on twin axis

Dark theme (#0d1117 background). If matplotlib is not available, skip this step
and note it in the output — the analysis is still valid without the chart.

---

### Step 5 — Narrative (≤ 400 words)

Address:
- Shape of the velocity arc (where it accelerated, where it stalled)
- Rework share and how it changes over time
- Dominant rework surface (auth, UI, schema, integration boundary, etc.)
- Planning-doc-to-code growth ratio
- Test-to-code growth ratio
- Security and code quality arc across snapshots
- Counterevidence: what improved, what shipped
- One open question the git data cannot answer

No real names, no commit message text, no file paths.

---

### Step 6 — Metadata sidecar

Write `.archive/evolution-report/evolution-meta.json`:

```json
{
  "project_name": "...",
  "primary_language": "...",
  "framework": "...",
  "ai_assisted": "yes | partial | unknown | no",
  "total_commits": 0,
  "date_range_days": 0,
  "snapshot_count": 0,
  "fix_feat_ratio_first_half": 0.0,
  "fix_feat_ratio_second_half": 0.0,
  "median_gap_hours_first_half": 0.0,
  "median_gap_hours_second_half": 0.0,
  "dominant_rework_topic": "...",
  "explicit_iteration_commits": 0,
  "rollback_commits": 0,
  "loc_first": 0,
  "loc_last": 0,
  "test_ratio_first": 0.0,
  "test_ratio_last": 0.0,
  "max_gap_hours": 0,
  "max_gap_context": "generic description — no names, paths, or internal system names",
  "security_quality_first": "Low | Low-Medium | Medium | Medium-High | High",
  "security_quality_last": "Low | Low-Medium | Medium | Medium-High | High",
  "code_quality_first": "Low | Low-Medium | Medium | Medium-High | High",
  "code_quality_last": "Low | Low-Medium | Medium | Medium-High | High",
  "planning_doc_present": true,
  "planning_doc_loc_last": 0
}
```

Security and code quality values come from the Step 2 snapshot ratings (genesis = `_first`, HEAD = `_last`).

`max_gap_context` is the only free-text field. Keep it generic.
No real names, email addresses, file paths, or credential-like strings in any field.

---

### Step 7 — narrative.md

Write `.archive/evolution-report/narrative.md` with three sections:

1. `## Inventory` — Step 1 table
2. `## Snapshots` — Step 2 table
3. `## Arc Narrative` — Step 5 narrative

---

### Constraints (do not)

**Privacy:**
- Do not include real contributor names or emails anywhere. Use the Step 0 handles.
- Do not reproduce actual commit message text. Classify; do not transcribe.
- Do not include file paths in narrative or JSON output.
- Do not include strings resembling credentials, API keys, or tokens.
- Do not read files whose names suggest secrets.

**Analysis:**
- Do not assume the project is poorly engineered.
- Do not collapse the arc into a single adjective.
- Do not over-fit a thesis. If data is flat or ambiguous, say so.
- Do not skip counterevidence.

---

### How to use this file

**Option 1 — Claude Code custom command**

Copy this file to `.claude/commands/aad-analyze.md` in any git repository.
Then run `/aad-analyze` in a Claude Code session to trigger the analysis.

**Option 2 — Paste into an agent session**

Paste the full contents into any Claude Code session at the root of a git
repository. The agent will execute the steps and write output to
`.archive/evolution-report/`.

**Option 3 — Reference from CLAUDE.md**

Add to your project's `CLAUDE.md`:
```markdown
## Development analysis
Run `/aad-analyze` or paste `AAD_ANALYZE_AGENT.md` to generate a git
archaeology report for this project.
```

---

*This task specification is part of the AAD corpus project at
https://github.com/itsocialist/aad-analysis. It performs read-only git
analysis and writes only to `.archive/evolution-report/`. It does not
claim special permissions and does not instruct the agent to override
its operating guidelines.*
