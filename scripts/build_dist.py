#!/usr/bin/env python3
"""Generate every derived type-system file from the canonical tokens, or check they are current.

`tokens/pitchdog.system.tokens.json` is the only hand-edited source for semantic roles,
canvases and templates. This script writes everything that restates it:

- split token files and the DTCG export in `tokens/`
- role contracts, TypeScript types and the media-layer CSS in `dist/`
- canvas, copy and template contracts in `social/`, `youtube/` and `deck/`
- the Figma style map in `docs/`
- `dist/pitchdog-system.css`, `dist/pitchdog-system.min.css` and the copy inlined in the specimen

The web and UI layers (`dist/pitchdog-typography.css`, `dist/pitchdog-ui.css`) and the
font registration template stay hand-authored; they are assembled here, not generated.

The minified bundle is made with esbuild 0.28.2. Set `PD_ESBUILD` to a local binary, or
the script runs `npx --yes esbuild@0.28.2`.

Usage:
    python3 scripts/build_dist.py            # write
    python3 scripts/build_dist.py --check    # fail if any derived file is stale
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKENS = ROOT / "tokens" / "pitchdog.system.tokens.json"
ESBUILD_VERSION = "0.28.2"
ROLE_GROUPS = ["web", "ui", "social", "youtube", "deck"]

# Media layers generated from tokens. Attribute names are part of the public API.
MEDIA = {
    "social": {"css": "pitchdog-social.css", "canvas": "data-pd-canvas", "role": "data-pd-social"},
    "youtube": {"css": "pitchdog-youtube.css", "canvas": "data-pd-youtube-canvas", "role": "data-pd-youtube"},
    "deck": {"css": "pitchdog-deck.css", "canvas": "data-pd-deck-canvas", "role": "data-pd-deck"},
}
SYSTEM_PARTS = [
    "pitchdog-fonts.template.css",
    "pitchdog-typography.css",
    "pitchdog-ui.css",
    "pitchdog-social.css",
    "pitchdog-youtube.css",
    "pitchdog-deck.css",
]
SPECIMEN = "pitchdog-typography-system.html"
SPECIMEN_OPEN = '<style id="pd-system-css">'
FAMILY_VARS = {
    "head": "--pd-font-head-active",
    "headAlt": "--pd-font-head-alt",
    "body": "--pd-font-body",
    "bodyAlt": "--pd-font-body-alt",
    "eyebrow": "--pd-font-eyebrow",
}
FIGMA_SURFACES = {"web": "Web", "ui": "UI", "social": "Social", "youtube": "YouTube", "deck": "Deck"}
FIGMA_WORDS = {"ui": "UI", "youtube": "YouTube"}
DTCG_VALUE_KEYS = {"family", "size", "weight", "tracking", "lineHeight"}


def as_json(value) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def kebab(name: str) -> str:
    return re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", name).lower()


def short_name(group: str, role_name: str) -> str:
    prefix = f"{group}."
    return role_name[len(prefix):] if role_name.startswith(prefix) else role_name


# ---------------------------------------------------------------- media CSS

def declarations(role: dict) -> str:
    family = role["family"]
    weight = role["weight"]
    parts = [f"font-family:var({FAMILY_VARS[family]})", f"font-weight:{weight}"]
    if family in {"head", "headAlt"}:
        parts += ["font-style:normal", f'font-variation-settings:"wght" {weight},"ital" {role.get("ital", 0)}']
    elif family == "eyebrow":
        width = role.get("width", 87.5)
        parts += [
            "font-style:normal",
            f"font-stretch:{width:g}%",
            f'font-variation-settings:"wght" {weight},"wdth" {width:g},"ital" {role.get("ital", 0)}',
            "font-variant-ligatures:none",
        ]
    else:
        parts.append(f"font-style:{role.get('style', 'normal')}")
    parts += [
        f"font-size:{role['size']}",
        f"line-height:{role['lineHeight']!r}",
        f"letter-spacing:{role['tracking']}",
    ]
    return ";".join(parts) + ";"


def role_selector(attr: str, name: str) -> str:
    return f'[{attr}="{name}"]'


def media_css(group: str, section: dict) -> str:
    config = MEDIA[group]
    canvas_attr, role_attr = config["canvas"], config["role"]
    canvases = section["canvases"]
    roles = {short_name(group, name): role for name, role in section["roles"].items()}
    deck = group == "deck"

    lines = ["@layer pd.media {"]
    base = "container-type:size; position:relative; overflow:hidden;"
    if deck:
        base += " box-sizing:border-box;"
    lines.append(f"  :where([{canvas_attr}]) {{ {base} }}")
    for key, canvas in canvases.items():
        ratio = canvas["ratio"].replace(" ", "")
        lines.append(f'  :where([{canvas_attr}="{kebab(key)}"]) {{ aspect-ratio:{ratio}; }}')
    if deck:
        # Safe areas are published as insets relative to the slide itself.
        lines.append("  :where([data-pd-deck-safe]) { position:absolute; }")
        for key, canvas in canvases.items():
            safe = canvas["safe"]
            inset = " ".join(
                f"{safe[side] / canvas[axis] * 100:.3f}".rstrip("0").rstrip(".") + unit
                for side, axis, unit in [
                    ("top", "height", "cqb"),
                    ("right", "width", "cqi"),
                    ("bottom", "height", "cqb"),
                    ("left", "width", "cqi"),
                ]
            )
            lines.append(f'  :where([{canvas_attr}="{kebab(key)}"] > [data-pd-deck-safe]) {{ inset:{inset}; }}')
    for name, role in roles.items():
        lines.append(f":where({role_selector(role_attr, name)}){{{declarations(role)}}}")
    for name, role in roles.items():
        if role["family"] in {"head", "headAlt"} and role.get("ital") == 1:
            lines.append(f"  :where({role_selector(role_attr, name)}) {{ --pd-ital:1; }}")
        if role.get("case") == "upper":
            lines.append(f"  :where({role_selector(role_attr, name)}) {{ text-transform:uppercase; }}")
    for wrap in ("balance", "pretty"):
        names = [name for name, role in roles.items() if role.get("wrap") == wrap]
        if names:
            selectors = ",".join(role_selector(role_attr, name) for name in names)
            lines.append(f"  :where({selectors}) {{ text-wrap:{wrap}; }}")
    if deck:
        for name, role in roles.items():
            read = role.get("read")
            if not read:
                continue
            selector = f'[data-pd-deck-density="read"] {role_selector(role_attr, name)}'
            same = f'[data-pd-deck-density="read"]{role_selector(role_attr, name)}'
            body = f"font-size:{read['size']};"
            if "lineHeight" in read:
                body += f"line-height:{read['lineHeight']!r};"
            lines.append(f"  :where({selector},{same}) {{ {body} }}")
        lines.append("  @media print {")
        lines.append(f"    :where([{canvas_attr}]) {{ inline-size:100%; margin:0; break-after:page; break-inside:avoid; }}")
        for key in canvases:
            # Chromium ignores `page` on size-contained boxes, so the slide's parent names the page too.
            selector = f'[{canvas_attr}="{kebab(key)}"]'
            lines.append(f"    :where({selector},:has(> {selector})) {{ page:pd-deck-{kebab(key)}; }}")
        lines.append("  }")
    lines.append("}")
    if deck:
        for key, canvas in canvases.items():
            lines.append(f"@page pd-deck-{kebab(key)} {{ size:{canvas['width']}px {canvas['height']}px; margin:0; }}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- JSON surfaces

def split_tokens(tokens: dict) -> dict[str, str]:
    meta = tokens["meta"]
    web = tokens["web"]
    typography = {
        "meta": meta,
        "families": tokens["families"],
        "anchors": tokens["anchors"],
        "contexts": tokens["contexts"],
        "tones": tokens["tones"],
        "measures": {name: measure["value"] for name, measure in web["measures"].items()},
        "wrapStyles": list(web["wrapStyles"]),
        "roles": web["roles"],
    }
    files = {"tokens/pitchdog.typography.tokens.json": as_json(typography)}
    for group in ["ui", "social", "youtube", "deck"]:
        files[f"tokens/pitchdog.{group}.tokens.json"] = as_json({"meta": meta, **tokens[group]})
    files["tokens/pitchdog.arrows.tokens.json"] = as_json(tokens["arrows"])
    return files


def dtcg_role(role: dict) -> dict:
    return {
        "$type": "typography",
        "$value": {
            "fontFamily": f"{{font.family.{role['family']}}}",
            "fontSize": role["size"],
            "fontWeight": role["weight"],
            "letterSpacing": role["tracking"],
            "lineHeight": role["lineHeight"],
        },
        "$extensions": {"pitchdog": {key: value for key, value in role.items() if key not in DTCG_VALUE_KEYS}},
    }


def dtcg(tokens: dict) -> str:
    anchors = tokens["anchors"]
    font = {
        "family": {key: {"$type": "fontFamily", "$value": name} for key, name in tokens["families"].items()},
        "weight": {
            family: {str(weight): {"$type": "fontWeight", "$value": weight} for weight in anchors[family]["wght"]}
            for family in ["head", "body", "eyebrow"]
        },
    }
    types: dict = {}
    for group in ROLE_GROUPS:
        tree: dict = {}
        for name, role in tokens[group]["roles"].items():
            parts = short_name(group, name).split(".")
            node = tree
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = dtcg_role(role)
        types[group] = tree
    document = {
        "font": font,
        "type": types,
        "$extensions": {
            "pitchdog": {
                "version": tokens["meta"]["version"],
                "anchorPolicy": "Only listed master anchors are valid production values.",
            }
        },
    }
    return as_json(document)


def media_contracts(tokens: dict) -> dict[str, str]:
    files: dict[str, str] = {}
    for group in MEDIA:
        section = tokens[group]
        files[f"{group}/canvas-contracts.json"] = as_json(section["canvases"])
        copy = {}
        for name, role in section["roles"].items():
            contract = {"maxLines": role["maxLines"], "maxWords": role["maxWords"]}
            for key in ("maxItems",):
                if key in role:
                    contract[key] = role[key]
            read = {key: value for key, value in role.get("read", {}).items() if key.startswith("max")}
            if read:
                contract["read"] = read
            copy[name] = contract
        files[f"{group}/copy-contracts.json"] = as_json(copy)
        if "templates" in section:
            files[f"{group}/templates.json"] = as_json(section["templates"])
    return files


def typescript(tokens: dict) -> str:
    anchors = tokens["anchors"]
    measures = tokens["web"]["measures"]

    def numbers(values) -> str:
        return ", ".join(f"{value:g}" if isinstance(value, float) else str(value) for value in values)

    def union(names) -> str:
        return " | ".join(f'"{name}"' for name in names)

    lines = [
        f'export const VERSION = "{tokens["meta"]["version"]}" as const;',
        f"export const HEAD_WEIGHTS = [{numbers(anchors['head']['wght'])}] as const;",
        f"export const BODY_WEIGHTS = [{numbers(anchors['body']['wght'])}] as const;",
        f"export const EYEBROW_WEIGHTS = [{numbers(anchors['eyebrow']['wght'])}] as const;",
        f"export const EYEBROW_WIDTHS = [{numbers(anchors['eyebrow']['wdth'])}] as const;",
        f"export const ARROWS = [{union(tokens['arrows']['glyphs'])}] as const;".replace(" | ", ", "),
        "export const WEB_MEASURES = {",
        *[f'  {name}: "{measure["value"]}",' for name, measure in measures.items()],
        "} as const;",
        f"export const WEB_WRAP_STYLES = [{union(tokens['web']['wrapStyles'])}] as const;".replace(" | ", ", "),
        f"export const DECK_CANVASES = [{union(kebab(key) for key in tokens['deck']['canvases'])}] as const;".replace(" | ", ", "),
        f"export const DECK_DENSITIES = [{union(tokens['deck']['densities'])}] as const;".replace(" | ", ", "),
        "",
        "export type HeadWeight = typeof HEAD_WEIGHTS[number];",
        "export type BodyWeight = typeof BODY_WEIGHTS[number];",
        "export type EyebrowWeight = typeof EYEBROW_WEIGHTS[number];",
        "export type EyebrowWidth = typeof EYEBROW_WIDTHS[number];",
        "export type WebMeasure = keyof typeof WEB_MEASURES;",
        "export type WebWrapStyle = typeof WEB_WRAP_STYLES[number];",
        "export type DeckCanvas = typeof DECK_CANVASES[number];",
        "export type DeckDensity = typeof DECK_DENSITIES[number];",
        f"export type WebRole = {union(tokens['web']['roles'])};",
        f"export type UiRole = {union(tokens['ui']['roles'])};",
        f"export type SocialRole = {union(tokens['social']['roles'])};",
        f"export type YouTubeRole = {union(tokens['youtube']['roles'])};",
        f"export type DeckRole = {union(tokens['deck']['roles'])};",
        "",
        "export function isHeadWeight(value: number): value is HeadWeight { return (HEAD_WEIGHTS as readonly number[]).includes(value); }",
        "export function isBodyWeight(value: number): value is BodyWeight { return (BODY_WEIGHTS as readonly number[]).includes(value); }",
        "export function isEyebrowWeight(value: number): value is EyebrowWeight { return (EYEBROW_WEIGHTS as readonly number[]).includes(value); }",
        "export function isEyebrowWidth(value: number): value is EyebrowWidth { return (EYEBROW_WIDTHS as readonly number[]).includes(value); }",
    ]
    return "\n".join(lines) + "\n"


def figma_name(group: str, role_name: str) -> str:
    words = []
    for part in role_name.split("."):
        spaced = re.sub(r"(?<=[a-z0-9])([A-Z])", r" \1", part)
        words.append(" ".join(FIGMA_WORDS.get(word.lower(), word[:1].upper() + word[1:]) for word in spaced.split()))
    return " / ".join(words)


def csv_cell(value) -> str:
    text = "" if value is None else str(value)
    return f'"{text}"' if "," in text or '"' in text else text


def figma_map(tokens: dict) -> str:
    header = "Surface,Figma style,Token role,Family,Weight,Italic/Style,Width,Size policy,Line height,Tracking"
    rows = [header]

    def row(group: str, style: str, name: str, role: dict, size: str, line_height) -> str:
        family = role["family"]
        posture = role.get("ital", 0) if family in {"head", "headAlt", "eyebrow"} else role.get("style", "normal")
        width = role.get("width", 87.5) if family == "eyebrow" else ""
        return ",".join(
            csv_cell(value)
            for value in [FIGMA_SURFACES[group], style, name, family, role["weight"], posture, width, size, repr(line_height), role["tracking"]]
        )

    for group in ROLE_GROUPS:
        for name, role in tokens[group]["roles"].items():
            rows.append(row(group, figma_name(group, name), name, role, role["size"], role["lineHeight"]))
        for name, role in tokens[group]["roles"].items():
            read = role.get("read")
            if read:
                style = figma_name(group, name).replace("Deck / ", "Deck / Read / ", 1)
                rows.append(row(group, style, name, role, read["size"], read.get("lineHeight", role["lineHeight"])))
    # RFC 4180 line endings, as spreadsheet and Figma importers expect.
    return "\r\n".join(rows) + "\r\n"


# ---------------------------------------------------------------- CSS bundle

def esbuild_command() -> list[str]:
    local = os.environ.get("PD_ESBUILD")
    if local:
        return [local]
    npx = shutil.which("npx")
    if not npx:
        raise SystemExit("ERROR: esbuild is required for the minified bundle; set PD_ESBUILD or install Node.js")
    return [npx, "--yes", f"esbuild@{ESBUILD_VERSION}"]


def minify(css: str) -> str:
    command = esbuild_command()
    version = subprocess.run(command + ["--version"], capture_output=True, text=True, check=True).stdout.strip()
    if version != ESBUILD_VERSION:
        raise SystemExit(f"ERROR: esbuild {ESBUILD_VERSION} is required, found {version}")
    result = subprocess.run(command + ["--loader=css", "--minify"], input=css, capture_output=True, text=True, check=True)
    return result.stdout


def build(tokens: dict) -> dict[str, str]:
    files: dict[str, str] = {}
    for group, config in MEDIA.items():
        files[f"dist/{config['css']}"] = media_css(group, tokens[group])
    files.update(split_tokens(tokens))
    files["tokens/pitchdog.system.dtcg.json"] = dtcg(tokens)
    files["dist/pitchdog-role-contracts.json"] = as_json({group: tokens[group]["roles"] for group in ROLE_GROUPS})
    files["dist/pitchdog-system.ts"] = typescript(tokens)
    files.update(media_contracts(tokens))
    files["docs/figma-style-map.csv"] = figma_map(tokens)

    def text(name: str) -> str:
        key = f"dist/{name}"
        return files[key] if key in files else (ROOT / key).read_bytes().decode("utf-8")

    system = "\n".join(text(name) for name in SYSTEM_PARTS)
    files["dist/pitchdog-system.css"] = system
    files["dist/pitchdog-system.min.css"] = minify(system)

    # The specimen inlines the system CSS (fonts come from a separate link) so the
    # standalone file it builds works offline. Keep that copy identical to dist.
    specimen = (ROOT / SPECIMEN).read_bytes().decode("utf-8")
    start = specimen.index(SPECIMEN_OPEN) + len(SPECIMEN_OPEN)
    end = specimen.index("</style>", start)
    inline = "\n".join(text(name) for name in SYSTEM_PARTS[1:]).rstrip("\n")
    files[SPECIMEN] = specimen[:start] + inline + specimen[end:]
    return files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report stale derived files; change nothing")
    args = parser.parse_args()
    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    files = build(tokens)
    stale = [
        path
        for path, content in files.items()
        if not (ROOT / path).is_file() or (ROOT / path).read_bytes() != content.encode("utf-8")
    ]
    if args.check:
        for path in stale:
            print(f"stale: {path}")
        print(f"Derived files checked: {len(files)} files, {len(stale)} stale")
        if stale:
            print("Run `python3 scripts/build_dist.py` and commit the result.")
        return 1 if stale else 0
    for path in stale:
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(files[path].encode("utf-8"))
    print(f"Derived files built: {len(files)} files, {len(stale)} updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
