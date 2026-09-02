#!/usr/bin/env python3
"""Verify the canonical pitch.dog type-system repository as a consumable release."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "13.1.1"
FONT_SUFFIXES = {".woff2", ".woff", ".ttf", ".otf", ".ttc"}
SKILL_ROOT = ROOT / "skills" / "pitchdog-type-system"
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
    check(package.get("version") == EXPECTED_VERSION, f"package version is {EXPECTED_VERSION}")
    check(package.get("private") is True, "package cannot be published accidentally")
    check(
        package.get("repository", {}).get("url") == "https://github.com/bomkino/pitchdog-type-system.git",
        "package repository URL is canonical HTTPS",
    )
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

    canonical = json.loads((ROOT / "tokens" / "pitchdog.system.tokens.json").read_text(encoding="utf-8"))
    dtcg = json.loads((ROOT / "tokens" / "pitchdog.system.dtcg.json").read_text(encoding="utf-8"))
    provenance = json.loads((ROOT / "FONT-PROVENANCE.json").read_text(encoding="utf-8"))
    wrap_contract = json.loads((ROOT / "dist" / "pitchdog-wrap-contracts.json").read_text(encoding="utf-8"))
    check(canonical.get("meta", {}).get("version") == EXPECTED_VERSION, "canonical tokens match package version")
    check(canonical.get("meta", {}).get("status") == "production", "canonical tokens declare production")
    check(
        dtcg.get("$extensions", {}).get("pitchdog", {}).get("version") == EXPECTED_VERSION,
        "DTCG export matches package version",
    )
    check(provenance.get("release") == EXPECTED_VERSION, "font provenance matches package version")
    check(wrap_contract.get("version") == EXPECTED_VERSION, "wrap contract matches package version")
    check(
        (ROOT / "dist" / "pitchdog-system.ts").read_text(encoding="utf-8").startswith(
            f'export const VERSION = "{EXPECTED_VERSION}" as const;'
        ),
        "TypeScript export matches package version",
    )
    check(f"Current release: **v{EXPECTED_VERSION}**" in (ROOT / "README.md").read_text(encoding="utf-8"), "README matches package version")
    receipt = (ROOT / "RELEASE-RECEIPT.md").read_text(encoding="utf-8")
    check(f"Package version: **{EXPECTED_VERSION}**" in receipt, "release receipt matches package version")
    check("State: **production release**" in receipt, "release receipt declares production")


def validate_agent_skill() -> None:
    required = {
        SKILL_ROOT / "SKILL.md",
        SKILL_ROOT / "NOTICE.md",
        SKILL_ROOT / "agents" / "openai.yaml",
        SKILL_ROOT / "references" / "task-routing.md",
        SKILL_ROOT / "references" / "version-and-migration.md",
        SKILL_ROOT / "references" / "runtime-verification.md",
    }
    check(all(path.is_file() for path in required), "Codex skill structure is complete")
    if not all(path.is_file() for path in required):
        return

    actual = {path for path in SKILL_ROOT.rglob("*") if path.is_file()}
    check(actual == required, "Codex skill contains only its declared lean file set")
    check(not any(path.is_symlink() for path in SKILL_ROOT.rglob("*")), "Codex skill contains no symlinks")

    entrypoint = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
    lines = entrypoint.splitlines()
    closing = lines.index("---", 1) if len(lines) > 1 and "---" in lines[1:] else -1
    frontmatter: dict[str, str] = {}
    frontmatter_valid = bool(lines and lines[0] == "---" and closing > 1)
    if frontmatter_valid:
        for line in lines[1:closing]:
            match = re.fullmatch(r"([a-z][a-z0-9_-]*): (.+)", line)
            if not match or match.group(1) in frontmatter:
                frontmatter_valid = False
                break
            frontmatter[match.group(1)] = match.group(2)
    check(frontmatter_valid and set(frontmatter) == {"name", "description"}, "Codex skill frontmatter is a flat name and description")
    check(frontmatter.get("name") == "pitchdog-type-system", "Codex skill name is canonical")
    description = frontmatter.get("description", "")
    check("Always invoke for any type work" in description, "Codex skill carries the universal type-work trigger")
    check("TODO" not in entrypoint and "TODO" not in metadata, "Codex skill has no scaffold placeholders")
    local_links: list[tuple[Path, str]] = []
    for document in sorted(SKILL_ROOT.rglob("*.md")):
        for pointer in re.findall(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)", document.read_text(encoding="utf-8")):
            if "://" not in pointer:
                local_links.append((document, pointer))
    check(
        bool(local_links) and all((document.parent / pointer).resolve().is_file() for document, pointer in local_links),
        "Codex skill local Markdown references resolve",
    )

    metadata_lines = metadata.splitlines()
    interface: dict[str, str] = {}
    metadata_valid = bool(metadata_lines and metadata_lines[0] == "interface:")
    if metadata_valid:
        for line in metadata_lines[1:]:
            match = re.fullmatch(r'  ([a-z][a-z0-9_]*): "([^"]*)"', line)
            if not match or match.group(1) in interface:
                metadata_valid = False
                break
            interface[match.group(1)] = match.group(2)
    check(
        metadata_valid and set(interface) == {"display_name", "short_description", "default_prompt"},
        "Codex skill interface metadata is structurally valid",
    )
    check(25 <= len(interface.get("short_description", "")) <= 64, "Codex skill short description length is valid")
    check(interface.get("default_prompt", "").startswith("Use $pitchdog-type-system"), "Codex skill default prompt starts with its invocation")
    check("$pitchdog-type-system" in interface.get("default_prompt", ""), "Codex skill metadata invokes the canonical skill name")

    duplicated_assets = [
        path.relative_to(SKILL_ROOT).as_posix()
        for path in SKILL_ROOT.rglob("*")
        if path.is_file() and (path.suffix.lower() in FONT_SUFFIXES or path.suffix.lower() in {".css", ".json"})
    ]
    check(not duplicated_assets, f"Codex skill contains no duplicated fonts, CSS, or token data: {duplicated_assets}")


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
    validate_agent_skill()
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
