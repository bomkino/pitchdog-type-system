#!/usr/bin/env python3
"""Normalize pitch.dog font naming and style-linking metadata, or check that it is normalized.

The FontBlind v13 source binaries carry inconsistent internal names: PD Eyebrow calls
itself "Untitled", two Eyebrow static anchors share one name, PD Body Italic calls its
subfamily "Regular", and the static anchors disagree about which faces are Bold.

This tool rewrites only naming and style-linking metadata:

- `name` records 1, 2, 3, 4, 6, 16, 17 and 25, plus new records for variable instances
- `OS/2.fsSelection` bits 0 (italic), 5 (bold) and 6 (regular)
- `head.macStyle` bits 0 (bold) and 1 (italic)
- `fvar` instance subfamily and PostScript name IDs
- CFF top-dict family, full, weight and PostScript names

Outlines, metrics, axes, kerning and every other table are left untouched.
`tools/compare_font_payloads.py` proves that for a before/after pair.

Usage:
    python3 tools/normalize_font_names.py PATH [PATH ...]           # rewrite in place
    python3 tools/normalize_font_names.py --check PATH [PATH ...]   # verify only
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from fontTools.ttLib import TTFont

FONT_SUFFIXES = {".woff2", ".woff", ".ttf", ".otf"}

# Order matters: the longest prefix wins.
FAMILIES = [
    ("pd-head-alt", "PD Head Alt", "PDHeadAlt"),
    ("pd-head", "PD Head", "PDHead"),
    ("pd-body-alt", "PD Body Alt", "PDBodyAlt"),
    ("pd-body", "PD Body", "PDBody"),
    ("pd-eyebrow", "PD Eyebrow", "PDEyebrow"),
]

WEIGHT_NAMES = {
    100: "Thin",
    200: "ExtraLight",
    250: "ExtraLight",
    265: "Thin",
    300: "Light",
    350: "Book",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}

ITALIC_BIT = 1 << 0
BOLD_BIT = 1 << 5
REGULAR_BIT = 1 << 6
MAC_BOLD = 1 << 0
MAC_ITALIC = 1 << 1
MANAGED_NAME_IDS = (1, 2, 3, 4, 6, 16, 17, 25)


@dataclass(frozen=True)
class Plan:
    family: str
    ps_family: str
    weight: int
    italic: bool
    variable: bool
    names: dict[int, str]
    fs_selection_bits: int
    mac_style_bits: int


def family_for(path: Path) -> tuple[str, str]:
    stem = path.name
    for prefix, family, ps_family in FAMILIES:
        if stem.startswith(prefix):
            return family, ps_family
    raise ValueError(f"not a governed pitch.dog font file name: {path}")


def is_italic(path: Path, font: TTFont) -> bool:
    stem = path.stem
    if "italic" in stem.split("-"):
        return True
    return bool(font["OS/2"].fsSelection & ITALIC_BIT) and "fvar" not in font


def style_name(weight: int, italic: bool) -> str:
    weight_name = WEIGHT_NAMES[weight]
    if weight_name == "Regular":
        return "Italic" if italic else "Regular"
    return f"{weight_name} Italic" if italic else weight_name


def version_number(font: TTFont) -> str:
    """The version the font reports in name ID 5, e.g. "3.000" from "Version 3.000"."""
    version = font["name"].getDebugName(5) or ""
    parts = version.replace(";", " ").split()
    if len(parts) >= 2 and parts[0] == "Version":
        return parts[1]
    return f"{font['head'].fontRevision:.3f}"


def plan_for(path: Path, font: TTFont) -> Plan:
    family, ps_family = family_for(path)
    variable = "fvar" in font
    italic = is_italic(path, font)
    weight = 400 if variable else font["OS/2"].usWeightClass
    if weight not in WEIGHT_NAMES:
        raise ValueError(f"unexpected weight class {weight}: {path}")
    revision = version_number(font)

    if variable:
        style = "Italic" if italic else "Regular"
        ps_name = f"{ps_family}-{style}"
        names = {
            1: family,
            2: style,
            3: f"{revision};PITCHDOG;{ps_name}",
            4: f"{family} {style}",
            6: ps_name,
            16: family,
            17: style,
            25: f"{ps_family}Italic" if italic else ps_family,
        }
        bold = False
    else:
        style = style_name(weight, italic)
        bold = weight == 700
        ribbi = weight in (400, 700)
        ps_name = f"{ps_family}-{style.replace(' ', '')}"
        names = {
            1: family if ribbi else f"{family} {WEIGHT_NAMES[weight]}",
            2: ("Bold " if bold else "") + ("Italic" if italic else ("" if bold else "Regular")),
            3: f"{revision};PITCHDOG;{ps_name}",
            4: f"{family} {style}",
            6: ps_name,
            16: family,
            17: style,
        }
        names[2] = names[2].strip()

    fs_bits = (ITALIC_BIT if italic else 0) | (BOLD_BIT if bold else 0)
    if not italic and not bold:
        fs_bits |= REGULAR_BIT
    mac_bits = (MAC_ITALIC if italic else 0) | (MAC_BOLD if bold else 0)
    return Plan(family, ps_family, weight, italic, variable, names, fs_bits, mac_bits)


def instance_names(plan: Plan, font: TTFont) -> list[tuple[str, str]]:
    """Return the (subfamily, PostScript) pair every fvar instance should carry."""
    name_table = font["name"]
    rows = []
    for instance in font["fvar"].instances:
        coordinates = instance.coordinates
        italic = plan.italic or coordinates.get("ital", 0) >= 1
        weight_name = WEIGHT_NAMES[round(coordinates["wght"])]
        if weight_name == "Regular":
            label = "Italic" if italic else "Regular"
        else:
            label = f"{weight_name} Italic" if italic else weight_name
        rows.append((label, f"{plan.ps_family}-{label.replace(' ', '')}"))
    return rows


def records_for(name_table, name_id: int):
    return [record for record in name_table.names if record.nameID == name_id]


def set_managed_name(name_table, name_id: int, value: str | None) -> None:
    existing = records_for(name_table, name_id)
    if value is None:
        for record in existing:
            name_table.removeNames(nameID=name_id, platformID=record.platformID, platEncID=record.platEncID, langID=record.langID)
        return
    targets = {(record.platformID, record.platEncID, record.langID) for record in existing}
    targets.add((3, 1, 0x409))
    for platform_id, encoding_id, language_id in sorted(targets):
        name_table.setName(value, name_id, platform_id, encoding_id, language_id)


def apply(path: Path) -> bool:
    font = TTFont(path, recalcTimestamp=False, recalcBBoxes=False)
    plan = plan_for(path, font)
    name_table = font["name"]

    # Variable instances get their own name records so shared IDs (STAT, elided
    # fallback, subfamily) are never rewritten under another table's feet.
    if plan.variable:
        for instance, (label, ps_name) in zip(font["fvar"].instances, instance_names(plan, font)):
            instance.subfamilyNameID = name_table.addName(label, platforms=((3, 1, 0x409),), minNameID=256)
            instance.postscriptNameID = name_table.addName(ps_name, platforms=((3, 1, 0x409),), minNameID=256)

    for name_id in MANAGED_NAME_IDS:
        set_managed_name(name_table, name_id, plan.names.get(name_id))
    name_table.removeUnusedNames(font)

    os2 = font["OS/2"]
    os2.fsSelection = (os2.fsSelection & ~(ITALIC_BIT | BOLD_BIT | REGULAR_BIT)) | plan.fs_selection_bits
    head = font["head"]
    head.macStyle = (head.macStyle & ~(MAC_BOLD | MAC_ITALIC)) | plan.mac_style_bits

    if "CFF " in font:
        cff = font["CFF "].cff
        top = cff.topDictIndex[0]
        cff.fontNames[0] = plan.names[6]
        top.FamilyName = plan.names[16]
        top.FullName = plan.names[4]
        top.Weight = WEIGHT_NAMES[plan.weight]

    before = path.read_bytes()
    font.save(path)
    font.close()
    return path.read_bytes() != before


def problems(path: Path) -> list[str]:
    font = TTFont(path, lazy=True)
    plan = plan_for(path, font)
    name_table = font["name"]
    found: list[str] = []
    for name_id in MANAGED_NAME_IDS:
        expected = plan.names.get(name_id)
        records = records_for(name_table, name_id)
        if expected is None:
            if records:
                found.append(f"name {name_id} should be absent")
            continue
        if not records:
            found.append(f"name {name_id} missing (expected {expected!r})")
        for record in records:
            if record.toUnicode() != expected:
                found.append(f"name {name_id} is {record.toUnicode()!r}, expected {expected!r}")
    fs = font["OS/2"].fsSelection & (ITALIC_BIT | BOLD_BIT | REGULAR_BIT)
    if fs != plan.fs_selection_bits:
        found.append(f"fsSelection style bits {fs:#x}, expected {plan.fs_selection_bits:#x}")
    mac = font["head"].macStyle & (MAC_BOLD | MAC_ITALIC)
    if mac != plan.mac_style_bits:
        found.append(f"macStyle {mac:#x}, expected {plan.mac_style_bits:#x}")
    if plan.variable:
        for instance, (label, ps_name) in zip(font["fvar"].instances, instance_names(plan, font)):
            actual = (name_table.getDebugName(instance.subfamilyNameID), name_table.getDebugName(instance.postscriptNameID))
            if actual != (label, ps_name):
                found.append(f"instance {instance.coordinates} named {actual}, expected {(label, ps_name)}")
    if "CFF " in font:
        cff = font["CFF "].cff
        top = cff.topDictIndex[0]
        actual = (cff.fontNames[0], top.FamilyName, top.FullName)
        expected = (plan.names[6], plan.names[16], plan.names[4])
        if actual != expected:
            found.append(f"CFF names {actual}, expected {expected}")
    font.close()
    return found


def collect(paths: list[Path]) -> list[Path]:
    fonts: list[Path] = []
    for path in paths:
        if path.is_dir():
            fonts.extend(sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in FONT_SUFFIXES))
        elif path.suffix.lower() in FONT_SUFFIXES:
            fonts.append(path)
    return fonts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--check", action="store_true", help="report files that are not normalized; change nothing")
    args = parser.parse_args()
    fonts = collect(args.paths)
    if not fonts:
        print("ERROR: no font files found", file=sys.stderr)
        return 2

    if args.check:
        failures = {path: problems(path) for path in fonts}
        failures = {path: found for path, found in failures.items() if found}
        for path, found in failures.items():
            for message in found:
                print(f"{path}: {message}")
        # The same face legitimately ships in several containers and folders; two
        # different faces must never share a PostScript name.
        faces: dict[tuple[bool, str], tuple[Path, tuple]] = {}
        for path in fonts:
            font = TTFont(path, lazy=True)
            plan = plan_for(path, font)
            name = font["name"].getDebugName(6)
            identity = (plan.family, plan.weight, plan.italic, path.stem.replace("-site", ""))
            key = (plan.variable, name)
            if key in faces and faces[key][1][:3] != identity[:3]:
                print(f"{path}: PostScript name {name!r} also used by {faces[key][0]}")
                failures[path] = ["duplicate"]
            faces.setdefault(key, (path, identity))
            font.close()
        print(f"Font naming checked: {len(fonts)} files, {len(failures)} with problems")
        return 1 if failures else 0

    changed = sum(apply(path) for path in fonts)
    print(f"Normalized {len(fonts)} font files ({changed} changed)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
