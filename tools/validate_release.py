#!/usr/bin/env python3
"""Static integrity checks for the pitch.dog Type System release."""
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
EXPECTED_COUNTS = {"web": 17, "ui": 14, "social": 9, "youtube": 7, "deck": 14, "subtitle": 3}
EXPECTED_CANVASES = {"social": 4, "youtube": 5, "deck": 2, "subtitle": 4}
MEDIA_ATTRIBUTES = {
    "social": ("data-pd-canvas", "data-pd-social"),
    "youtube": ("data-pd-youtube-canvas", "data-pd-youtube"),
    "deck": ("data-pd-deck-canvas", "data-pd-deck"),
    "subtitle": ("data-pd-subtitle-frame", "data-pd-subtitle"),
}

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
RELEASE = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["version"]
check(meta.get("version") == RELEASE, f"version is {RELEASE}")
check(meta.get("displayVersion") == RELEASE.split(".")[0], "display version is the major version")
check(meta.get("status") == "production", "canonical token state is production")
check(
    meta.get("fontSource") == "FontBlind-Final-2026-08-28-v13.zip",
    "FontBlind v13 font authority recorded",
)

for split_name in [
    "pitchdog.typography.tokens.json",
    "pitchdog.ui.tokens.json",
    "pitchdog.social.tokens.json",
    "pitchdog.youtube.tokens.json",
    "pitchdog.deck.tokens.json",
    "pitchdog.subtitle.tokens.json",
]:
    split_meta = (load_json(ROOT / "tokens" / split_name) or {}).get("meta", {})
    check(split_meta.get("version") == meta.get("version"), f"{split_name} carries the canonical version")
    check(split_meta.get("status") == meta.get("status"), f"{split_name} carries the canonical release state")

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

for group in ["ui", "social", "youtube", "deck", "subtitle"]:
    exported = (dtcg.get("type") or {}).get(group) or {}
    canonical = tokens.get(group, {}).get("roles", {})
    prefix = f"{group}."
    check(
        {f"{prefix}{name}": value for name, value in exported.items()}
        == {
            name: {
                "$type": "typography",
                "$value": {
                    "fontFamily": f"{{font.family.{role['family']}}}",
                    "fontSize": role["size"],
                    "fontWeight": role["weight"],
                    "letterSpacing": role["tracking"],
                    "lineHeight": role["lineHeight"],
                },
                "$extensions": {
                    "pitchdog": {
                        key: value
                        for key, value in role.items()
                        if key not in {"family", "size", "weight", "tracking", "lineHeight"}
                    }
                },
            }
            for name, role in canonical.items()
        },
        f"DTCG {group} role values match the canonical source",
    )


