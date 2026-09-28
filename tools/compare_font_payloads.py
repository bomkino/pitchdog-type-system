#!/usr/bin/env python3
"""Prove that two font files differ only in naming and style-linking metadata.

Every table is compiled from both files and compared byte for byte, except the
tables `normalize_font_names.py` is allowed to touch. Those are compared field by
field with the permitted fields masked out. Any other difference fails.

Usage:
    python3 tools/compare_font_payloads.py BEFORE AFTER
    python3 tools/compare_font_payloads.py --tree BEFORE_DIR AFTER_DIR [--json OUT]
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

FONT_SUFFIXES = {".woff2", ".woff", ".ttf", ".otf"}
NAME_ONLY_TABLES = {"name"}
FIELD_CHECKED_TABLES = {"head", "OS/2", "fvar", "CFF "}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def masked_head(font: TTFont):
    table = copy.copy(font["head"])
    table.checkSumAdjustment = 0
    table.macStyle &= ~0b11
    return vars(table)


def masked_os2(font: TTFont):
    table = copy.copy(font["OS/2"])
    table.fsSelection &= ~0b1100001
    fields = {key: value for key, value in vars(table).items() if not key.startswith("_")}
    fields["panose"] = vars(fields["panose"]) if "panose" in fields else None
    return fields


def masked_fvar(font: TTFont):
    return [
        (axis.axisTag, axis.minValue, axis.defaultValue, axis.maxValue, axis.flags)
        for axis in font["fvar"].axes
    ] + [
        (tuple(sorted(instance.coordinates.items())), instance.flags)
        for instance in font["fvar"].instances
    ]


def masked_cff(font: TTFont):
    cff = font["CFF "].cff
    top = cff.topDictIndex[0]
    glyphs = top.CharStrings
    outlines = {}
    for name in top.charset:
        charstring = glyphs[name]
        charstring.decompile()
        outlines[name] = charstring.program
    # Offsets move when a name grows; the data they point at is compared directly.
    offsets = {"charset", "Encoding", "CharStrings", "Private", "FDArray", "FDSelect", "Subrs"}
    naming = {"FamilyName", "FullName", "Weight"}
    kept = {
        key: value
        for key, value in top.rawDict.items()
        if key not in naming | offsets and isinstance(value, (int, float, str, list, tuple))
    }
    kept["charset"] = list(top.charset)
    private = {
        key: value
        for key, value in top.Private.rawDict.items()
        if key not in offsets and isinstance(value, (int, float, str, list, tuple))
    }
    subrs = getattr(top.Private, "Subrs", None)
    if subrs is not None:
        private["Subrs"] = [subrs.getItemAndSelector(index)[0].bytecode for index in range(len(subrs))]
    private["GlobalSubrs"] = [cff.GlobalSubrs.getItemAndSelector(index)[0].bytecode for index in range(len(cff.GlobalSubrs))]
    return {"top": kept, "private": private, "outlines": outlines}


def compare(before_path: Path, after_path: Path) -> dict:
    before = TTFont(before_path)
    after = TTFont(after_path)
    result = {
        "before": {"sha256": sha256(before_path), "bytes": before_path.stat().st_size},
        "after": {"sha256": sha256(after_path), "bytes": after_path.stat().st_size},
        "changedTables": [],
        "problems": [],
    }
    tags_before = set(before.keys()) - {"GlyphOrder"}
    tags_after = set(after.keys()) - {"GlyphOrder"}
    if tags_before != tags_after:
        result["problems"].append(f"table set changed: {sorted(tags_before ^ tags_after)}")
    if before.getGlyphOrder() != after.getGlyphOrder():
        result["problems"].append("glyph order changed")

    for tag in sorted(tags_before & tags_after):
        if tag in NAME_ONLY_TABLES:
            result["changedTables"].append(tag)
            continue
        if tag in FIELD_CHECKED_TABLES:
            masker = {"head": masked_head, "OS/2": masked_os2, "fvar": masked_fvar, "CFF ": masked_cff}[tag]
            if masker(before) != masker(after):
                result["problems"].append(f"{tag} changed outside naming and style-link fields")
            else:
                result["changedTables"].append(tag)
            continue
        if before.getTableData(tag) != after.getTableData(tag):
            if before[tag].compile(before) != after[tag].compile(after):
                result["problems"].append(f"{tag} changed")
    return result


def pairs(before_root: Path, after_root: Path):
    for before in sorted(before_root.rglob("*")):
        if before.is_file() and before.suffix.lower() in FONT_SUFFIXES:
            relative = before.relative_to(before_root)
            yield relative, before, after_root / relative


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--tree", action="store_true", help="compare every font below two directories")
    parser.add_argument("--json", type=Path, help="write the per-file report here")
    args = parser.parse_args()

    if args.tree:
        report = {}
        for relative, before, after in pairs(args.before, args.after):
            if not after.is_file():
                report[relative.as_posix()] = {"problems": ["missing after normalization"]}
                continue
            report[relative.as_posix()] = compare(before, after)
    else:
        report = {args.after.name: compare(args.before, args.after)}

    failing = {key: value["problems"] for key, value in report.items() if value["problems"]}
    for key, found in failing.items():
        print(f"{key}: {'; '.join(found)}")
    if args.json:
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Compared {len(report)} fonts: {len(report) - len(failing)} differ only in naming metadata, {len(failing)} fail")
    return 1 if failing else 0


if __name__ == "__main__":
    raise SystemExit(main())
