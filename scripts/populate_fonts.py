#!/usr/bin/env python3
"""Populate the governed fonts from the accepted FontBlind v13 source or its generated handoff ZIP.

The source binaries are rebuilt into the v13 handoff, verified against that handoff's
own checksums, renamed by `tools/normalize_font_names.py`, and then accepted only if
every font matches the hashes committed for this release. Only font binaries are
written; the handoff's documentation stays as committed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools" / "font-handoff-builder-v13" / "make_font_handoff.py"
RUNTIME_MANIFEST = ROOT / "dist" / "pitchdog-font-runtime.json"
HANDOFF_TARGET = ROOT / "pitchdog-font-handoff"
NORMALIZER = ROOT / "tools" / "normalize_font_names.py"
FONT_SUFFIXES = {".woff2", ".woff", ".ttf", ".otf", ".ttc"}
RUNTIME_TARGET = ROOT / "assets" / "fonts"

WEB_TO_RUNTIME = {
    "pd-head.woff2": "pd-head.woff2",
    "pd-head-alt.woff2": "pd-head-alt.woff2",
    "pd-body-roman.woff2": "pd-body-roman.woff2",
    "pd-body-italic.woff2": "pd-body-italic.woff2",
    "pd-body-alt-roman.woff2": "pd-body-alt-roman.woff2",
    "pd-body-alt-italic.woff2": "pd-body-alt-italic.woff2",
    "pd-eyebrow.woff2": "pd-eyebrow-site.woff2",
}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def safe_member(info: ZipInfo) -> PurePosixPath:
    path = PurePosixPath(info.filename)
    mode = (info.external_attr >> 16) & 0o170000
    if path.is_absolute() or ".." in path.parts or mode == 0o120000:
        raise RuntimeError(f"Unsafe ZIP member: {info.filename}")
    return path


def detect_handoff_root(zf: ZipFile) -> str:
    marker = "01-WEB-VARIABLE/pd-head.woff2"
    matches = [name[: -len(marker)].rstrip("/") for name in zf.namelist() if name.endswith(marker)]
    if len(matches) != 1:
        raise RuntimeError("Expected one pitchdog-font-handoff-v13 root")
    return matches[0]


def unpack_handoff(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with ZipFile(archive) as zf:
        prefix = detect_handoff_root(zf)
        prefix_parts = PurePosixPath(prefix).parts
        for info in zf.infolist():
            member = safe_member(info)
            if member.parts[: len(prefix_parts)] != prefix_parts:
                continue
            relative = PurePosixPath(*member.parts[len(prefix_parts) :])
            if not relative.parts:
                continue
            target = destination.joinpath(*relative.parts)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(zf.read(info))


def verify_handoff(root: Path) -> int:
    manifest = root / "SHA256SUMS.txt"
    if not manifest.exists():
        raise RuntimeError("Handoff SHA256SUMS.txt is missing")
    governed: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        relative = relative.lstrip("*")
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts:
            raise RuntimeError(f"Unsafe handoff checksum path: {relative}")
        target = root.joinpath(*path.parts)
        if not target.is_file() or sha256(target) != expected.lower():
            raise RuntimeError(f"Handoff checksum failed: {relative}")
        governed.add(path.as_posix())
    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path != manifest
    }
    if governed != actual:
        missing = sorted(actual - governed)
        extra = sorted(governed - actual)
        raise RuntimeError(f"Handoff checksum coverage mismatch; missing={missing}, extra={extra}")
    font_count = sum(path.suffix.lower() in FONT_SUFFIXES for path in root.rglob("*") if path.is_file())
    if font_count != 138:
        raise RuntimeError(f"Expected 138 handoff font files, found {font_count}")
    return font_count


def stage_runtime(handoff: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    web = handoff / "01-WEB-VARIABLE"
    for source_name, target_name in WEB_TO_RUNTIME.items():
        source = web / source_name
        if not source.is_file():
            raise RuntimeError(f"Missing handoff runtime face: {source_name}")
        shutil.copy2(source, destination / target_name)

    expected = json.loads(RUNTIME_MANIFEST.read_text(encoding="utf-8"))
    expected_names = set()
    for record in expected:
        target = destination / Path(record["file"]).name
        expected_names.add(target.name)
        if target.stat().st_size != record["bytes"] or sha256(target) != record["sha256"]:
            raise RuntimeError(f"Runtime verification failed: {target.name}")
    actual_names = {path.name for path in destination.iterdir() if path.is_file()}
    if actual_names != expected_names:
        raise RuntimeError("Runtime directory contains an unexpected file set")


def committed_font_hashes() -> dict[str, str]:
    manifest = HANDOFF_TARGET / "SHA256SUMS.txt"
    if not manifest.is_file():
        raise RuntimeError("Committed pitchdog-font-handoff/SHA256SUMS.txt is missing")
    hashes: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        relative = relative.lstrip("*")
        if PurePosixPath(relative).suffix.lower() in FONT_SUFFIXES:
            hashes[relative] = expected.lower()
    return hashes


def verify_against_release(staged_handoff: Path, staged_runtime: Path) -> dict[str, str]:
    expected = committed_font_hashes()
    staged = {
        path.relative_to(staged_handoff).as_posix(): sha256(path)
        for path in staged_handoff.rglob("*")
        if path.is_file() and path.suffix.lower() in FONT_SUFFIXES
    }
    if set(staged) != set(expected):
        raise RuntimeError(
            f"Font set differs from this release; missing={sorted(set(expected) - set(staged))}, extra={sorted(set(staged) - set(expected))}"
        )
    mismatched = sorted(relative for relative, digest in staged.items() if digest != expected[relative])
    if mismatched:
        raise RuntimeError(
            f"{len(mismatched)} normalized fonts do not match this release (first: {mismatched[0]}). "
            "Install the pinned tools: python3 -m pip install -r tools/requirements.txt"
        )
    stage_runtime(staged_handoff, staged_runtime)
    return expected


def install_fonts(staged_handoff: Path, staged_runtime: Path, fonts: dict[str, str], replace: bool) -> None:
    present = [relative for relative in fonts if (HANDOFF_TARGET / relative).exists()]
    present += [path.name for path in RUNTIME_TARGET.glob("*")] if RUNTIME_TARGET.exists() else []
    if present and not replace:
        raise RuntimeError("Governed fonts already exist; inspect them or rerun with --replace")
    for relative in fonts:
        target = HANDOFF_TARGET / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(staged_handoff / relative, target)
    if RUNTIME_TARGET.exists():
        shutil.rmtree(RUNTIME_TARGET)
    shutil.copytree(staged_runtime, RUNTIME_TARGET)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--replace", action="store_true", help="replace existing governed font files")
    args = parser.parse_args()
    archive = args.archive.resolve()
    if not archive.is_file():
        print(f"ERROR: archive not found: {archive}", file=sys.stderr)
        return 2

    try:
        with tempfile.TemporaryDirectory(prefix="pitchdog-fonts-") as temp_name:
            temp = Path(temp_name)
            with ZipFile(archive) as zf:
                names = zf.namelist()
            is_source = any("01-PUBLIC-FONTS/LAB/" in name for name in names)
            is_handoff = any(name.endswith("01-WEB-VARIABLE/pd-head.woff2") for name in names)
            if is_source:
                handoff_zip = temp / "pitchdog-font-handoff-v13.zip"
                subprocess.run(
                    [sys.executable, str(BUILDER), str(archive), "--output", str(handoff_zip)],
                    check=True,
                )
            elif is_handoff:
                handoff_zip = archive
            else:
                raise RuntimeError("Archive is neither the accepted FontBlind v13 source nor its generated handoff")

            staged_handoff = temp / "handoff"
            unpack_handoff(handoff_zip, staged_handoff)
            font_count = verify_handoff(staged_handoff)
            subprocess.run([sys.executable, str(NORMALIZER), str(staged_handoff)], check=True)

            staged_runtime = temp / "runtime-fonts"
            fonts = verify_against_release(staged_handoff, staged_runtime)
            install_fonts(staged_handoff, staged_runtime, fonts, args.replace)

        subprocess.run([sys.executable, str(ROOT / "scripts" / "checksums.py"), "--write"], check=True)
        print(f"Populated and verified {font_count} handoff fonts plus 7 runtime faces")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
