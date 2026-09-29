# Task routing

Every path below is relative to the pinned commit, and every file is read from that commit. Treat the names as routing candidates: if a path is absent at the pinned commit, find its governed equivalent in that commit's README and tree. If none exists, report a version capability gap.

## Shared semantic work

Start with `docs/SPECIFICATION.md` and `tokens/pitchdog.system.tokens.json`. Use the applicable generated contract in `dist/` for implementation. Read `docs/GOVERNANCE.md` only when a governed role does not fit or a raw declaration already exists in the touched scope.

## Web installation and integration

Read `README.md`, `docs/USING-IN-PROJECTS.md`, `docs/IMPLEMENTATION.md`, and `package.json`. Use package exports from that version. When the work sets paragraphs, or touches wrapping or reading measure, read `docs/WEB-TEXT-WRAPPING.md` and `dist/pitchdog-wrap-contracts.json` when present; absence means the pinned version does not govern that capability.

## Spacing

When the work spaces text blocks on a page or a slide, read `docs/SPACING.md` when present. On the web, space a column of text with its flow contract rather than margins on each element; on slides, use the deck spacing steps. Absence means the pinned version does not govern spacing.

## Interface work

Read `docs/UI-UX-TYPOGRAPHY.md`, `tokens/pitchdog.ui.tokens.json`, `interface/component-contracts.json`, and the applicable generated role contract in `dist/`. Read `docs/ACCESSIBILITY-QA.md` before accepting a rendered interface.

## Social or YouTube work

For social work, read `docs/SOCIAL-TYPOGRAPHY.md`, `tokens/pitchdog.social.tokens.json`, and the canvas and copy contracts in `social/`. For YouTube work, use the parallel document, token source, and contracts in `youtube/`. Keep platform research dates visible when a task depends on current platform rules; `docs/RESEARCH-SOURCES.md` records when each rule was checked. Refresh a time-sensitive rule from its primary platform source before relying on it, and report any difference rather than treating old research as current.

## Deck or presentation work

Read `docs/DECKS.md`, `tokens/pitchdog.deck.tokens.json`, and the canvas, copy and template contracts in `deck/`. Choose the density (present or read) before choosing sizes. Deck roles carry their own wrapping, so the web wrapping branch does not apply to slides. For Keynote, PowerPoint or Figma, take sizes from `docs/DECKS.md`: its point-size table for present density, and its read column with the conversion it gives for read density. Google Slides cannot load the PD families, so a deck set there is a font mismatch whatever its sizes; follow the document's advice on rebuilding it.

## Subtitle or caption work

Read `docs/SUBTITLES.md`, `tokens/pitchdog.subtitle.tokens.json`, and the canvas and copy contracts in `subtitle/` when present. Choose the frame and style first, then decide whether subtitles are burned in or shipped as a text track: burned-in subtitles take their sizes from the document's frame table, and a text track leaves size to the player and the viewer. Wording and timing come from the transcript or the user, and line breaks follow the document's rules; propose any change to wording or timing for the user to approve. Placement on vertical video rests on third-party guides to the platforms' interfaces; `docs/RESEARCH-SOURCES.md` records when they were checked, and a changed interface is reported like any other refreshed platform rule.

## Figma or design-tool work

Read `docs/FIGMA-MAPPING.md`, `docs/figma-style-map.csv`, and `docs/ANCHOR-POLICY.md`. Treat the design-tool library as a derived copy: reconcile its styles against the canonical source and a rendered specimen.

## Native, desktop, or video files

Read `docs/ANCHOR-POLICY.md`, `docs/FONT-NAMING.md`, `docs/KNOWN-FONT-DETAILS.md`, `FONT-PROVENANCE.json`, and the relevant documentation inside the handoff directory identified by that source. Choose native or fixed-canvas files from the manifest inside that handoff; reserve `dist/pitchdog-font-runtime.json` for the web runtime.

## Review, accessibility or failure diagnosis

Read `docs/ACCESSIBILITY-QA.md`, then the branch document for the affected surface. A review of how type looks is judged on the rendered result at its delivery size, measured, not from the token values alone. For font loading, substitution, naming, or posture problems, also read `docs/KNOWN-FONT-DETAILS.md`, `dist/pitchdog-font-runtime.json`, and [runtime verification](runtime-verification.md).

## Version change or release work

Read [version and migration](version-and-migration.md), `CHANGELOG.md`, `RELEASE-RECEIPT.md`, and any migration document that spans the pinned and target versions.
