#!/usr/bin/env python3
"""Static integrity checks for the pitch.dog Type System v13 release."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_SUFFIXES = {".woff2", ".woff", ".otf", ".ttf", ".ttc"}
ARROWS = ["←", "↑", "→", "↓", "↔", "↕", "↖", "↗", "↘", "↙", "↩", "↪"]
EXPECTED_ANCHORS = {
    "head": {"wght": [265, 300, 400, 500, 600, 700, 900], "ital": [0, 1]},
    "headAlt": {"wght": [265, 300, 400, 500, 600, 700, 900], "ital": [0, 1]},
    "body": {"wght": [100, 250, 300, 400, 600, 700, 900]},
    "bodyAlt": {"wght": [100, 250, 300, 400, 600, 700, 900]},
    "eyebrow": {
        "wght": [100, 200, 300, 350, 400, 500, 600, 700, 800, 900],
        "wdth": [87.5, 100],
        "ital": [0, 1],
    },
}
EXPECTED_COUNTS = {"web": 17, "ui": 14, "social": 9, "youtube": 7}
EXPECTED_CANVASES = {"social": 4, "youtube": 5}

errors: list[str] = []
checks: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        checks.append(message)
    else:
        errors.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostic path
        errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")
        return None


def flatten_dtcg_typography(node: dict, prefix: str = "") -> dict:
    """Return dotted paths for every typography token below a DTCG group."""
    flattened: dict = {}
    for name, value in node.items():
        path = f"{prefix}.{name}" if prefix else name
        if isinstance(value, dict) and value.get("$type") == "typography":
            flattened[path] = value
        elif isinstance(value, dict):
            flattened.update(flatten_dtcg_typography(value, path))
    return flattened


# Every JSON file in the package must parse.
for json_file in sorted(ROOT.rglob("*.json")):
    if json_file == ROOT / "evidence/static-validation.json":
        continue
    load_json(json_file)
check(not any(message.startswith("invalid JSON:") for message in errors), "all JSON parses")

tokens = load_json(ROOT / "tokens/pitchdog.system.tokens.json") or {}
meta = tokens.get("meta", {})
check(meta.get("version") == "13.1.0", "version is 13.1.0")
check(meta.get("displayVersion") == "13", "display version is lucky number 13")
check(
    meta.get("fontSource") == "FontBlind-Final-2026-08-28-v13.zip",
    "v13 font authority recorded",
)

anchors = tokens.get("anchors", {})
for family, expected in EXPECTED_ANCHORS.items():
    actual = anchors.get(family, {})
    for axis, values in expected.items():
        check(actual.get(axis) == values, f"{family} {axis} anchors exact")

allowed_weights = {
    family: set(contract["wght"]) for family, contract in EXPECTED_ANCHORS.items()
}
for group, expected_count in EXPECTED_COUNTS.items():
    roles = tokens.get(group, {}).get("roles", {})
    check(len(roles) == expected_count, f"{group} has {expected_count} semantic roles")
    for role_name, role in roles.items():
        family = role.get("family")
        weight = role.get("weight")
        check(family in allowed_weights, f"{group}.{role_name} uses a governed family")
        if family in allowed_weights:
            check(
                weight in allowed_weights[family],
                f"{group}.{role_name} uses an authentic weight anchor",
            )
        if family in {"head", "headAlt"}:
            check(role.get("ital", 0) in {0, 1}, f"{group}.{role_name} Head ital is anchored")
        elif family in {"body", "bodyAlt"}:
            check(
                role.get("style", "normal") in {"normal", "italic"},
                f"{group}.{role_name} Body posture selects an authentic file",
            )
        elif family == "eyebrow":
            check(role.get("width", 87.5) in {87.5, 100}, f"{group}.{role_name} Eyebrow width is anchored")
            check(role.get("ital", 0) in {0, 1}, f"{group}.{role_name} Eyebrow ital is binary")

dtcg = load_json(ROOT / "tokens/pitchdog.system.dtcg.json") or {}
dtcg_web_group = (dtcg.get("type") or {}).get("web")
dtcg_web = (
    flatten_dtcg_typography(dtcg_web_group)
    if isinstance(dtcg_web_group, dict)
    else {}
)
canonical_web = tokens.get("web", {}).get("roles", {})
web_measures = tokens.get("web", {}).get("measures", {})
check(
    {name: contract.get("value") for name, contract in web_measures.items()}
    == {
        "narrow": "38ch",
        "intro": "48ch",
        "reading": "45ch",
        "default": "48ch",
        "wide": "52ch",
        "ceiling": "54ch",
    },
    "web measure tokens are exact",
)
wrap_styles = tokens.get("web", {}).get("wrapStyles", {})
check(
    set(wrap_styles) == {"auto", "balance", "pretty", "stable", "avoid-orphans"},
    "web wrapping styles are complete",
)
check(
    len(dtcg_web) == 17 and set(dtcg_web) == set(canonical_web),
    "DTCG preserves all 17 unique web role paths",
)


def dtcg_web_role_matches(role_name: str, exported: dict) -> bool:
    role = canonical_web[role_name]
    expected_value = {
        "fontFamily": f"{{font.family.{role['family']}}}",
        "fontSize": role["size"],
        "fontWeight": role["weight"],
        "letterSpacing": role["tracking"],
        "lineHeight": role["lineHeight"],
    }
    expected_extension = {
        key: value
        for key, value in role.items()
        if key not in {"family", "size", "weight", "tracking", "lineHeight"}
    }
    return (
        exported.get("$value") == expected_value
        and exported.get("$extensions", {}).get("pitchdog") == expected_extension
    )

check(
    set(dtcg_web) == set(canonical_web)
    and all(dtcg_web_role_matches(name, dtcg_web[name]) for name in canonical_web),
    "DTCG web role values match the canonical source",
)

for group, expected_count in EXPECTED_CANVASES.items():
    canvases = tokens.get(group, {}).get("canvases", {})
    check(len(canvases) == expected_count, f"{group} has {expected_count} canonical canvases")

arrow_contract = tokens.get("arrows", {})
check(arrow_contract.get("glyphs") == ARROWS, "all twelve native arrows are governed")
check(
    arrow_contract.get("roles", {}).get("ui", {}).get("family") == "eyebrow"
    and arrow_contract.get("roles", {}).get("ui", {}).get("weight") == 600
    and arrow_contract.get("roles", {}).get("ui", {}).get("width") == 100,
    "UI arrows use Eyebrow 600 at width 100",
)

font_audit = load_json(ROOT / "evidence/font-audit.json") or {}
fonts = font_audit.get("fonts", {})
check(len(fonts) == 7, "font audit records seven runtime variable fonts")
for key, font in fonts.items():
    check(font.get("hasRupee") is True, f"{key} contains native rupee")
    check(all(font.get("arrowsPresent", {}).get(glyph) for glyph in ARROWS), f"{key} contains all arrows")
check(fonts.get("eyebrow", {}).get("codepointCount") == 404, "Eyebrow has 404 encoded characters")
check(fonts.get("eyebrow", {}).get("currencyCount") == 34, "Eyebrow has 34 supported currencies")
check(
    [axis.get("tag") for axis in fonts.get("eyebrow", {}).get("axes", [])]
    == ["wght", "wdth", "ital"],
    "Eyebrow exposes genuine wght, wdth and ital axes",
)

html_path = ROOT / "pitchdog-typography-system-v13.html"
baker_path = ROOT / "MAKE-STANDALONE-v13.html"
html = html_path.read_text(encoding="utf-8")
baker = baker_path.read_text(encoding="utf-8")
check(html == baker, "main lab and local baker are identical")
check("font/woff2;base64" not in html, "distributable HTML contains no embedded font payload")
malformed_inline_axis = re.compile(
    r'<[^>]*\bstyle="[^">]*font-variation-settings:"'
)
check(
    not any(malformed_inline_axis.search(document) for document in (html, baker)),
    "HTML inline axis styles use valid attribute quoting",
)
check(
    '<link rel="stylesheet" href="dist/pitchdog-fonts.template.css" data-pd-repo-fonts>' in html,
    "repository font stylesheet is linked",
)
check(
    "clone.querySelector('[data-pd-repo-fonts]')?.remove()" in baker,
    "standalone builder removes the repository font stylesheet",
)
check('"ital" 1' in html and 'data-pd-emphasis="head-italic"' in html, "Head italic proof is explicit")
check("sha256Fallback" in baker, "local baker has a non-secure-context SHA-256 fallback")
check("DecompressionStream" in baker, "local baker can unpack supported ZIPs in-browser")
check("Build embedded standalone HTML" in baker, "local standalone builder is present")
check("data:image/svg+xml" in html, "inline SVG favicon is embedded in review HTML")
for glyph in ARROWS:
    check(glyph in html, f"HTML specimen contains {glyph}")

manifest = load_json(ROOT / "assets/favicons/site.webmanifest") or {}
check(
    manifest.get("start_url") == "./pitchdog-typography-system-v13.html",
    "web manifest points to v13 HTML",
)
for relative in [
    "assets/favicons/favicon.svg",
    "assets/favicons/favicon-16x16.png",
    "assets/favicons/favicon-32x32.png",
    "assets/favicons/apple-touch-icon.png",
    "assets/favicons/icon-192.png",
    "assets/favicons/icon-512.png",
    "assets/favicons/site.webmanifest",
]:
    check((ROOT / relative).exists(), f"favicon asset exists: {relative}")

browser_validation = load_json(ROOT / "evidence/browser-validation.json") or {}
check(browser_validation.get("passed") == 100, "browser gauntlet records 100 passes")
check(browser_validation.get("failed") == 0, "browser gauntlet records zero failures")
check(not browser_validation.get("console"), "browser gauntlet records no console errors")
check(not browser_validation.get("pageErrors"), "browser gauntlet records no page errors")

font_files = [path for path in ROOT.rglob("*") if path.is_file() and path.suffix.lower() in FONT_SUFFIXES]
unexpected_fonts = []
for path in font_files:
    relative = path.relative_to(ROOT)
    if relative.parts[:2] == ("assets", "fonts"):
        continue
    if relative.parts and relative.parts[0] == "pitchdog-font-handoff-v13":
        continue
    unexpected_fonts.append(relative.as_posix())
check(not unexpected_fonts, f"no font binaries outside governed directories: {unexpected_fonts}")

required_docs = [
    "SPECIFICATION.md",
    "ANCHOR-POLICY.md",
    "HEAD-ITALICS.md",
    "DENSE-TEXT.md",
    "UI-UX-TYPOGRAPHY.md",
    "SOCIAL-TYPOGRAPHY.md",
    "YOUTUBE.md",
    "ARROWS.md",
    "ACCESSIBILITY-QA.md",
    "IMPLEMENTATION.md",
    "GOVERNANCE.md",
    "VALIDATION-REPORT.md",
    "WEB-TEXT-WRAPPING.md",
]
for name in required_docs:
    check((ROOT / "docs" / name).exists(), f"documentation exists: {name}")

wrap_contracts = load_json(ROOT / "dist" / "pitchdog-wrap-contracts.json") or {}
check(wrap_contracts.get("version") == "13.1.0", "wrap contracts carry the release version")
check(
    wrap_contracts.get("measures", {}).get("reading") == "45ch"
    and wrap_contracts.get("measures", {}).get("ceiling") == "54ch",
    "wrap contract measures preserve the reading target and accessibility ceiling",
)
typography_css = (ROOT / "dist" / "pitchdog-typography.css").read_text(encoding="utf-8")
for marker in [
    'data-pd-wrap="balance"',
    'data-pd-wrap="pretty"',
    'data-pd-wrap="stable"',
    'data-pd-wrap="avoid-orphans"',
    'data-pd-measure="reading"',
    'data-pd-measure="ceiling"',
    "@supports (text-wrap-style: avoid-orphans)",
    "hyphens: auto",
]:
    check(marker in typography_css, f"typography CSS contains {marker}")

result = {
    "pass": not errors,
    "checksPassed": len(checks),
    "checksFailed": len(errors),
    "checks": checks,
    "errors": errors,
}
print(json.dumps(result, indent=2, ensure_ascii=False))
raise SystemExit(1 if errors else 0)