def kebab(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", name).lower()


for group, expected_count in EXPECTED_CANVASES.items():
    canvases = tokens.get(group, {}).get("canvases", {})
    check(len(canvases) == expected_count, f"{group} has {expected_count} canonical canvases")
    canvas_attr, role_attr = MEDIA_ATTRIBUTES[group]
    media_css = (ROOT / "dist" / f"pitchdog-{group}.css").read_text(encoding="utf-8")
    for key in canvases:
        check(f'[{canvas_attr}="{kebab(key)}"]' in media_css, f"{group} CSS sizes the {key} canvas")
    roles = tokens.get(group, {}).get("roles", {})
    governed = {name.split(".", 1)[1] for name in roles}
    for name in sorted(governed):
        check(f'[{role_attr}="{name}"]' in media_css, f"{group} CSS implements {group}.{name}")
    for starter in sorted((ROOT / group).glob("*.html")):
        used = set(re.findall(rf'{role_attr}="([^"]+)"', starter.read_text(encoding="utf-8")))
        check(
            bool(used) and used <= governed,
            f"{starter.relative_to(ROOT).as_posix()} uses only governed {group} roles: {sorted(used - governed)}",
        )


def slide_size(size: str) -> tuple[float, float]:
    """Return the (cqi, cqb) pair of a deck size such as `min(1.68cqi, 2.8cqb)`."""
    match = re.fullmatch(r"min\(([\d.]+)cqi, ([\d.]+)cqb\)", size)
    return (float(match.group(1)), float(match.group(2))) if match else (-1.0, -1.0)


def cqb_value(length: str) -> float:
    match = re.fullmatch(r"([\d.]+)cqb", length)
    return float(match.group(1)) if match else -1.0


deck = tokens.get("deck", {})
deck_roles = deck.get("roles", {})
floor = deck.get("floor", {})
present_floor = cqb_value(floor.get("present", ""))
read_floor = cqb_value(floor.get("read", ""))
check(present_floor > 0 and 0 < read_floor <= present_floor, "deck publishes present and read size floors")
check(set(deck.get("densities", {})) == {"present", "read"}, "deck densities are present and read")
for name, role in deck_roles.items():
    cqi, cqb = slide_size(role.get("size", ""))
    check(cqb > 0, f"{name} size is a cqi/cqb pair")
    minimum = read_floor if name in floor.get("exceptions", []) else present_floor
    check(cqb >= minimum, f"{name} meets its size floor")
    check(abs(cqi - round(cqb * 0.6, 2)) < 1e-9, f"{name} sets 4:3 slides at 80 percent of widescreen")
    read = role.get("read")
    if read:
        read_cqi, read_cqb = slide_size(read.get("size", ""))
        check(read_floor <= read_cqb < cqb, f"{name} read density is smaller and above the read floor")
        check(abs(read_cqi - round(read_cqb * 0.6, 2)) < 1e-9, f"{name} read size keeps the 4:3 ratio")
        check(
            all(read.get(key, role.get(key, 0)) >= role.get(key, 0) for key in ("maxLines", "maxWords", "maxItems")),
            f"{name} read density allows at least the present copy",
        )
for name, template in deck.get("templates", {}).items():
    check(bool(template.get("roles")) and set(template["roles"]) <= set(deck_roles), f"deck template {name} uses governed roles")
deck_css = (ROOT / "dist" / "pitchdog-deck.css").read_text(encoding="utf-8")
for marker in [
    '[data-pd-deck-density="read"]',
    "[data-pd-deck-safe]",
    "@page pd-deck-widescreen { size:1920px 1080px; margin:0; }",
    "@page pd-deck-standard { size:1440px 1080px; margin:0; }",
    "break-after:page",
]:
    check(marker in deck_css, f"deck CSS contains {marker}")
system_css = (ROOT / "dist" / "pitchdog-system.css").read_text(encoding="utf-8")
check(deck_css in system_css, "system CSS bundles the deck layer")
deck_spacing = {step: value for step, value in deck.get("spacing", {}).items() if step != "note"}
check(list(deck_spacing) == ["2xs", "xs", "s", "m", "l"], "deck publishes five spacing steps")
previous = 0.0
for step, value in deck_spacing.items():
    cqi, cqb = slide_size(value)
    check(cqb > previous and abs(cqi - round(cqb * 0.6, 2)) < 1e-9, f"deck spacing {step} grows and keeps the 4:3 ratio")
    previous = cqb
    check(f"--pd-deck-space-{step}:{value}" in deck_css, f"deck CSS declares --pd-deck-space-{step}")

# Web flow spacing: the hand-authored CSS must restate the scale and the before/after contract exactly.
typography_css = (ROOT / "dist" / "pitchdog-typography.css").read_text(encoding="utf-8")
web_spacing = tokens.get("web", {}).get("spacing", {})
for step, value in web_spacing.get("scale", {}).items():
    check(f"--pd-space-{step}: {value};" in typography_css, f"typography CSS declares --pd-space-{step}")
MEDIA_SELECTOR = ":is(figure, img, picture, video, table, pre, hr)"
css_flow: dict[str, dict[str, str]] = {"before": {}, "after": {}}
for rule in re.findall(r":where\(\[data-pd-flow\]\) > :where\((.+?)\) \{ margin-block-start: var\(--pd-space-([\w]+)\); \}", typography_css):
    selector, step = rule
    side = "before" if selector.startswith("* + ") else "after"
    names = re.findall(r'data-pd-type="([^"]+)"', selector)
    if MEDIA_SELECTOR in selector:
        names.append("media")
    for name in names:
        css_flow[side][name] = step
flow = web_spacing.get("flow", {})
check(flow.get("text") == "1em" and "var(--pd-flow-space, 1em)" in typography_css, "flow sets text after text at 1em")
for side in ("before", "after"):
    check(css_flow[side] == flow.get(side), f"typography CSS flow spacing {side} headings matches the tokens")
scale_order = list(web_spacing.get("scale", {}))
for name, step in flow.get("before", {}).items():
    after = flow.get("after", {}).get(name)
    if after and name != "media":
        check(scale_order.index(step) > scale_order.index(after), f"flow puts more space before {name} than after it")

def srgb_channel(value: float) -> float:
    value /= 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[float, float, float]) -> float:
    red, green, blue = (srgb_channel(channel) for channel in rgb)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(first: tuple[float, float, float], second: tuple[float, float, float]) -> float:
    lighter, darker = sorted((luminance(first), luminance(second)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def hex_rgb(value: str) -> tuple[float, float, float]:
    match = re.fullmatch(r"#([0-9A-Fa-f]{6})", value)
    return tuple(float(int(match.group(1)[i : i + 2], 16)) for i in (0, 2, 4)) if match else (-1.0, -1.0, -1.0)


def black_box_opacity(value: str) -> float:
    match = re.fullmatch(r"rgb\(0 0 0 / ([\d.]+)\)", value)
    return float(match.group(1)) if match else -1.0


# Subtitles: BBC Subtitle Guidelines 9.2.1 line heights and 3.1 line lengths; Netflix line and character limits.
subtitle = tokens.get("subtitle", {})
subtitle_roles = subtitle.get("roles", {})
for key, canvas in subtitle.get("canvases", {}).items():
    width, height = canvas.get("width", 0), canvas.get("height", 0)
    vertical = height > width
    low, high = (3.9, 4.5) if vertical else (7.0, 8.0)
    for name in ("subtitle.line", "subtitle.italic"):
        role = subtitle_roles.get(name, {})
        cqi, cqb = slide_size(role.get("size", ""))
        line_px = min(cqi * width, cqb * height) / 100 * role.get("lineHeight", 0)
        percent = line_px / height * 100 if height else 0
        check(low <= percent <= high, f"{name} line height on the {key} frame is {low}-{high} % of frame height ({percent:.2f})")
    cue = canvas.get("cue", {})
    width_limit = 68.0 if canvas.get("ratio") == "16 / 9" else 90.0
    max_width = re.fullmatch(r"([\d.]+)cqi", cue.get("maxWidth", ""))
    check(bool(max_width) and float(max_width.group(1)) <= width_limit, f"subtitle {key} cue is at most {width_limit:g} % of frame width")
    check(cqb_value(cue.get("bottom", "")) > 0, f"subtitle {key} cue sits above the frame edge")
    check(0 < cue.get("maxChars", 0) <= 42, f"subtitle {key} cue publishes a characters-per-line limit of at most 42")
for name, role in subtitle_roles.items():
    check(role.get("maxLines", 0) <= 2, f"{name} holds at most two lines")
    check(0 < role.get("maxChars", 0) <= 42, f"{name} holds at most 42 characters per line")
    check(role.get("family") in {"body", "bodyAlt"}, f"{name} uses a Body voice")
white, black = (255.0, 255.0, 255.0), (0.0, 0.0, 0.0)
for name, style in subtitle.get("styles", {}).items():
    ink = hex_rgb(style.get("ink", ""))
    check(ink[0] >= 0, f"subtitle style {name} ink is a hex colour")
    if style.get("box") == "transparent":
        check(style.get("outline", "none") != "none", f"subtitle style {name} without a box carries an outline")
        continue
    opacity = black_box_opacity(style.get("box", ""))
    check(0 < opacity <= 1, f"subtitle style {name} box is translucent black")
    worst = min(contrast(ink, tuple(channel * (1 - opacity) for channel in backdrop)) for backdrop in (white, black))
    check(worst >= 4.5, f"subtitle style {name} keeps 4.5:1 over a white or black picture ({worst:.2f}:1)")
subtitle_css = (ROOT / "dist" / "pitchdog-subtitle.css").read_text(encoding="utf-8")
for marker in ["[data-pd-subtitle-cue]", "inline-size:fit-content", "::cue", '[data-pd-subtitle-style="cinema"]']:
    check(marker in subtitle_css, f"subtitle CSS contains {marker}")
check(subtitle_css in system_css, "system CSS bundles the subtitle layer")

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

html_path = ROOT / "pitchdog-typography-system.html"
html = html_path.read_text(encoding="utf-8")
baker = html  # the specimen is also the local standalone builder
check(not (ROOT / "MAKE-STANDALONE-v13.html").exists(), "no duplicate standalone-builder copy")
runtime_records = load_json(ROOT / "dist" / "pitchdog-font-runtime.json") or []
expected_match = re.search(r"const EXPECTED=(\[.*?\]);", html)
html_expected = json.loads(expected_match.group(1)) if expected_match else []
check(
    {record["key"]: (record["bytes"], record["sha256"]) for record in html_expected}
    == {record["key"]: (record["bytes"], record["sha256"]) for record in runtime_records},
    "specimen loader verifies the shipped runtime font hashes",
)
check(f'data-pd-version="{RELEASE.split(".")[0]}"' in html, "specimen carries the display version")
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
    manifest.get("start_url") == "./pitchdog-typography-system.html",
    "web manifest points to the specimen HTML",
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
    if relative.parts and relative.parts[0] == "pitchdog-font-handoff":
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
    "DECKS.md",
    "SUBTITLES.md",
    "SPACING.md",
    "ARROWS.md",
    "ACCESSIBILITY-QA.md",
    "IMPLEMENTATION.md",
    "GOVERNANCE.md",
    "FONT-NAMING.md",
    "MIGRATION-v13-to-v2.md",
    "VALIDATION-REPORT.md",
    "WEB-TEXT-WRAPPING.md",
]
for name in required_docs:
    check((ROOT / "docs" / name).exists(), f"documentation exists: {name}")

wrap_contracts = load_json(ROOT / "dist" / "pitchdog-wrap-contracts.json") or {}
check(wrap_contracts.get("version") == RELEASE, "wrap contracts carry the release version")
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
