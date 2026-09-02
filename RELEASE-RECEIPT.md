# Release receipt

## Identity

- Product: **pitch.dog Type System**
- Canonical display version: **13**
- Package version: **13.1.1**
- Font authority: `FontBlind-Final-2026-08-28-v13.zip`
- Release date: **3 September 2026**
- State: **production release**

## Scope

Version 13 governs typography across:

- website and long-form editorial pages
- dense operational content
- product and internal-tool interfaces
- social media
- YouTube thumbnails, Shorts, podcast covers, channel banners, and end screens
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
- `MAKE-STANDALONE-v13.html` embeds the accepted CC0-1.0 font binaries locally when a one-file review artifact is needed.

## Agent Skill

- `skills/pitchdog-type-system/` is the model-invoked Codex Agent Skill for every task that touches type.
- The skill resolves a tag to a full commit, preserves existing consumer pins unless migration is authorized, and routes each task to the relevant canonical source files.
- The skill contains process, routing, and its rights notice only. It contains no copied type values, CSS, token data, or font binaries.
- Release completion requires independent readback of the tagged source, packaged skill asset, GitHub Release, local installation, and source-to-install hashes.

## Validation receipt

- The semantic contracts and font binaries remain unchanged from 13.1.0. Retained machine-captured font and browser evidence keeps its original 13.0.0 / 28 August identity; it supports the unchanged payload, not this patch release's identity.
- Repository validation rechecked package exports, canonical metadata, governed font boundaries, font hashes, the full handoff, and repository checksums.
- Skill validation rechecked its frontmatter, universal trigger, invocation metadata, local references, and zero duplicated typography payloads.
- Realistic agent runs exercised an existing pinned consumer, a contradictory latest-release request, and runtime font diagnosis; `evidence/agent-skill-behavior-v13.1.1.md` records the observed decisions and limits.
- Browser console and page errors remain absent in the retained version 13 browser evidence. Consumer-specific launch checks remain outside this repository receipt.

## Primary artifacts

- `pitchdog-typography-system-v13.html`
- `MAKE-STANDALONE-v13.html`
- `tokens/pitchdog.system.tokens.json`
- `tokens/pitchdog.system.dtcg.json`
- `dist/pitchdog-system.css`
- `dist/pitchdog-wrap-contracts.json`
- `dist/pitchdog-system.ts`
- `docs/SPECIFICATION.md`
- `docs/WEB-TEXT-WRAPPING.md`
- `skills/pitchdog-type-system/SKILL.md`
- `evidence/agent-skill-behavior-v13.1.1.md`
- `docs/VALIDATION-REPORT.md`
- `evidence/pitchdog-typography-preview-v13.png`
- `SHA256SUMS.txt`

## Launch boundary

Version 13.1.1 adds the Codex Agent Skill and aligns release metadata; it does not change the governed typography contracts or font binaries from 13.1.0. The pitch.dog website received focused Chromium checks at 320, 390, 1200 and 3840 CSS px. Cross-browser, hardware and assistive-technology checks remain explicit consumer launch gates rather than claims made by this package.
