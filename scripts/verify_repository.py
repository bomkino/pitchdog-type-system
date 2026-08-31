#!/usr/bin/env python3
"""Verify the private pitch.dog type-system repository as a consumable release."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
FONT_SUFFIXES = {".woff2", ".woff", ".ttf", ".otf", ".ttc"}
errors: list[str] = []
checks: list[str] = []


def check(condition: bool, message: str) -> None:
    (checks if condition else errors).append(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def validate_package() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    check(package.get("name") == "@pitchdog/type-system", "package name is canonical")
    check(package.get("version") == "13.1.0", "package version is 13.1.0")
    check(package.get("private") is True, "package cannot be published accidentally")
    packaged = set(package.get("files", []))
    for legal_file in ["LICENSE.md", "FONT-LICENSE.md", "FONT-PROVENANCE.json"]:
        check(legal_file in packaged, f"web package includes {legal_file}")
    check(package.get("exports", {}).get("./fonts.css") == "./dist/pitchdog-fonts.template.css", "split CSS exposes governed font registration")
    for name, target in package.get("exports", {}).items():
        path = ROOT / target.replace("./", "", 1)
        if "*" in target:
            check(path.parent.exists(), f"package export base exists: {name}")
        else:
            check(path.is_file(), f"package export exists: {name}")


def validate_runtime() -> None:
    records = json.loads((ROOT / "dist" / "pitchdog-font-runtime.json").read_text(encoding="utf-8"))
    expected: set[Path] = set()
    for record in records:
        path = ROOT / record["file"]
        expected.add(path)
        check(path.is_file(), f"runtime font exists: {record['key']}")
        if path.is_file():
            check(path.stat().st_size == record["bytes"], f"runtime font size exact: {record['key']}")
            check(sha256(path) == record["sha256"], f"runtime font hash exact: {record['key']}")
    actual = {path for path in (ROOT / "assets" / "fonts").glob("*") if path.is_file()} if (ROOT / "assets" / "fonts").exists() else set()
    check(actual == expected, "runtime directory contains exactly seven governed faces")


def validate_handoff() -> None:
    handoff = ROOT / "pitchdog-font-handoff-v13"
    sums = handoff / "SHA256SUMS.txt"
    check(sums.is_file(), "full font handoff is present")
    if not sums.is_file():
        return
    governed: set[str] = set()
    for line in sums.read_text(encoding="utf-8").splitlines():
        try:
            expected, relative = line.split(maxsplit=1)
        except ValueError:
            errors.append(f"malformed handoff checksum line: {line!r}")
            continue
        relative = relative.lstrip("*")
        pure = PurePosixPath(relative)
        safe = not pure.is_absolute() and ".." not in pure.parts
        check(safe, f"safe handoff path: {relative}")
        if not safe:
            continue
        target = handoff.joinpath(*pure.parts)
        check(target.is_file(), f"handoff file exists: {relative}")
        if target.is_file():
            check(sha256(target) == expected.lower(), f"handoff hash exact: {relative}")
        governed.add(pure.as_posix())
    actual = {
        path.relative_to(handoff).as_posix()
        for path in handoff.rglob("*")
        if path.is_file() and path != sums
    }
    check(actual == governed, "handoff checksum manifest covers every payload")
    font_count = sum(path.suffix.lower() in FONT_SUFFIXES for path in handoff.rglob("*") if path.is_file())
    check(font_count == 138, "handoff contains 138 font files")


def validate_font_boundaries() -> None:
    unexpected: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in FONT_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        if relative.parts[:2] == ("assets", "fonts"):
            continue
        if relative.parts and relative.parts[0] == "pitchdog-font-handoff-v13":
            continue
        unexpected.append(relative.as_posix())
    check(not unexpected, f"no fonts outside governed directories: {unexpected}")


def run_validator(path: Path, label: str) -> None:
    result = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, capture_output=True)
    if result.returncode == 0:
        checks.append(label)
    else:
        errors.append(f"{label} failed\n{result.stdout}\n{result.stderr}".strip())


def main() -> int:
    validate_package()
    validate_runtime()
    validate_handoff()
    validate_font_boundaries()
    run_validator(ROOT / "tools" / "validate_release.py", "semantic type-system validation")
    run_validator(ROOT / "scripts" / "checksums.py", "repository checksum validation")
    result = {
        "pass": not errors,
        "checksPassed": len(checks),
        "checksFailed": len(errors),
        "errors": errors,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
