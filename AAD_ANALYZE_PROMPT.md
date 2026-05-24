# Reusable prompt — codebase-evolution snapshot collection

Version: 1.1 | Schema: evolution-meta v1 | Updated: 2026-05-24

---

> ### ⚠ PRIVACY CHECK — DO THIS BEFORE PASTING THE PROMPT
>
> This prompt reads your git history. Take 30 seconds first:
>
> 1. **Secrets in history?** Run: `git log --all -S "password\|secret\|token\|apikey\|api_key" --oneline | head -20`  
>    If anything appears, resolve it before running this analysis.
> 2. **OK to share aggregate statistics?** The output contains commit counts, LOC counts, and ratios — no code, no messages, no paths.
> 3. **Contributor emails are auto-anonymized.** Real names and emails never appear in any output file.
>
> If you are unsure about any of the above, read [CONTRIBUTE.md](./CONTRIBUTE.md#privacy) before proceeding.

---

Paste the block below into a fresh Claude Code session at the root of any
git repository to produce a comparable snapshot dataset and chart.
Each run emits an `evolution.png` and two CSVs (per-commit + snapshot
metrics) so results from multiple projects can be cross-compared.

The goal is to build a corpus of AI-assisted development arcs — not to
prove a single thesis. Different projects will show different shapes.
Surface what's there.

---

## PROMPT

You are analyzing a codebase to capture its development-evolution arc.
This is part of a multi-project study on AI-assisted / vibe-coded
development patterns. Follow the facts; do not force a narrative.

### Step 0 — Privacy and safety scan

**Run this step before any other analysis. Do not skip it.**

1. **Secret detection:** Check for any files whose names suggest they
   contain credentials: `.env`, `*.key`, `*.pem`, `*credentials*`,
   `*secret*`, `*token*`. Do NOT read their contents. Do NOT include
   their paths in any output. If any exist, report: "⚠ Potential secret
   files detected: [count] file(s). Skipping contents. Recommend
   reviewing before sharing analysis."

2. **Contributor anonymization:** Replace all real contributor names and
   email addresses with anonymous handles — `contributor-1`,
   `contributor-2`, etc. — ordered by first-commit date. Use these
   handles in every output file, every table, every CSV row. Real names
   and emails must not appear anywhere in the analysis output.

3. **Commit message handling:** Do NOT quote or reproduce actual commit
   message text anywhere in any output. Classify messages by type
   (feat/fix/refactor/etc.) and extract keyword topics, but never
   reproduce the literal text.

4. **File path handling:** Do NOT include actual file paths in narrative
   or summary output. Use structural descriptions only: "TypeScript
   source files", "test directory", "config files", etc. Paths may
   appear internally in CSV columns where they are strictly necessary
   for the analysis (e.g. `files_changed`), but strip them from all
   human-readable narrative and the JSON sidecar.

**Confirm in one line before proceeding:**
> "Privacy scan complete. [N] contributors anonymized as contributor-1
> through contributor-N. [Secret files: none / ⚠ see above]."

---

### Step 1 — Inventory
Report:
- Total commits, date range, number of contributors (use anonymized handles)
- Top-level directory layout (category names only, not full paths)
- Stated purpose (from README / package metadata)
- Whether commit messages follow conventional-commits (feat/fix/etc.)
- Whether there is a SPRINT.md, PLAN.md, ROADMAP.md, or equivalent
  planning artifact

Present as a markdown table with columns: Metric | Value.

### Step 2 — Choose 10 strategic snapshots
Pick commits that capture meaningful state changes, not evenly spaced
time slices. Justify each choice in one sentence. Mix of:
- Genesis (first commit)
- Each declared milestone / sprint boundary / version tag
- Plan pivots (commit messages that change scope or direction)
- Major refactors
- Rollback commits ("revert", "restore known-good", "disable X pending Y")
- Visible iteration runs (v2, v3, attempt #2)
- HEAD

If the project has fewer than ~30 commits, pick 5–7 snapshots instead.

For each snapshot, record:
- SHA, date, label, and one-sentence justification
- File count by extension (.py, .js/.ts/.tsx, .css, .sh, .md, .yml, .json)
- LOC by language
- Test LOC and test/code ratio
- TODO/FIXME/HACK/XXX count
- Planning-doc size (SPRINT.md or equivalent)
- Count of any project-specific dimension worth tracking (agents, MCP
  servers, microservices, dashboards — whatever the architecture exposes)
- **Security quality rating**: Low / Low-Medium / Medium / Medium-High / High
  with one-sentence rationale (key management, secrets hygiene, auth posture)
- **Code quality rating**: Low / Low-Medium / Medium / Medium-High / High
  with one-sentence rationale (structure, test coverage, tech debt signals)

Present as a markdown table: Snapshot | SHA | Date | LOC | Test Ratio |
Security | Code Quality | Notes.

### Step 3 — Per-commit velocity metrics
Across ALL commits (not just snapshots):
- Timestamp + anonymized contributor handle (never real name or email)
- Files changed, insertions, deletions
- Conventional-commit kind (feat/fix/refactor/test/plan/chore/docs/security/other)
- Topic tags derived from message keywords — classify the commit, do not
  quote message text (for a web app this might be auth/ui/api/infra/test/docs)
- Flag explicit iteration markers: regex `\bv\d+\b`, "attempt", "take 2",
  "retry", "redo", "revert", "rollback"
- Gap (hours) since previous commit

Save results to `.archive/evolution-report/per_commit_metrics.csv`.

### Step 4 — Per-commit velocity metrics chart inputs
Compute rolling aggregates for charting:
- Median inter-commit gap (first vs. second half of timeline)
- Fix/feat ratio by N-commit windows (N = max(5, total/10))
- Topic mix per window

### Step 5 — Produce one multi-panel chart with these panels
1. LOC by language stacked-area across snapshots, with snapshot labels
2. Hours-between-commits bar chart with rolling median overlay (cap at 72h)
3. Commit-kind stacked bars in N-commit windows
4. Fix-to-feature rolling ratio (window = max(5, total/10))
5. Topic mix per window
6. Iteration-thrash strip: scatter every commit; highlight commits matching
   the dominant rework topic; flag explicit-version-iteration markers
7. Planning-doc growth across snapshots
8. Code vs test LOC + test/code ratio on twin axis
9. Cumulative commits over wall time, shade gaps >24h

Use a dark theme and a consistent color palette so charts from
different projects are visually comparable. Save as
`.archive/evolution-report/evolution.png` plus the snapshot CSV
`.archive/evolution-report/snapshot_metrics.csv`.

### Step 6 — Narrative (≤ 400 words)
Lead with the SHAPE of the arc, not a verdict. Address explicitly:
- Where did velocity hold? Where did it stall? Wall-clock gaps?
- What share of commits is rework vs new functionality, and how does
  that ratio move over time?
- Which surface or subsystem dominates the rework? (e.g. UI/CSS,
  schema, auth, integration boundary)
- Are there explicit rollback or "restore known-good" commits?
- What's the planning-doc-to-code growth ratio?
- What's the test-to-code growth ratio?
- How did security quality and code quality ratings evolve across snapshots?
- Counterevidence: what improved, what shipped despite the friction?
- One open question the data raises that you can't answer from git alone

Do not quote commit messages. Do not include real names or emails.
Do not include file paths.

### Step 7 — Metadata for cross-project comparison
Emit a small JSON sidecar `.archive/evolution-report/evolution-meta.json`.

**Before writing this file:** ensure no field contains a real name, email
address, file path, or string that resembles a credential. The
`max_gap_context` field is free text — keep it generic (e.g.
"apparent break between sprints" rather than referencing team members
or internal systems by name).

```json
{
  "project_name": "...",
  "primary_language": "...",
  "framework": "...",
  "ai_assisted": "yes | partial | unknown | no",
  "total_commits": N,
  "date_range_days": N,
  "snapshot_count": 10,
  "fix_feat_ratio_first_half": X.XX,
  "fix_feat_ratio_second_half": X.XX,
  "median_gap_hours_first_half": X.XX,
  "median_gap_hours_second_half": X.XX,
  "dominant_rework_topic": "...",
  "explicit_iteration_commits": N,
  "rollback_commits": N,
  "loc_first": N, "loc_last": N,
  "test_ratio_first": X.XX, "test_ratio_last": X.XX,
  "max_gap_hours": N,
  "max_gap_context": "generic description only — no names, paths, or internal systems"
}
```

This JSON is what makes the corpus comparable — aggregate it across
projects to look at distributions, not just single-project shapes.

### Step 8 — Save narrative.md
Combine the outputs of Step 1 (inventory table), Step 2 (snapshot table),
and Step 6 (narrative) into a single file:
`.archive/evolution-report/narrative.md`

The file should have three sections:
1. `## Inventory` — the Step 1 markdown table
2. `## Snapshots` — the Step 2 snapshot table (SHA, date, label, LOC,
   test ratio, security rating, code quality rating, notes)
3. `## Arc Narrative` — the Step 6 narrative (≤ 400 words)

No real names, emails, commit message text, or file paths in this file.

### Step 9 — Do not

**Data safety:**
- **Do not include real contributor names or email addresses anywhere.**
  Use the handles assigned in Step 0.
- **Do not quote or reproduce actual commit message text.** Classify and
  summarize; never transcribe.
- **Do not include actual file paths** in narrative, tables, or the JSON
  sidecar. Use structural descriptions.
- **Do not include any string resembling a credential, token, API key,
  or password.** If one is encountered during analysis, stop and alert
  the user immediately before continuing.
- **Do not read the contents of files whose names suggest secrets**
  (.env, *.key, *.pem, credentials.*, secrets.*). Note their existence
  only.

**Analysis integrity:**
- Do not assume the project is poorly engineered. Many shapes are healthy.
- Do not collapse the arc into a single adjective.
- Do not over-fit a thesis. If the data is flat or ambiguous, say so.
- Do not skip the counterevidence step.
