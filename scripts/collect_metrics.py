#!/usr/bin/env python3
"""
collect_metrics.py — deterministic git metrics extractor for the AAD corpus.

Produces the same evolution-meta.json that COLLECT_PROMPT.md instructs an
LLM to produce, but from deterministic git commands. Use this for consistent,
auditable, privacy-safe results. The LLM prompt handles qualitative steps
(narrative, security ratings, charts) — this script handles the numbers.

Privacy guarantees:
  - Contributor emails are replaced with contributor-1 / contributor-2 etc.
  - Real names are never written to any output file.
  - Commit message text is classified (feat/fix/etc.) but never reproduced.
  - No file paths appear in the JSON sidecar.

Usage:
  cd /path/to/your/repo
  python3 /path/to/aad-analysis/scripts/collect_metrics.py

Output:
  .archive/evolution-report/evolution-meta.json   (schema-conformant)
  .archive/evolution-report/per_commit_metrics.csv (anonymized)

Then run the full COLLECT_PROMPT.md to add narrative, charts, and snapshots.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def git(*args, check=True):
    result = subprocess.run(
        ["git"] + list(args),
        capture_output=True, text=True, check=check
    )
    return result.stdout.strip()


def git_lines(*args):
    out = git(*args)
    return [l for l in out.splitlines() if l.strip()]


# ---------------------------------------------------------------------------
# Contributor anonymization
# ---------------------------------------------------------------------------

def build_contributor_map():
    """Map real emails -> contributor-N handles, ordered by first commit."""
    log = git("log", "--reverse", "--format=%ae")
    seen = {}
    for email in log.splitlines():
        email = email.strip().lower()
        if email and email not in seen:
            seen[email] = f"contributor-{len(seen) + 1}"
    return seen


# ---------------------------------------------------------------------------
# Commit classification (no message text is stored)
# ---------------------------------------------------------------------------

CONVENTIONAL_RE = re.compile(
    r"^(feat|fix|refactor|test|chore|docs|style|perf|ci|build|security|plan)"
    r"(\([^)]*\))?[!:]",
    re.IGNORECASE,
)

REWORK_MARKERS = re.compile(
    r"\bv\d+\b|attempt|take\s+\d|retry|redo|revert|rollback", re.IGNORECASE
)

TOPIC_KEYWORDS = {
    "auth":   r"auth|oauth|login|session|token|jwt|saml|sso|csrf",
    "ui":     r"\bui\b|css|style|layout|component|design|theme|modal|button",
    "api":    r"\bapi\b|endpoint|route|rest|graphql|rpc|handler",
    "db":     r"db|database|schema|migration|query|prisma|sequel|mongo|redis",
    "test":   r"\btest\b|spec|vitest|jest|pytest|coverage|fixture|mock",
    "infra":  r"infra|deploy|ci|cd|docker|k8s|terraform|pipeline|workflow",
    "docs":   r"\bdocs?\b|readme|changelog|comment",
    "security": r"security|secret|key|encrypt|vuln|cve|harden|sanitize",
    "perf":   r"perf|performance|speed|latency|cache|optim",
}


def classify_commit(message):
    """Return (kind, topics, is_rework). Never stores message text."""
    kind = "other"
    m = CONVENTIONAL_RE.match(message)
    if m:
        kind = m.group(1).lower()

    topics = []
    msg_lower = message.lower()
    for topic, pattern in TOPIC_KEYWORDS.items():
        if re.search(pattern, msg_lower):
            topics.append(topic)

    is_rework = bool(REWORK_MARKERS.search(message))
    return kind, topics, is_rework


# ---------------------------------------------------------------------------
# Per-commit metrics
# ---------------------------------------------------------------------------

def collect_commits(contributor_map):
    """Return list of dicts with anonymized metrics per commit."""
    sep = "\x1f"
    fmt = sep.join(["%H", "%ae", "%ai", "%s"])
    raw = git("log", "--reverse", f"--format={fmt}", "--numstat")

    commits = []
    current = None

    for line in raw.splitlines():
        parts = line.split(sep)
        if len(parts) == 4:
            sha, email, date_str, subject = parts
            email = email.strip().lower()
            handle = contributor_map.get(email, "contributor-unknown")
            kind, topics, is_rework = classify_commit(subject)
            dt = datetime.fromisoformat(date_str.strip())
            current = {
                "sha": sha[:8],
                "contributor": handle,   # anonymized
                "timestamp": dt.isoformat(),
                "kind": kind,
                "topics": ",".join(topics),
                "is_rework": is_rework,
                "files_changed": 0,
                "insertions": 0,
                "deletions": 0,
                "gap_hours": None,
            }
            commits.append(current)
        elif current and line.strip():
            # numstat line: insertions<tab>deletions<tab>filename
            cols = line.split("\t")
            if len(cols) >= 2:
                try:
                    ins = int(cols[0]) if cols[0] != "-" else 0
                    dels = int(cols[1]) if cols[1] != "-" else 0
                    current["insertions"] += ins
                    current["deletions"] += dels
                    current["files_changed"] += 1
                except ValueError:
                    pass

    # compute gaps
    for i in range(1, len(commits)):
        t_prev = datetime.fromisoformat(commits[i - 1]["timestamp"])
        t_curr = datetime.fromisoformat(commits[i]["timestamp"])
        gap = (t_curr - t_prev).total_seconds() / 3600
        commits[i]["gap_hours"] = round(gap, 2)

    return commits


# ---------------------------------------------------------------------------
# Aggregate metrics
# ---------------------------------------------------------------------------

def median(values):
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2


def compute_aggregates(commits):
    n = len(commits)
    half = n // 2
    first_half = commits[:half]
    second_half = commits[half:]

    def fix_feat_ratio(subset):
        feats = sum(1 for c in subset if c["kind"] == "feat")
        fixes = sum(1 for c in subset if c["kind"] == "fix")
        return round(fixes / feats, 3) if feats > 0 else 0.0

    def median_gap(subset):
        gaps = [c["gap_hours"] for c in subset if c["gap_hours"] is not None]
        return round(median(gaps), 2)

    gaps = [c["gap_hours"] for c in commits if c["gap_hours"] is not None]
    max_gap = max(gaps) if gaps else 0
    max_gap_idx = next(
        (i for i, c in enumerate(commits) if c["gap_hours"] == max_gap), 0
    )

    from collections import Counter
    topic_counts = Counter()
    for c in commits:
        for t in c["topics"].split(","):
            if t:
                topic_counts[t] += 1
    dominant_topic = topic_counts.most_common(1)[0][0] if topic_counts else "unknown"

    explicit_iter = sum(1 for c in commits if c["is_rework"])
    revert_count = sum(1 for c in commits if c["kind"] == "other" and
                       re.search(r"revert|rollback", "", re.IGNORECASE))

    return {
        "fix_feat_ratio_first_half": fix_feat_ratio(first_half),
        "fix_feat_ratio_second_half": fix_feat_ratio(second_half),
        "median_gap_hours_first_half": median_gap(first_half),
        "median_gap_hours_second_half": median_gap(second_half),
        "dominant_rework_topic": dominant_topic,
        "explicit_iteration_commits": explicit_iter,
        "rollback_commits": revert_count,
        "max_gap_hours": round(max_gap, 1),
        "max_gap_context": "see narrative.md — do not include names or paths here",
    }


# ---------------------------------------------------------------------------
# LOC (rough, language-agnostic)
# ---------------------------------------------------------------------------

def count_loc_at_head():
    """Count non-blank, non-comment lines by extension at HEAD."""
    try:
        files = git_lines("ls-files")
    except Exception:
        return 0

    total = 0
    for f in files:
        if not Path(f).exists():
            continue
        ext = Path(f).suffix.lower()
        if ext in (".png", ".jpg", ".gif", ".ico", ".woff", ".ttf", ".pdf",
                   ".zip", ".gz", ".lock"):
            continue
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                total += sum(1 for line in fh if line.strip())
        except OSError:
            pass
    return total


def count_loc_at_first_commit():
    first_sha = git("log", "--reverse", "--format=%H", "--max-count=1")
    try:
        raw = git("show", "--numstat", f"{first_sha}^..{first_sha}")
    except Exception:
        return 0
    total = 0
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            try:
                total += int(parts[0])
            except ValueError:
                pass
    return total


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # confirm we're in a git repo
    try:
        git("rev-parse", "--is-inside-work-tree")
    except subprocess.CalledProcessError:
        print("ERROR: not inside a git repository.", file=sys.stderr)
        sys.exit(1)

    print("Step 0 — Privacy scan + contributor anonymization...")
    contributor_map = build_contributor_map()
    n_contributors = len(contributor_map)
    print(f"  {n_contributors} contributor(s) anonymized.")

    # check for obvious secret files (names only, no content read)
    secret_patterns = [".env", "*.key", "*.pem", "*credentials*", "*secret*"]
    secret_files = []
    for pattern in secret_patterns:
        try:
            found = git("ls-files", pattern, check=False)
            secret_files.extend([l for l in found.splitlines() if l.strip()])
        except Exception:
            pass
    if secret_files:
        print(f"  ⚠  Potential secret files detected ({len(secret_files)}).")
        print("     Review these before sharing any analysis output.")
        for sf in secret_files[:5]:
            print(f"     - {sf}")
    else:
        print("  No obvious secret file names detected.")

    print("Collecting per-commit metrics...")
    commits = collect_commits(contributor_map)

    print("Computing aggregates...")
    agg = compute_aggregates(commits)

    # date range
    if commits:
        t0 = datetime.fromisoformat(commits[0]["timestamp"])
        t1 = datetime.fromisoformat(commits[-1]["timestamp"])
        date_range_days = max(1, (t1 - t0).days)
    else:
        date_range_days = 0

    # LOC
    loc_last = count_loc_at_head()
    loc_first = count_loc_at_first_commit()

    # project name — use directory name as default (contributor should review)
    project_name = Path.cwd().name

    meta = {
        "project_name": project_name,
        "primary_language": "unknown — fill in",
        "framework": "unknown — fill in",
        "ai_assisted": "unknown",
        "total_commits": len(commits),
        "date_range_days": date_range_days,
        "snapshot_count": 0,
        "fix_feat_ratio_first_half": agg["fix_feat_ratio_first_half"],
        "fix_feat_ratio_second_half": agg["fix_feat_ratio_second_half"],
        "median_gap_hours_first_half": agg["median_gap_hours_first_half"],
        "median_gap_hours_second_half": agg["median_gap_hours_second_half"],
        "dominant_rework_topic": agg["dominant_rework_topic"],
        "explicit_iteration_commits": agg["explicit_iteration_commits"],
        "rollback_commits": agg["rollback_commits"],
        "loc_first": loc_first,
        "loc_last": loc_last,
        "test_ratio_first": 0.0,
        "test_ratio_last": 0.0,
        "max_gap_hours": agg["max_gap_hours"],
        "max_gap_context": agg["max_gap_context"],
    }

    # write output
    out_dir = Path(".archive/evolution-report")
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON sidecar
    json_path = out_dir / "evolution-meta.json"
    with open(json_path, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Written: {json_path}")

    # CSV (anonymized)
    csv_path = out_dir / "per_commit_metrics.csv"
    import csv
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "sha", "contributor", "timestamp", "kind", "topics",
            "is_rework", "files_changed", "insertions", "deletions", "gap_hours"
        ])
        writer.writeheader()
        writer.writerows(commits)
    print(f"Written: {csv_path}")

    print()
    print("Next steps:")
    print("  1. Edit evolution-meta.json: fill in primary_language, framework, ai_assisted")
    print("  2. Review max_gap_context — keep it generic (no names, paths, or internal system names)")
    print("  3. Run COLLECT_PROMPT.md in Claude Code for narrative, charts, and snapshot table")
    print("  4. Validate: python3 /path/to/aad-analysis/schema/validate.py .archive/evolution-report/evolution-meta.json")


if __name__ == "__main__":
    main()
