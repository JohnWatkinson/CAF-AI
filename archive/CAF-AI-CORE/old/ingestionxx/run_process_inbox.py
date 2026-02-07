import os
import sys
from datetime import datetime

import yaml

REQUIRED_FIELDS = [
    "type",
    "region",
    "language",
    "source",
    "generated",
    "retrieved",
    "agent",
    "reviewed",
    "reviewer",
    "verified",
    "status",
    "original_file",
    "notes",
]

STAGED_DIR = "knowledge/staged/"
INBOX_DIR = "knowledge/inbox/"


def today():
    return datetime.now().strftime("%Y-%m-%d")


def parse_md_with_yaml(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].lstrip()
            return meta, body
    return {}, content


def build_yaml_block(meta):
    return (
        "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n\n"
    )


def default_for(field):
    if field in ["verified"]:
        return False
    if field in ["generated", "retrieved"]:
        return today()
    if field in ["reviewed", "reviewer"]:
        return ""
    if field == "status":
        return "staged"
    return ""


def process_file(filepath):
    filename = os.path.basename(filepath)
    print(f"\nProcessing: {filename}")

    try:
        meta, body = parse_md_with_yaml(filepath)
    except Exception as e:
        print(f"  [ERROR] Could not parse YAML frontmatter: {e}")
        return {"filename": filename, "status": "error", "reason": str(e)}

    updated_fields = []
    warnings = []
    # Ensure 'type' exists (alias for previous 'topic')
    if "type" not in meta and "topic" in meta:
        meta["type"] = meta["topic"]
        updated_fields.append("type (from topic)")
    # Remove legacy 'topic' key if present
    if "topic" in meta:
        meta.pop("topic")

    # Set schema version if missing
    if "schema_version" not in meta:
        meta["schema_version"] = "1.0"
        updated_fields.append("schema_version")

    # Fill missing required fields with good defaults
    for field in REQUIRED_FIELDS:
        if field not in meta or meta[field] is None:
            meta[field] = default_for(field)
            updated_fields.append(field)
        # Warn if still blank after default (except reviewer, notes)
        if not meta[field] and field not in ["reviewer", "notes"]:
            warnings.append(field)

    # Always set status to 'staged'
    meta["status"] = "staged"
    # Auto-fill original_file if blank
    if not meta.get("original_file"):
        meta["original_file"] = filename
        updated_fields.append("original_file")

    # YAML frontmatter always at top
    new_content = build_yaml_block(meta) + body
    staged_path = os.path.join(STAGED_DIR, filename)

    try:
        with open(staged_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        print(f"  [ERROR] Failed to write file: {e}")
        return {"filename": filename, "status": "error", "reason": str(e)}

    print(f"  → staged/{filename}")
    if updated_fields:
        print(f"  [!] Updated fields: {', '.join(updated_fields)}")
    if warnings:
        print(f"  [!] Warning: Fields still blank: {', '.join(warnings)}")
    return {
        "filename": filename,
        "status": "ok",
        "updated": updated_fields,
        "warnings": warnings,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_process_inbox.py <filename|--all>")
        return
    os.makedirs(STAGED_DIR, exist_ok=True)
    if sys.argv[1] == "--all":
        results = []
        for fname in os.listdir(INBOX_DIR):
            if fname.endswith(".md"):
                result = process_file(os.path.join(INBOX_DIR, fname))
                results.append(result)

        # At the end, print a summary
        ok = [r for r in results if r["status"] == "ok"]
        errors = [r for r in results if r["status"] == "error"]
        print(
            f"\nProcessed: {len(results)} files  |  Staged: {len(ok)}  |  Errors: {len(errors)}"
        )
        if errors:
            print("Files with errors:")
            for err in errors:
                print(f"  - {err['filename']}: {err['reason']}")
    else:
        process_file(sys.argv[1])


if __name__ == "__main__":
    main()


# It will:
# Take a filename (or a folder for batch mode)
# Check/add YAML frontmatter
# Ensure all required fields are present
# Update the status: staged
# Save to staged/ with the same filename
# Log missing fields/issues

# python ingestion/run_process_inbox.py knowledge/inbox/imu_torino_sitepages.md
# python ingestion/run_process_inbox.py --all
