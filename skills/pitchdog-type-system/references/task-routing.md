# Task routing

Every path below is relative to the pinned commit, and every file is read from that commit. Treat the names as routing candidates: if a path is absent at the pinned commit, find its governed equivalent in that commit's README and tree. If none exists, report a version capability gap.

## Shared semantic work

Start with `docs/SPECIFICATION.md` and `tokens/pitchdog.system.tokens.json`. Use the applicable generated contract in `dist/` for implementation. Read `docs/GOVERNANCE.md` only when a governed role does not fit or a raw declaration already exists in the touched scope.

## Web installation and integration

Read `README.md`, `docs/USING-IN-PROJECTS.md`, `docs/IMPLEMENTATION.md`, and `package.json`. Use package exports from that version. When the work sets paragraphs, or touches wrapping or reading measure, read `docs/WEB-TEXT-WRAPPING.md` and `dist/pitchdog-wrap-contracts.json` when present; absence means the pinned version does not govern that capability.

## Interface work

Read `docs/UI-UX-TYPOGRAPHY.md`, `tokens/pitchdog.ui.tokens.json`, `interface/component-contracts.json`, and the applicable generated role contract in `dist/`. Read `docs/ACCESSIBILITY-QA.md` before accepting a rendered interface.

## Social or YouTube work

For social work, read `docs/SOCIAL-TYPOGRAPHY.md`, `tokens/pitchdog.social.tokens.json`, and the canvas and copy contracts in `social/`. For YouTube work, use the parallel document, token source, and contracts in `youtube/`. Keep platform research dates visible when a task depends on current platform rules; refresh time-sensitive rules from primary platform sources rather than treating old research as current.

## Deck or presentation work

Read `docs/DECKS.md`, `tokens/pitchdog.deck.tokens.json`, and the canvas, copy and template contracts in `deck/`. Choose the density (present or read) before choosing sizes. Deck roles carry their own wrapping, so the web wrapping branch does not apply to slides. For Keynote, PowerPoint, Google Slides or Figma, take sizes from `docs/DECKS.md`: its point-size table for present density, and its read column with the conversion it gives for read density.

## Figma or design-tool work

Read `docs/FIGMA-MAPPING.md`, `docs/figma-style-map.csv`, and `docs/ANCHOR-POLICY.md`. Treat the design-tool library as a derived copy: reconcile its styles against the canonical source and a rendered specimen.

## Native, desktop, or video work

Read `docs/ANCHOR-POLICY.md`, `docs/FONT-NAMING.md`, `docs/KNOWN-FONT-DETAILS.md`, `FONT-PROVENANCE.json`, and the relevant documentation inside the handoff directory identified by that source. Choose native or fixed-canvas files from the manifest inside that handoff; reserve `dist/pitchdog-font-runtime.json` for the web runtime.

## Accessibility or failure diagnosis

Read `docs/ACCESSIBILITY-QA.md`, then the branch document for the affected surface. For font loading, substitution, naming, or posture problems, also read `docs/KNOWN-FONT-DETAILS.md`, `dist/pitchdog-font-runtime.json`, and [runtime verification](runtime-verification.md).

## Version change or release work

Read [version and migration](version-and-migration.md), `CHANGELOG.md`, `RELEASE-RECEIPT.md`, and any migration document that spans the pinned and target versions.
