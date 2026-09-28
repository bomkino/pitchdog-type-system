# Release receipt

## Identity

- Product: **pitch.dog Type System**
- Canonical display version: **2**
- Package version: **2.2.0**
- Font authority: `FontBlind-Final-2026-08-28-v13.zip`
- Release date: **28 September 2026**
- State: **production release**

## Scope

The system governs typography across:

- website and long-form editorial pages
- dense operational content
- product and internal-tool interfaces
- social media
- YouTube thumbnails, Shorts, podcast covers, channel banners, and end screens
- pitch decks on 16:9 and 4:3 slides, presented live or read as a PDF
- web reading measures and content-role wrapping contracts
- the complete native arrow set

## Canonical decisions

- Variable fonts remain mandatory.
- Static production typography snaps to authentic source anchors.
- Head and Head Alt use the real continuous `ital` axis, with `0` and `1` as static semantic states.
- Body and Body Alt use separate authentic Roman and Italic variable files.
- Eyebrow uses only the approved weight anchors, width endpoints `87.5` and `100`, and binary posture.
- Components consume semantic roles rather than raw typographic values.
- Short display copy balances; selected editorial prose uses pretty wrapping; controls, navigation, data and dense UI retain normal wrapping.
- Calibrated opt-in measures target about 56–80 characters in PD Body. They are font-specific approximations, not generic `ch` folklore.
- The progressive `avoid-orphans` contract falls back to normal wrapping where it is not supported.
- The default HTML contains no embedded font payload. The canonical repository includes the governed runtime WOFF2 files plus the complete handoff.
- Deck roles size from the slide with container units, set 4:3 slides at 80 percent of 16:9, and never go below 1.8 percent of the slide height. Present and read densities share one role set.
- Every derived file is generated from `tokens/pitchdog.system.tokens.json` by `scripts/build_dist.py`; CI rejects stale output. The web and UI CSS layers remain hand-authored.
- Every font file carries its canonical family name and a unique PostScript name (`docs/FONT-NAMING.md`); only naming and style-linking metadata differs from the FontBlind v13 source.

## Agent Skill

- `skills/pitchdog-type-system/` is the model-invoked Agent Skill, for Codex and Claude, for every task that touches type.
- The skill resolves a tag to a full commit, preserves existing consumer pins unless migration is authorized, and routes each task to the relevant canonical source files.
- The skill contains process, routing, and its rights notice only. It contains no copied type values, CSS, token data, or font binaries.
- Release completion requires independent readback of the tagged source, packaged skill asset, GitHub Release, local installation, and source-to-install hashes.

## Validation receipt

- 2.2.0 rewrites the Agent Skill for agents and adds `AGENTS.md`; no token, CSS, contract or font file changes. `evidence/agent-skill-behavior-v2.2.0.md` records decision-level runs on the pinned, contradictory-latest, runtime-diagnosis and deck branches.
- 2.1.0 adds deck mode and generated derived files; font binaries are byte-identical to 2.0.0. `scripts/build_dist.py --check` passes, and the release validator checks every deck role against its floor, the 80 percent 4:3 ratio, the read-density ordering and limits, template roles, starter markup and the deck print rules.
- `evidence/browser-deck-v2.1.0.json`: in Chromium 141 the starter deck loads all four families; at present and read density on both canvases no element leaves a slide's safe area; computed sizes match the tokens; printing gives 10 pages at 1920 × 1080 px (widescreen) and 1440 × 1080 px (standard); all ten specimen views open, the Decks view has no overflow, and there are no console or page errors.
- 2.0.0 changes font naming metadata only. `evidence/font-name-normalization-v2.0.0.json` records, for all 145 shipped font files, the source and new SHA-256 and that every table other than naming and style-link fields is unchanged (`tools/compare_font_payloads.py`).
- `tools/normalize_font_names.py --check` passes on every font: canonical names, correct style bits, and no two faces sharing a PostScript name.
- `evidence/browser-font-rename-v2.0.0.json`: in Chromium 141 all seven faces load, and all nine specimen views render pixel-identical to 13.1.1 once the changed header text is excluded. The specimen's local loader verifies the new runtime hashes and builds a standalone file with the seven fonts embedded. No console or page errors.
- Repository validation rechecks package exports, canonical metadata, governed font boundaries, font hashes, the full handoff, the normalization evidence and repository checksums.
- The semantic contracts are unchanged from 13.1.1, so the retained 13.0.0 font-audit and 100-check browser evidence still describes the typography; it does not describe the new font names.
- Consumer-specific launch checks remain outside this repository receipt.

## Primary artifacts

- `pitchdog-typography-system.html`
- `tokens/pitchdog.system.tokens.json`
- `tokens/pitchdog.system.dtcg.json`
- `dist/pitchdog-system.css`
- `dist/pitchdog-wrap-contracts.json`
- `dist/pitchdog-system.ts`
- `docs/SPECIFICATION.md`
- `docs/WEB-TEXT-WRAPPING.md`
- `skills/pitchdog-type-system/SKILL.md`
- `evidence/agent-skill-behavior-v2.2.0.md`
- `evidence/agent-skill-behavior-v13.1.1.md`
- `AGENTS.md`
- `evidence/font-name-normalization-v2.0.0.json`
- `evidence/browser-font-rename-v2.0.0.json`
- `evidence/browser-deck-v2.1.0.json`
- `docs/DECKS.md`
- `deck/deck-starter.html`
- `scripts/build_dist.py`
- `docs/FONT-NAMING.md`
- `docs/MIGRATION-v13-to-v2.md`
- `docs/VALIDATION-REPORT.md`
- `evidence/pitchdog-typography-preview-v13.png`
- `SHA256SUMS.txt`

## Launch boundary

Version 2.0.0 renames font metadata and cleans up the repository; typography contracts, glyphs and metrics are unchanged from 13.1.1. Native and design-tool users must reinstall the fonts (`docs/MIGRATION-v13-to-v2.md`). Cross-browser, hardware and assistive-technology checks remain explicit consumer launch gates rather than claims made by this package.
