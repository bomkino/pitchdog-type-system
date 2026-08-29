#!/usr/bin/env python3
"""Write or verify the repository-wide SHA-256 manifest."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "SHA256SUMS.txt"
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
SKIP_FILES = {"SHA256SUMS.txt", ".DS_Store", "Thumbs.db"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def files() -> list[Path]:
    rows: list[Path] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if path.is_file() and path.name not in SKIP_FILES:
            rows.append(path)
    return sorted(rows, key=lambda item: item.relative_to(ROOT).as_posix())


def render() -> str:
    return "".join(
        f"{digest(path)}  {path.relative_to(ROOT).as_posix()}\n"
        for path in files()
    )


def verify() -> int:
    if not MANIFEST.exists():
        print("ERROR: SHA256SUMS.txt is missing")
        return 1
    expected = MANIFEST.read_text(encoding="utf-8")
    actual = render()
    if expected != actual:
        print("ERROR: SHA256SUMS.txt is stale or a repository file changed")
        return 1
    print(f"Repository checksums verified: {len(files())} files")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="replace SHA256SUMS.txt")
    args = parser.parse_args()
    if args.write:
        MANIFEST.write_text(render(), encoding="utf-8")
        print(f"Wrote {MANIFEST} ({len(files())} files)")
        return 0
    return verify()


if __name__ == "__main__":
    raise SystemExit(main())

