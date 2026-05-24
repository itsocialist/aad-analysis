# Contributing to the AAD Corpus

Thank you for contributing to the AI-Assisted Development corpus. Every submission — whether the project used AI or not — helps build a richer picture of how software gets built today.

## Prerequisites

- [Claude Code](https://claude.ai/code) (free tier works)
- A git repository (any language, any age)

## Step-by-step guide

### Step 1 — Run COLLECT_PROMPT.md in your project root

Open a Claude Code session at the root of your git repository and paste the full contents of [COLLECT_PROMPT.md](./COLLECT_PROMPT.md).

Claude will analyze your commit history and produce several output files under `.archive/evolution-report/`.

### Step 2 — Locate your contribution file

The prompt produces `.archive/evolution-report/evolution-meta.json`. That is your contribution file. It contains aggregate metrics only — no source code, no file paths, no commit messages.

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

### Step 3 (optional) — Anonymize

If you prefer not to identify the project:
- Change `project_name` to something generic (e.g. `"python-api-service-2026"`)
- Generalize `max_gap_context` to avoid revealing organizational details
- You can leave `framework` vague (e.g. `"Python web framework"`)

The fields that matter most for corpus analysis are the numeric ones (commits, LOC, ratios, gaps) — these do not need to be altered.

### Step 4 — Validate

Run the validator to confirm your file matches the schema:

```bash
python3 schema/validate.py path/to/evolution-meta.json
```

On success you will see a one-line summary. On failure, each error is labeled with the field that failed.

If you don't have the repo cloned yet:
```bash
git clone https://github.com/briandawson/aad-analysis.git
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

## Privacy

The schema captures **aggregate metrics only**:
- No source code is collected
- No file paths are collected
- No commit messages are collected
- LOC counts and ratios are summary statistics

The most sensitive field is `max_gap_context`, which is a free-text description of what was happening during the longest commit gap. You can generalize this or leave it blank if preferred.

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
