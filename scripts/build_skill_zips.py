"""Rebuild claude-ai-skill-zips/*.zip from the Git source of skills/ and write
tests/archive-inventory.json, the file tests/test_archives.py checks.

Each ZIP holds exactly the files Git has for skills/<skill>/, named
<skill>/<path> with forward slashes, the same bytes as in Git (no line ending
changes). A ZIP whose contents already match is left as it is, so its bytes
and hash do not change. Others are written again with fixed timestamps, so a
rebuild of the same source gives the same file.

Usage (from the repo root, after staging or committing the skill changes):
    python scripts/build_skill_zips.py          # rebuild and write the inventory
    python scripts/build_skill_zips.py --check  # report only, change nothing

Skills whose name starts with a prefix in SKIP_PREFIXES are left alone (not
rebuilt, not in the inventory). The optise-helix-* skills are co-owned with
Optise, so their ZIPs change only when both owners agree. To include them,
pass --include-optise.
"""
import hashlib
import io
import json
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZIP_DIR = ROOT / "claude-ai-skill-zips"
INVENTORY = ROOT / "tests" / "archive-inventory.json"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
SKIP_PREFIXES = ("optise-helix-",)


def git_source():
    """Files under skills/ in the current Git index, as {skill: {name: bytes}}."""
    tree = subprocess.check_output(["git", "-C", str(ROOT), "write-tree"], text=True).strip()
    raw = subprocess.check_output(["git", "-C", str(ROOT), "archive", "--format=tar", tree, "skills"])
    skills = {}
    with tarfile.open(fileobj=io.BytesIO(raw)) as t:
        for m in t:
            if not m.isfile():
                continue
            rel = m.name.removeprefix("skills/")
            skill = rel.split("/", 1)[0]
            skills.setdefault(skill, {})[rel] = t.extractfile(m).read()
    return skills


def matches(path, expected):
    try:
        with zipfile.ZipFile(path) as z:
            if z.testzip() is not None or set(z.namelist()) != set(expected):
                return False
            return all(z.read(n) == body for n, body in expected.items())
    except (OSError, zipfile.BadZipFile):
        return False


def write_zip(path, expected):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(expected):
            info = zipfile.ZipInfo(name, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, expected[name])
    path.write_bytes(buf.getvalue())


def main(check_only, skip):
    source = git_source()
    rebuilt, kept, skipped, rows = [], [], [], []
    for skill in sorted(source):
        if not (source[skill].get(f"{skill}/SKILL.md")):
            continue  # not a skill folder
        if skill.startswith(skip):
            skipped.append(skill)
            continue
        path = ZIP_DIR / f"{skill}.zip"
        if matches(path, source[skill]):
            kept.append(skill)
        else:
            rebuilt.append(skill)
            if not check_only:
                write_zip(path, source[skill])
        if path.exists():
            rows.append({
                "repo": "helix-gtm-suite",
                "file": f"claude-ai-skill-zips/{skill}.zip",
                "entries": len(source[skill]),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    orphans = sorted(p.stem for p in ZIP_DIR.glob("*.zip") if p.stem not in source)
    print(f"already matching: {len(kept)}; {'out of date' if check_only else 'rebuilt'}: {len(rebuilt)}")
    for s in rebuilt:
        print("  ", s)
    if skipped:
        print("left alone (co-owned):", ", ".join(skipped))
    if orphans:
        print("ZIPs with no skill folder (left alone):", ", ".join(orphans))
    if not check_only:
        INVENTORY.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {INVENTORY.relative_to(ROOT)} with {len(rows)} rows")
    return 1 if (check_only and rebuilt) else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    sys.exit(main("--check" in args, () if "--include-optise" in args else SKIP_PREFIXES))
