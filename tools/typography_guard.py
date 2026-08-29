#!/usr/bin/env python3
"""Reject ungoverned typography declarations in authored component CSS.

Generated system CSS intentionally contains raw declarations and should not be
passed to this tool. Scan application/component source directories instead.
Use an inline `pd-type-exception:` comment only for a documented exception.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PROPERTIES = (
    "font-family",
    "font-size",
    "font-weight",
    "font-style",
    "line-height",
    "letter-spacing",
    "font-variation-settings",
    "font-feature-settings",
    "font-stretch",
)
EXCEPTION_MARKER = "pd-type-exception:"


def iter_css(path: Path):
    if path.is_file() and path.suffix.lower() == ".css":
        yield path
    elif path.is_dir():
        yield from path.rglob("*.css")


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: typography_guard.py <file-or-directory> [...]", file=sys.stderr)
        return 2

    errors: list[str] = []
    pattern = re.compile(
        r"\b(?:" + "|".join(re.escape(prop) for prop in PROPERTIES) + r")\s*:"
    )

    for raw in argv:
        path = Path(raw)
        if not path.exists():
            errors.append(f"{path}: path does not exist")
            continue
        for css_file in iter_css(path):
            for line_number, line in enumerate(
                css_file.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
            ):
                if pattern.search(line) and EXCEPTION_MARKER not in line:
                    errors.append(
                        f"{css_file}:{line_number}: ungoverned typography declaration"
                    )

    if errors:
        print("\n".join(errors))
        return 1

    print("Typography guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
