# Changelog

## 2.0.0

Numbering restarts at 2.0.0 after 13.1.1. Pin by tag; version-sorting tools will still list 13.x higher.

**Fonts install under their real names.** Every font file now carries the family names the CSS already used: PD Head, PD Head Alt, PD Body, PD Body Alt and PD Eyebrow.

- PD Eyebrow no longer installs as `Untitled`.
- Eyebrow's 350 and 400 static anchors no longer share one name (`PDEyebrow-Book` and `PDEyebrow-Regular`).
- PD Body Italic is labelled Italic, and Roman and Italic files of PD Body and PD Body Alt pair as one family.
- Static fallbacks follow the standard Regular/Italic/Bold/Bold Italic linking; every face has a unique PostScript name.
- Glyphs, metrics, axes, anchors, kerning and every semantic role are unchanged. `tools/compare_font_payloads.py` proves this for all 145 files, and all nine specimen views render pixel-identical to 13.1.1 in Chromium.
- Every font hash and byte size changed; `dist/pitchdog-font-runtime.json` records the new and source values.

**Repository**

- Renamed `pitchdog-font-handoff-v13/` to `pitchdog-font-handoff/` and the specimen to `pitchdog-typography-system.html`. Removed `MAKE-STANDALONE-v13.html`, an identical copy; the specimen still builds the standalone file, now from the runtime fonts.
- Added `tools/normalize_font_names.py` (with a `--check` mode CI runs), `tools/compare_font_payloads.py` and pinned `tools/requirements.txt`. `scripts/populate_fonts.py` now rebuilds from source, renames, and accepts only a byte-exact match. Removed the redundant `tools/prepare_fonts.py`.
- Added an automatic release workflow: merging a version bump to `main` tags it and publishes the Release with runtime-font, handoff and skill ZIPs plus SHA-256 sidecars. It can also publish a missing Release page for an existing tag.
- Rewrote the README for public readers; added `CONTRIBUTING.md`, `SECURITY.md`, issue templates and a pull-request template.
- Added `docs/FONT-NAMING.md` and `docs/MIGRATION-v13-to-v2.md`; rewrote `docs/KNOWN-FONT-DETAILS.md`.
- Validators now read the version from `package.json` instead of hard-coding it.

## 13.1.1

- Added the model-invoked `pitchdog-type-system` Codex Agent Skill for every task that touches type.
- Kept the skill procedural and lean: it resolves immutable source, routes to canonical files, preserves consumer pins, and verifies real output without copying typography data or fonts.
- Added repository checks for skill structure, invocation metadata, local reference integrity, and the absence of duplicated type-system payloads inside the skill.
- Aligned current release metadata to production and corrected public-source instructions while preserving the all-rights-reserved system and font-only CC0 boundary.
- Left font binaries, semantic roles, metrics, and other typography contracts unchanged from 13.1.0.

## 13.1.0

- Added governed web measure tokens for short display support, introductions, sustained prose, operational copy and the WCAG line-length ceiling.
- Added explicit `auto`, `balance`, `pretty`, `stable` and progressive `avoid-orphans` wrapping contracts as data attributes and utility classes.
- Kept the legacy `.pd-balance`, `.pd-pretty` and `.pd-prose` utilities as compatible aliases.
- Added opt-in language-aware hyphenation instead of forcing word breaks across the system.
- Documented when balancing helps, when prettier wrapping costs too much, how authored line breaks interact with both, and why reading measure remains a separate decision.
- Extended the typography guard and release validator so wrapping policy is testable rather than advisory.

## 13.0.0

- Renamed the release line to lucky-number version 13.
- Replaced every unanchored production weight and width with an authentic font master anchor.
- Repaired Head italics by driving the `ital` axis directly.
- Updated the font authority to `FontBlind-Final-2026-08-28-v13.zip`.
- Added all twelve arrow glyphs to system contracts and specimens.
- Added deep dense-text specimens and copy contracts.
- Added a complete UI/UX typography layer, density policy and component mappings.
- Added YouTube thumbnails, Shorts, podcast cover, channel banner and end-screen contracts.
- Retained social media canvases and brought them under the same anchor policy.
- Added SHA-256 verification to the local font loader.
- Kept the standalone review artifact font-free by default; the private repository now carries seven governed runtime faces and the complete font handoff.
- Corrected the web manifest start URL from the obsolete v3 filename to the canonical v13 HTML.
- Repaired and strengthened the typography guard.
- Expanded release validation to 237 static contract checks and 488 repository checks.
- Completed the 100-check real-font Chromium gauntlet and local standalone-baker round trip.
- Repaired DTCG web-role collisions that had silently dropped `display.hero` and `heading.section`.
- Repaired malformed inline variation-axis styles in the HTML specimen.
- Added private Git consumption metadata, explicit exports, CI, provenance and repository font loading.
