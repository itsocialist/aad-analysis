#!/usr/bin/env python3
"""
AAD Evolution Meta validator.

Usage:
    python validate.py path/to/evolution-meta.json
    python validate.py --all path/to/corpus/projects/

Exits 0 on success, 1 on validation failure.
"""

import sys
import json
import os
import subprocess


def ensure_jsonschema():
    """Auto-install jsonschema if not present."""
    try:
        import jsonschema  # noqa: F401
    except ImportError:
        print("jsonschema not found. Installing...", file=sys.stderr)
        # Try --user install first, then --break-system-packages as fallback
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "jsonschema", "-q", "--user"],
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "jsonschema", "-q",
                     "--break-system-packages"],
                    stderr=subprocess.DEVNULL,
                )
            except subprocess.CalledProcessError:
                print(
                    "Could not auto-install jsonschema.\n"
                    "Please run:  pip install jsonschema\n"
                    "or:          python3 -m venv .venv && source .venv/bin/activate "
                    "&& pip install jsonschema",
                    file=sys.stderr,
                )
                sys.exit(2)


ensure_jsonschema()

import jsonschema  # noqa: E402


SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "evolution-meta.schema.json")


def load_schema():
    with open(SCHEMA_PATH) as f:
        return json.load(f)


def validate_file(path, schema):
    """Validate a single JSON file. Returns (ok, summary_or_errors)."""
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error: {e}"]
    except FileNotFoundError:
        return False, [f"File not found: {path}"]

    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))

    if errors:
        messages = []
        for err in errors:
            path_str = " -> ".join(str(p) for p in err.path) if err.path else "(root)"
            messages.append(f"  [{path_str}] {err.message}")
        return False, messages

    # Build one-line summary
    project_name = data.get("project_name", data.get("project", {}).get("name", os.path.basename(path)))
    language = data.get("primary_language", "unknown")
    commits = data.get("total_commits", "?")
    loc_first = data.get("loc_first", "?")
    loc_last = data.get("loc_last", "?")
    summary = f"{project_name} | {language} | {commits} commits | LOC {loc_first} -> {loc_last}"
    return True, summary


def validate_all(directory, schema):
    """Validate all .json files in a directory. Returns (pass_count, fail_count)."""
    json_files = sorted(
        f for f in os.listdir(directory) if f.endswith(".json")
    )
    if not json_files:
        print(f"No .json files found in {directory}", file=sys.stderr)
        return 0, 0

    pass_count = 0
    fail_count = 0

    for filename in json_files:
        filepath = os.path.join(directory, filename)
        ok, result = validate_file(filepath, schema)
        if ok:
            print(f"  [OK] {filename}")
            print(f"        {result}")
            pass_count += 1
        else:
            print(f"  [FAIL] {filename}")
            for msg in result:
                print(f"        {msg}")
            fail_count += 1

    return pass_count, fail_count


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    try:
        schema = load_schema()
    except FileNotFoundError:
        print(f"Schema not found at: {SCHEMA_PATH}", file=sys.stderr)
        sys.exit(1)

    if args[0] == "--all":
        if len(args) < 2:
            print("Usage: validate.py --all <directory>", file=sys.stderr)
            sys.exit(1)
        directory = args[1]
        if not os.path.isdir(directory):
            print(f"Not a directory: {directory}", file=sys.stderr)
            sys.exit(1)

        print(f"\nValidating all JSON files in: {directory}\n")
        pass_count, fail_count = validate_all(directory, schema)
        total = pass_count + fail_count
        print(f"\n{'='*50}")
        print(f"Results: {pass_count}/{total} passed, {fail_count}/{total} failed")
        sys.exit(0 if fail_count == 0 else 1)

    else:
        # Single file mode
        filepath = args[0]
        ok, result = validate_file(filepath, schema)
        if ok:
            print(f"  [OK] {os.path.basename(filepath)}")
            print(f"        {result}")
            sys.exit(0)
        else:
            print(f"  [FAIL] {os.path.basename(filepath)}")
            for msg in result:
                print(f"        {msg}")
            sys.exit(1)


if __name__ == "__main__":
    main()
