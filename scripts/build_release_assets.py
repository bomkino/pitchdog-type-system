#!/usr/bin/env python3
"""Build the GitHub Release assets: runtime fonts, full font handoff and agent skill.

Each ZIP is written with fixed timestamps and sorted entries so the same tree always
produces the same bytes, and gets a `.sha256` sidecar in `sha256sum` format.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
LEGAL = ["FONT-LICENSE.md", "FONT-PROVENANCE.json"]


def write_zip(output: Path, prefix: str, entries: list[tuple[Path, str]]) -> None:
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for source, name in sorted(entries, key=lambda item: item[1]):
            info = ZipInfo(f"{prefix}/{name}", date_time=FIXED_TIME)
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, source.read_bytes())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    (output.parent / f"{output.name}.sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")
    print(f"{digest}  {output.name}")


def tree(root: Path) -> list[tuple[Path, str]]:
    return [(path, path.relative_to(root).as_posix()) for path in root.rglob("*") if path.is_file()]


def legal() -> list[tuple[Path, str]]:
    return [(ROOT / name, name) for name in LEGAL]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True, help="release tag, for example v2.0.0")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    fonts = f"pitchdog-fonts-{args.tag}"
    write_zip(args.output / f"{fonts}.zip", fonts, tree(ROOT / "assets" / "fonts") + legal())

    handoff = f"pitchdog-font-handoff-{args.tag}"
    write_zip(args.output / f"{handoff}.zip", handoff, tree(ROOT / "pitchdog-font-handoff") + legal())

    skill = f"pitchdog-type-system-skill-{args.tag}"
    write_zip(args.output / f"{skill}.zip", "pitchdog-type-system", tree(ROOT / "skills" / "pitchdog-type-system"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
