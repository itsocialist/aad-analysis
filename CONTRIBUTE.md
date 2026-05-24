# Contributing to the AAD Corpus

Thank you for contributing to the AI-Assisted Development corpus. Every submission — whether the project used AI or not — helps build a richer picture of how software gets built today.

---

## Privacy — what gets collected and what doesn't

**What the analysis produces:**
- Commit counts, LOC counts, fix/feat ratios, gap durations — aggregate statistics only
- A short free-text narrative you review before sharing

**What the analysis never collects:**
- Source code
- File paths
- Commit message text
- Real contributor names or email addresses (these are replaced with `contributor-1`, `contributor-2`, etc. automatically)

**One thing to check before you run:** scan your git history for accidentally committed secrets.

```bash
git log --all -S "password\|secret\|token\|apikey" --oneline | head -20
```

If anything appears, address it before running the analysis. The analysis tool does not read `.env` or credential files, but it reads git history — if a secret was committed, it is in that history.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) (free tier works)
- A git repository (any language, any age)

## Step-by-step guide

### Step 1 — Run AAD_ANALYZE_PROMPT.md in your project root

Open a Claude Code session at the root of your git repository and paste the full contents of [AAD_ANALYZE_PROMPT.md](./AAD_ANALYZE_PROMPT.md).

Claude will analyze your commit history and produce several output files under `.archive/evolution-report/`.

### Step 2 — Locate your contribution file

The analysis produces `.archive/evolution-report/evolution-meta.json`. That is your contribution file. It contains aggregate metrics only — no source code, no file paths, no commit messages, no contributor identities.

Example output:
```json
{
  "project_name": "my-project",
  "primary_language": "Python",
  "framework": "FastAPI",
  "ai_assisted": "yes",
  "total_commits": 87,
  "date_range_days": 21,
  ...
}
```

### Step 3 — Review and anonymize before sharing

Open `evolution-meta.json` and review these two fields before submitting:

- **`project_name`** — use a generic name or codename if you prefer not to identify the project (e.g. `"python-api-service-2026"`, `"ts-webapp-internal"`). The numeric fields matter more than the name.
- **`max_gap_context`** — this is the only free-text field. Keep it generic: "break between sprints" rather than referencing team members, clients, or internal system names.

Everything else is a number. Contributor emails were replaced with handles automatically in Step 1. Commit message text was never stored.

### Step 4 — Validate

Run the validator to confirm your file matches the schema:

```bash
python3 schema/validate.py path/to/evolution-meta.json
```

On success you will see a one-line summary. On failure, each error is labeled with the field that failed.

If you don't have the repo cloned yet:
```bash
git clone https://github.com/itsocialist/aad-analysis.git
cd aad-analysis
python3 schema/validate.py /path/to/your/evolution-meta.json
```

### Step 5 — Add contributor fields

Open your `evolution-meta.json` and add two fields:

```json
{
  ...
  "contributor": "your-github-handle",
  "submitted_date": "2026-05-24"
}
```

`contributor` is your GitHub username. `submitted_date` is today in ISO 8601 format (YYYY-MM-DD).

### Step 6 — Copy to corpus/projects/

Choose a filename that matches your project name (lowercase, hyphens for spaces):

```bash
cp path/to/evolution-meta.json corpus/projects/your-project-name.json
```

### Step 7 — Open a pull request

1. Fork the repo on GitHub
2. Create a branch: `git checkout -b corpus/your-project-name`
3. Commit: `git add corpus/projects/your-project-name.json && git commit -m "corpus: add your-project-name"`
4. Push and open a PR titled **"corpus: add [project-name]"**

We review all submissions within a few days.

---

## Privacy summary

| What | Collected? |
|------|-----------|
| Source code | No |
| File paths | No |
| Commit message text | No |
| Contributor names / emails | No — replaced with contributor-1, contributor-2, etc. |
| Commit counts, LOC, ratios | Yes — these are the corpus signals |
| `max_gap_context` | Yes — free text you write and review before submitting |

If you have any doubt about what's in your `evolution-meta.json` before submitting, open it and read it. It's a small JSON file. Everything in it should be something you're comfortable making public.

---

## What makes a good contribution?

Any git repository qualifies. Good corpus data comes from:

| Signal | Why it helps |
|--------|-------------|
| Projects where you used AI heavily | Core corpus signal |
| Projects where you used no AI | Baseline comparison |
| Projects with >30 commits | More meaningful velocity metrics |
| Projects spanning >7 days | Captures gap patterns |
| Mixed-language projects | Language diversity |
| Projects that shipped | Survivorship data |
| Projects that were abandoned | Anti-survivorship data |

The `ai_assisted` field (`yes` / `partial` / `unknown` / `no`) lets the corpus cover the full spectrum. A "no AI" project from 2023 is just as valuable as a vibe-coded weekend sprint from 2026.

---

## Questions?

Open a GitHub issue or start a discussion. We're happy to help you generate your first contribution.
