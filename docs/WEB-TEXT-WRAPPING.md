# Web text wrapping and reading measure

Version 13.1 turns line wrapping into an explicit content-role decision. It does not ask one browser keyword to repair weak copy, an over-wide layout or an unclear hierarchy.

## The policy

| Content job | Wrap | Measure | Why |
|---|---|---|---|
| Display, section heading, short caption | `balance` | Role-specific, usually 11.5–25ch | The phrase is short and the line endings are part of the composition. Keep it to five lines or fewer. |
| Hero or section introduction | `pretty` | `intro` (about 71 characters in PD Body) | A small amount of important prose benefits from better last lines and fewer awkward breaks. |
| Sustained editorial reading | `pretty` | `reading` (about 67 characters in PD Body) | Reading quality matters more than the small extra layout cost. |
| Repeated cards, archive descriptions, operational copy | `avoid-orphans` or `auto` | `default`–`wide` (about 71–77 characters in PD Body) | Prefer a lower-cost last-line improvement when supported; normal wrapping is a safe fallback. |
| Editable text | `stable` | Component-specific | Earlier lines should not keep reflowing while a person types. |
| Navigation, buttons, filters, data, metadata and dense UI | `auto` | Component-specific | Predictability and speed matter more than decorative line endings. |

The browser algorithms are progressive enhancement. Copy structure, measure and line height remain the real foundation.

## Measure tokens

- `narrow` — 38ch, roughly 56 characters of representative PD Body copy
- `intro` — 48ch, roughly 71 characters for propositions and section introductions
- `reading` — 45ch, roughly 67 characters for sustained prose
- `default` — 48ch, roughly 71 characters for general website copy
- `wide` — 52ch, roughly 77 characters for compact operational copy with enough leading
- `ceiling` — 54ch, calibrated to roughly 80 characters and not intended as a normal target

The values deliberately sit inside the 45–90 character range used by USWDS, near its 66-character long-reading target, and below the 75-character GOV.UK recommendation for ordinary page layouts. They also respect WCAG 2.2’s 80-character Visual Presentation ceiling.

`ch` measures the advance width of the font’s zero; it does not count characters. These new utility values were therefore calibrated in PD Body against representative English copy instead of copying generic `ch` numbers. They remain approximations: review real text in the real font rather than treating a token as a guarantee. Version 13’s intrinsic role widths remain unchanged for compatibility; adding a `data-pd-measure` contract is the explicit opt-in to the calibrated reading measures.

## Why `pretty` is opt-in

`text-wrap-style` is inherited. A rule on `body`, every `p`, or an application shell can silently affect controls, table cells, generated content and hundreds of repeated cards. The CSS Text specification also allows `pretty` to spend more layout time considering multiple lines. Use it where the words deserve that work; do not pay for it everywhere.

Browser algorithms and limits differ. MDN records a six-line balancing limit in Chromium and ten lines in Firefox. The pitch.dog contract is intentionally stricter: balance only composed text expected to remain within five lines.

## Authored breaks and copy editing

- Edit the sentence before styling it. Remove accidental ellipses, duplicated ideas, soft filler and clauses that make the reader hold too much in memory.
- Use paragraphs, lists and subheads to express structure. Wrapping cannot create structure that is missing from the copy.
- Use `<br>` only for a deliberate thought turn that should survive every viewport. It creates separate balancing contexts and is not a responsive layout tool.
- Do not sculpt line endings with strings of non-breaking spaces. They turn an aesthetic preference into an overflow bug.
- Do not fully justify web prose. A clean rag is more resilient under zoom, font fallback and user text-spacing overrides.

## API

```html
<h2 data-pd-type="heading.section" data-pd-wrap="balance">
  Three kinds of pitch. One unreasonable standard.
</h2>

<p data-pd-type="lead.section" data-pd-wrap="pretty" data-pd-measure="intro">
  Important introductory copy goes here.
</p>

<p data-pd-type="body.default" data-pd-wrap="avoid-orphans" data-pd-measure="default">
  Repeated supporting copy receives normal wrapping today and lower-cost orphan protection where the browser supports it.
</p>

<div contenteditable="true" data-pd-ui="input" data-pd-wrap="stable"></div>
```

Class equivalents are available as `.pd-wrap-*` and `.pd-measure-*`. The older `.pd-balance`, `.pd-pretty` and `.pd-prose` names remain compatible aliases.

For language-aware hyphenation, put the correct `lang` on the document or content block and opt in with `data-pd-hyphenate` or `.pd-hyphenate`. Never enable automatic hyphenation without a trustworthy language declaration.

## Required QA

- 320, 360 and 390 CSS px widths
- 768–1024 CSS px intermediate layouts
- 1440, 1920 and 3840 CSS px desktop layouts
- 200% text zoom and WCAG text-spacing overrides
- real, unusually short and unusually long copy
- font loaded, font blocked and fallback-font states
- one- through five-line headings for balance
- editable typing for stable wrapping
- correct `lang` before hyphenation

## Sources

Checked 31 August 2026.

- W3C, CSS Text Module Level 4: https://www.w3.org/TR/css-text-4/
- MDN, `text-wrap-style`: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap-style
- W3C WAI, Understanding WCAG 2.2 SC 1.4.8: https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation
- U.S. Web Design System, Typography: https://designsystem.digital.gov/components/typography/
- GOV.UK Design System, Layout: https://design-system.service.gov.uk/styles/layout/
