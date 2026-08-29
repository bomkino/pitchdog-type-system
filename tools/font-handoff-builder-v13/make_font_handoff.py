#!/usr/bin/env python3
"""Build the curated pitch.dog v13 font handoff from the FontBlind v13 source ZIP.

Uses only Python's standard library. The generated handoff contains font binaries;
this builder package does not.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

VERSION = "13"
SOURCE_BASENAME = "FontBlind-Final-2026-08-28-v13.zip"
OUTPUT_BASENAME = "pitchdog-font-handoff-v13.zip"
ROOT = "pitchdog-font-handoff-v13"
FIXED_DT = (2026, 8, 28, 0, 0, 0)

VARIABLE_MAP = [
    ("01-PUBLIC-FONTS/LAB/pd-head/web/pd-head.woff2", "01-WEB-VARIABLE/pd-head.woff2", "web", "PD Head", "woff2", ["wght 265–900", "ital 0–1"]),
    ("01-PUBLIC-FONTS/LAB/pd-head/web/pd-head-alt.woff2", "01-WEB-VARIABLE/pd-head-alt.woff2", "web", "PD Head Alt", "woff2", ["wght 265–900", "ital 0–1"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-roman.woff2", "01-WEB-VARIABLE/pd-body-roman.woff2", "web", "PD Body", "woff2", ["wght 100–900", "roman"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-italic.woff2", "01-WEB-VARIABLE/pd-body-italic.woff2", "web", "PD Body", "woff2", ["wght 100–900", "authentic italic"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-alt-roman.woff2", "01-WEB-VARIABLE/pd-body-alt-roman.woff2", "web", "PD Body Alt", "woff2", ["wght 100–900", "roman"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/web/pd-body-alt-italic.woff2", "01-WEB-VARIABLE/pd-body-alt-italic.woff2", "web", "PD Body Alt", "woff2", ["wght 100–900", "authentic italic"]),
    ("01-PUBLIC-FONTS/LAB/pd-eyebrow/site/pd-eyebrow-site.woff2", "01-WEB-VARIABLE/pd-eyebrow.woff2", "web", "PD Eyebrow", "woff2", ["wght 100–900", "wdth 87.5–100", "ital 0/1", "404-codepoint site runtime"]),
    ("01-PUBLIC-FONTS/LAB/pd-head/native/pd-head.ttf", "02-NATIVE-VARIABLE/pd-head.ttf", "native", "PD Head", "ttf", ["wght 265–900", "ital 0–1"]),
    ("01-PUBLIC-FONTS/LAB/pd-head/native/pd-head-alt.ttf", "02-NATIVE-VARIABLE/pd-head-alt.ttf", "native", "PD Head Alt", "ttf", ["wght 265–900", "ital 0–1"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/native/pd-body-roman.ttf", "02-NATIVE-VARIABLE/pd-body-roman.ttf", "native", "PD Body", "ttf", ["wght 100–900", "roman"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/native/pd-body-italic.ttf", "02-NATIVE-VARIABLE/pd-body-italic.ttf", "native", "PD Body", "ttf", ["wght 100–900", "authentic italic"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/native/pd-body-alt-roman.ttf", "02-NATIVE-VARIABLE/pd-body-alt-roman.ttf", "native", "PD Body Alt", "ttf", ["wght 100–900", "roman"]),
    ("01-PUBLIC-FONTS/LAB/pd-body/native/pd-body-alt-italic.ttf", "02-NATIVE-VARIABLE/pd-body-alt-italic.ttf", "native", "PD Body Alt", "ttf", ["wght 100–900", "authentic italic"]),
    ("01-PUBLIC-FONTS/LAB/pd-eyebrow/native/pd-eyebrow-variable-web.ttf", "02-NATIVE-VARIABLE/pd-eyebrow-full.ttf", "native", "PD Eyebrow", "ttf", ["wght 100–900", "wdth 87.5–100", "ital 0/1", "477-codepoint full master"]),
]

STATIC_GROUPS = [
    ("01-PUBLIC-FONTS/BLIND/pd-head/native/", ".ttf", "03-STATIC-ANCHORS-NATIVE/pd-head", 14),
    ("01-PUBLIC-FONTS/BLIND/pd-body/native/", ".otf", "03-STATIC-ANCHORS-NATIVE/pd-body", 28),
    ("01-PUBLIC-FONTS/BLIND/pd-eyebrow/native/", ".ttf", "03-STATIC-ANCHORS-NATIVE/pd-eyebrow", 20),
    ("01-PUBLIC-FONTS/BLIND/pd-head/web/", ".woff2", "04-OPTIONAL-STATIC-WEB/pd-head", 14),
    ("01-PUBLIC-FONTS/BLIND/pd-body/web/", ".woff2", "04-OPTIONAL-STATIC-WEB/pd-body", 28),
    ("01-PUBLIC-FONTS/BLIND/pd-eyebrow/web/", ".woff2", "04-OPTIONAL-STATIC-WEB/pd-eyebrow", 20),
]

FONT_CSS = r'''/* pitch.dog v13 — canonical variable webfont registration. */
@font-face {
  font-family: "PD Head";
  src: url("./pd-head.woff2") format("woff2-variations");
  font-weight: 265 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "PD Head";
  src: url("./pd-head.woff2") format("woff2-variations");
  font-weight: 265 900;
  font-style: italic;
  font-display: swap;
}
@font-face {
  font-family: "PD Head Alt";
  src: url("./pd-head-alt.woff2") format("woff2-variations");
  font-weight: 265 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "PD Head Alt";
  src: url("./pd-head-alt.woff2") format("woff2-variations");
  font-weight: 265 900;
  font-style: italic;
  font-display: swap;
}
@font-face {
  font-family: "PD Body";
  src: url("./pd-body-roman.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "PD Body";
  src: url("./pd-body-italic.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: italic;
  font-display: swap;
}
@font-face {
  font-family: "PD Body Alt";
  src: url("./pd-body-alt-roman.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "PD Body Alt";
  src: url("./pd-body-alt-italic.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-style: italic;
  font-display: swap;
}
@font-face {
  font-family: "PD Eyebrow";
  src: url("./pd-eyebrow.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-stretch: 87.5% 100%;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "PD Eyebrow";
  src: url("./pd-eyebrow.woff2") format("woff2-variations");
  font-weight: 100 900;
  font-stretch: 87.5% 100%;
  font-style: italic;
  font-display: swap;
}

/* Head italic is safest when the actual ital axis is explicit. */
.pd-head-italic {
  font-family: "PD Head";
  font-style: normal;
  font-variation-settings: "wght" 500, "ital" 1;
}

/* Production values should land on the approved anchors documented in AXES-AND-ANCHORS.md. */
'''

README_FIRST = r'''# pitch.dog Font Handoff — v13

Send this entire folder to web developers, app developers and social/content designers.

## Which folder each person uses

- **Web developers:** `01-WEB-VARIABLE/`
- **App developers:** `02-NATIVE-VARIABLE/`
- **Social, video and graphic designers:** install `02-NATIVE-VARIABLE/`
- **Fallback when a tool mishandles variable fonts:** uninstall the matching variable family, then use `03-STATIC-ANCHORS-NATIVE/`
- **Legacy or non-variable web target only:** `04-OPTIONAL-STATIC-WEB/`

## Canonical rule

The variable fonts are authoritative. Production values should land on the approved source anchors rather than arbitrary in-between values. Continuous interpolation is reserved for intentional animation or controlled experiments.

## Do not install duplicates

Do **not** install the variable and static versions of the same family at the same time. Font menus can merge or hide duplicate family records unpredictably. Use variable first. Use static anchors only as a fallback.

## Eyebrow naming caveat

The files are named `pd-eyebrow`, but the current internal installed family name is **Untitled**. Web CSS aliases it to `PD Eyebrow`, so web work is unaffected. Desktop and native tools may display `Untitled` in font menus. This is source-font metadata, not a packaging error. Rename it in a future source build if a clean installed name is required.

The 350 and 400 static Eyebrow anchors also share the same full and PostScript names. Do not install all Eyebrow static anchors together. Prefer the variable font; when a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time.

## Licence

The font binaries are dedicated under CC0 1.0 Universal. See `LICENSE-CC0-NOTE.md`. Keeping that notice with redistributed copies is a provenance best practice, not a licence condition.
'''

WEB_README = r'''# Web developers

Use the seven WOFF2 variable files in this folder and import `pitchdog-fonts.css`.

## Runtime faces

1. `pd-head.woff2`
2. `pd-head-alt.woff2`
3. `pd-body-roman.woff2`
4. `pd-body-italic.woff2`
5. `pd-body-alt-roman.woff2`
6. `pd-body-alt-italic.woff2`
7. `pd-eyebrow.woff2`

The Eyebrow file is the smaller 404-codepoint website runtime. It retains all 34 supported currencies, ₹, fraction slash, required shaping closure and the complete arrow set.

## Important implementation details

- Head and Head Alt carry `wght` and `ital` in one file. For critical italic display work, explicitly set `"ital" 1` rather than relying only on synthetic or inferred italics.
- Body and Body Alt use separate authentic Roman and Italic variable files.
- Eyebrow carries `wght`, `wdth` and binary `ital` axes.
- Use exact anchors from `../05-DOCUMENTATION/AXES-AND-ANCHORS.md`.
- Do not preload all seven files. Preload only fonts required by the likely first viewport.
- The static WOFF2 folder is optional and should not ship beside the variable files unless a specific target cannot use variable fonts.
'''

NATIVE_README = r'''# App developers and design tools

Use the seven variable TTF files in this folder first.

- Head and Head Alt: one variable TTF each.
- Body and Body Alt: separate authentic Roman and Italic variable TTFs.
- Eyebrow: the fuller 477-codepoint native master.

Keep production settings on the approved anchors. Some native frameworks expose axes by tag; others expose named instances. Where custom variation values are supported, use the tags and values in `../05-DOCUMENTATION/AXES-AND-ANCHORS.md`.

If a framework or design application mishandles variable instances, remove the variable family and install the matching files in `../03-STATIC-ANCHORS-NATIVE/` instead.

Do not install variable and static duplicates simultaneously.

Note: PD Eyebrow currently installs under the internal family name `Untitled`.

PD Body Italic has correct italic behaviour but exposes `Regular` in two native style-name records. Some native menus may pair it inconsistently; web CSS is unaffected.
'''

STATIC_NATIVE_README = r'''# Optional native static anchors

These are exact source-master anchors for tools that do not handle the variable fonts reliably.

- `pd-head/`: 14 TTF files, Primary and Alt, seven upright weight anchors each. Head italics still require the variable font because the source italic is an axis rather than a separate static family in this release.
- `pd-body/`: 28 OTF files, Primary and Alt, seven authentic Roman and seven authentic Italic anchors per family.
- `pd-eyebrow/`: 20 TTF files, ten Normal-width anchors in Upright and Italic.

Install these only after removing the matching variable family.

**Eyebrow warning:** the 350 and 400 upright files share `Untitled Regular` / `Untitled-Regular`; the 350 and 400 italic files share `Untitled Italic` / `Untitled-Italic`. Native installers can overwrite or hide one face. Prefer the variable Eyebrow. If a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time.
'''

STATIC_WEB_README = r'''# Optional static WOFF2 anchors

These are for a web target that cannot consume the canonical variable WOFF2 files.

Modern pitch.dog web work should use `../01-WEB-VARIABLE/` instead. Do not load both sets on the same page.
'''

ANCHORS = r'''# Axes and approved anchors

## PD Head / PD Head Alt

- Weight: `265, 300, 400, 500, 600, 700, 900`
- Italic: `0, 1`
- Continuous interpolation between upright and italic is permitted only for deliberate motion or a controlled specimen.

Typical system use:

- 500: section headings and feature quotations
- 600: hero and chapter displays
- 700: compressed media surfaces such as YouTube thumbnails

## PD Body / PD Body Alt

- Weight: `100, 250, 300, 400, 600, 700, 900`
- Roman and Italic are separate authentic variable files.

Typical system use:

- 400: reading and standard interface copy
- 600: functional emphasis, controls and compact titles
- 700: metrics and high-pressure media surfaces

## PD Eyebrow

- Weight: `100, 200, 300, 350, 400, 500, 600, 700, 800, 900`
- Width: `87.5, 100`
- Italic: `0, 1`

Typical system use:

- 500 / 87.5: metadata, filenames, dates and aligned data
- 600 / 100: compact UI arrows and icon-like controls
- Italic 1: rare annotations, never a generic decorative default

## Arrow set

`← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↩ ↪`

The arrows are present across all seven variable runtime faces and the static anchors.
'''

AUDIENCE_MAP = r'''# Audience map

| Audience | Primary files | Optional fallback | Notes |
|---|---|---|---|
| Website developer | `01-WEB-VARIABLE/*.woff2` | `04-OPTIONAL-STATIC-WEB/` | Import the included CSS; keep Head ital explicit. |
| iOS / Android / desktop app developer | `02-NATIVE-VARIABLE/*.ttf` | `03-STATIC-ANCHORS-NATIVE/` | Use exact axes; test platform font registration. |
| Figma / Adobe / Canva / social designer | `02-NATIVE-VARIABLE/*.ttf` | `03-STATIC-ANCHORS-NATIVE/` | Install variable first; do not install duplicates. |
| Video / YouTube designer | `02-NATIVE-VARIABLE/*.ttf` | static native anchors | Head 700 is the approved high-pressure display anchor. |

The full pitch.dog typography, UI, social and YouTube behaviour lives in the separate Type System v13 package. This handoff contains the font assets and the minimum integration contract only.
'''

LICENSE_NOTE = r'''# Font licence — CC0 1.0 Universal

The FontBlind v13 font binaries in this handoff (`.woff2`, `.woff`, `.ttf` and `.otf`) are dedicated to the public domain under **CC0 1.0 Universal** (`CC0-1.0`). They may be copied, modified, distributed and used, including commercially, without an attribution requirement.

Legal code: <https://creativecommons.org/publicdomain/zero/1.0/legalcode>

This declaration applies only to the font binaries. Handoff documentation, CSS, artwork, and pitch.dog names and marks are not placed under CC0 by this notice.

CC0 does not require recipients to retain this notice. Keeping it with redistributed font files is requested as a provenance best practice, not as an additional licence condition.

This file records pitch.dog's CC0 declaration for the v13 font release. It is not an independent legal audit of authorship, trademarks, provenance or third-party source material.
'''

KNOWN_ISSUES = r'''# Known source-font details

## PD Eyebrow internal family name

The Eyebrow binaries currently identify internally as `Untitled` / `Untitled Regular`, even though their filenames and design-system alias are `pd-eyebrow` / `PD Eyebrow`.

Consequences:

- Web: no practical issue. `@font-face` aliases the file as `PD Eyebrow`.
- Desktop design tools: the font may appear as `Untitled`.
- Native apps: some APIs may require the internal PostScript or family name rather than the filename.
- Collision risk: another installed font using the family name `Untitled` may conflict.

The static source also contains two internal collisions:

- 350 and 400 upright both expose `Untitled Regular` / `Untitled-Regular` and the same unique-name record.
- 350 and 400 italic both expose `Untitled Italic` / `Untitled-Italic` and the same unique-name record.

Native installers can overwrite, hide or substitute these distinct files. Prefer the variable Eyebrow. If a static fallback is unavoidable, install only one required Eyebrow weight/posture at a time.

## PD Body Italic style name

`pd-body-italic` has correct italic flags and italic angle, but its subfamily and typographic-subfamily records say `Regular`. Web CSS works correctly; some native menus or pairing APIs may display it inconsistently.

The handoff deliberately preserves the accepted v13 source binaries. A future font-source release should rename the internal records rather than patching them ad hoc in downstream products.
'''


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel_source(name: str) -> str:
    marker = "01-PUBLIC-FONTS/"
    idx = name.find(marker)
    if idx < 0:
        return name
    return name[idx:]


def locate(names: list[str], suffix: str) -> str:
    hits = [n for n in names if n.endswith(suffix)]
    if len(hits) != 1:
        raise RuntimeError(f"Expected exactly one source for {suffix!r}; found {len(hits)}")
    return hits[0]


def parse_source_sums(zf: ZipFile, names: list[str]) -> dict[str, str]:
    sum_names = [n for n in names if n.endswith("/SHA256SUMS") or n == "SHA256SUMS"]
    if len(sum_names) != 1:
        raise RuntimeError("Source SHA256SUMS was not found uniquely")
    out: dict[str, str] = {}
    for line in zf.read(sum_names[0]).decode("utf-8", "replace").splitlines():
        m = re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$", line.strip())
        if m:
            out[m.group(2)] = m.group(1).lower()
    return out


def zip_info(path: str) -> ZipInfo:
    info = ZipInfo(f"{ROOT}/{path}", FIXED_DT)
    info.compress_type = ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    return info


def doc_bytes(text: str) -> bytes:
    return (text.rstrip() + "\n").encode("utf-8")


def static_meta(output_path: str) -> dict:
    name = PurePosixPath(output_path).name
    family = "PD Head" if "/pd-head/" in output_path else "PD Body" if "/pd-body/" in output_path else "PD Eyebrow"
    if "alt" in name:
        family += " Alt"
    style = "italic" if "italic" in name.lower() else "upright"
    weight_match = re.search(r"(?:-|^)(100|200|250|265|300|350|400|500|600|700|800|900)(?:-|\.|$)", name)
    named = next((x for x in ["thin", "light", "regular", "medium", "semibold", "bold", "black"] if x in name.lower()), None)
    return {
        "family": family,
        "style": style,
        "weight": int(weight_match.group(1)) if weight_match else named,
        "variable": False,
    }


def build(source: Path, output: Path) -> dict:
    if not source.exists():
        raise FileNotFoundError(source)

    package_files: dict[str, bytes] = {}
    font_entries: list[dict] = []

    with ZipFile(source) as zf:
        names = [n for n in zf.namelist() if not n.endswith("/")]
        source_sums = parse_source_sums(zf, names)

        def add_font(source_name: str, output_path: str, extra: dict) -> None:
            data = zf.read(source_name)
            rel = rel_source(source_name)
            expected = source_sums.get(rel)
            actual = sha256(data)
            if expected and expected != actual:
                raise RuntimeError(f"Source checksum mismatch: {rel}")
            if output_path in package_files:
                raise RuntimeError(f"Duplicate output path: {output_path}")
            package_files[output_path] = data
            font_entries.append({
                "outputPath": output_path,
                "sourcePath": rel,
                "bytes": len(data),
                "sha256": actual,
                **extra,
            })

        for suffix, out, audience, family, fmt, axes in VARIABLE_MAP:
            src = locate(names, suffix)
            add_font(src, out, {
                "audience": audience,
                "family": family,
                "format": fmt,
                "variable": True,
                "axes": axes,
            })

        for source_dir, ext, output_dir, expected_count in STATIC_GROUPS:
            hits = sorted(n for n in names if source_dir in n and n.lower().endswith(ext))
            if len(hits) != expected_count:
                raise RuntimeError(f"Expected {expected_count} files in {source_dir}; found {len(hits)}")
            for src in hits:
                out = f"{output_dir}/{PurePosixPath(src).name}"
                meta = static_meta(out)
                add_font(src, out, {
                    "audience": "fallback",
                    "format": ext.lstrip("."),
                    **meta,
                })

    docs: dict[str, bytes] = {
        "README-FIRST.md": doc_bytes(README_FIRST),
        "LICENSE-CC0-NOTE.md": doc_bytes(LICENSE_NOTE),
        "01-WEB-VARIABLE/README.md": doc_bytes(WEB_README),
        "01-WEB-VARIABLE/pitchdog-fonts.css": doc_bytes(FONT_CSS),
        "02-NATIVE-VARIABLE/README.md": doc_bytes(NATIVE_README),
        "03-STATIC-ANCHORS-NATIVE/README.md": doc_bytes(STATIC_NATIVE_README),
        "04-OPTIONAL-STATIC-WEB/README.md": doc_bytes(STATIC_WEB_README),
        "05-DOCUMENTATION/AXES-AND-ANCHORS.md": doc_bytes(ANCHORS),
        "05-DOCUMENTATION/AUDIENCE-MAP.md": doc_bytes(AUDIENCE_MAP),
        "05-DOCUMENTATION/KNOWN-SOURCE-DETAILS.md": doc_bytes(KNOWN_ISSUES),
    }

    manifest = {
        "name": "pitch.dog Font Handoff",
        "version": "13",
        "sourceArchive": source.name,
        "generatedBy": "pitch.dog Font Handoff Builder v13",
        "fontFileCount": len(font_entries),
        "fontBytes": sum(e["bytes"] for e in font_entries),
        "canonicalPolicy": "Variable fonts first; exact source anchors for production; static files only as compatibility fallbacks.",
        "fonts": sorted(font_entries, key=lambda e: e["outputPath"]),
    }
    docs["05-DOCUMENTATION/FONT-MANIFEST.json"] = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")

    all_without_sums = {**package_files, **docs}
    sums = "".join(f"{sha256(data)}  {path}\n" for path, data in sorted(all_without_sums.items()))
    all_files = {**all_without_sums, "SHA256SUMS.txt": sums.encode("utf-8")}

    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as outzip:
        for path in sorted(all_files):
            outzip.writestr(zip_info(path), all_files[path])

    return {
        "output": str(output),
        "fontFiles": len(font_entries),
        "allFiles": len(all_files),
        "fontBytes": manifest["fontBytes"],
        "zipBytes": output.stat().st_size,
        "sha256": sha256(output.read_bytes()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help=f"Path to {SOURCE_BASENAME}")
    parser.add_argument("-o", "--output", type=Path, default=Path(OUTPUT_BASENAME))
    args = parser.parse_args()
    try:
        result = build(args.source, args.output)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
