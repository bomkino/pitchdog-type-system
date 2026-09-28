# Deck typography

Deck mode sets pitch decks and presentations with the same families, anchors and voice as the rest of pitch.dog. It adds fourteen slide roles, two slide canvases, and two densities: **present** for slides shown live, and **read** for decks sent ahead as a PDF.

Every size is measured from the slide itself with container query units, so a slide sets the same way in a browser window, full screen on a projector, and on a printed page.

See it working in `deck/deck-starter.html` (open it from a checkout) and in the Decks view of `pitchdog-typography-system.html`.

## Quick start

```html
<link rel="stylesheet" href="node_modules/@pitchdog/type-system/dist/pitchdog-system.css">

<main data-pd-deck-density="present">
  <section data-pd-deck-canvas="widescreen" style="inline-size: 100%">
    <div data-pd-deck-safe>
      <p data-pd-deck="kicker">Series A · 2026</p>
      <h1 data-pd-deck="title">Your pitch’s best friend.</h1>
      <p data-pd-deck="footer">pitch.dog</p>
    </div>
  </section>
</main>
```

- `data-pd-deck-canvas` makes the element a slide: it sets the aspect ratio and becomes the container every deck size is measured from. Give it a width; the height follows.
- `data-pd-deck-safe` is an optional child positioned on the canvas's safe area. Lay out its contents with your own flex or grid rules.
- `data-pd-deck="…"` applies a role. Roles only size correctly inside a canvas.
- `data-pd-deck-density="read"` on the deck, or on one slide, switches to the read sizes.

Import only the deck layer with `@pitchdog/type-system/deck.css` after `fonts.css` and `typography.css`; like the other media layers it uses variables that `typography.css` declares.

## Canvases

| Canvas | Size | Ratio | Safe area | Use |
| --- | --- | --- | --- | --- |
| `widescreen` | 1920 × 1080 | 16:9 | 80 px top and bottom, 96 px left and right | Keynote, Google Slides, PowerPoint and PDF default |
| `standard` | 1440 × 1080 | 4:3 | 80 px on every edge | Projectors, printed handouts and legacy templates |

Every size is written as `min(0.6 × Y cqi, Y cqb)`. On a 16:9 slide the height wins, so type is `Y` percent of the slide height. A 4:3 slide is narrower, so the width wins and every role sets at 80 percent of its widescreen size; copy held to a `ch` measure keeps its line breaks.

## Roles

Sizes are for a 1920 × 1080 slide. On a 1440 × 1080 slide multiply by 0.8.

| Role | Face | 16:9 present | 16:9 read | Lines / words | Use |
| --- | --- | --- | --- | --- | --- |
| `deck.title` | Head 600 | 101.5 px | — | 3 / 10 | Cover and closing titles |
| `deck.section` | Head 500 italic | 129.6 px | — | 2 / 5 | Chapter dividers in Head italic |
| `deck.headline` | Head 500 | 58.3 px | 49.7 px | 2 / 14 (read 3 / 20) | The claim at the top of a content slide |
| `deck.statement` | Head 500 | 82.1 px | 69.1 px | 4 / 16 (read 4 / 20) | A slide that is one sentence and nothing else |
| `deck.lead` | Body Alt 400 | 38.9 px | 32.4 px | 3 / 28 (read 4 / 40) | The sentence that explains a headline |
| `deck.body` | Body 400 | 30.2 px | 24.8 px | 7 / 55 (read 12 / 110) | Supporting paragraphs; keep them rare when presenting live |
| `deck.bullet` | Body 400 | 32.4 px | 27.0 px | 2 / 14 · 5 items (read 3 / 24 · 7 items) | List items; limits are per item |
| `deck.quote` | Head 500 italic | 56.2 px | 47.5 px | 5 / 32 (read 6 / 45) | Customer, investor and press quotes |
| `deck.metric` | Body 700 | 183.6 px | — | 1 / 2 | One hero number per slide |
| `deck.kicker` | Eyebrow 500 · wdth 87.5 · caps | 23.8 px | — | 1 / 6 | Section markers and slide eyebrows |
| `deck.label` | Body 600 | 24.8 px | 21.6 px | 2 / 8 | Metric labels, column heads, legends and attributions |
| `deck.data` | Eyebrow 500 · wdth 100 | 24.8 px | 21.6 px | 1 / 4 | Table figures and chart axes |
| `deck.source` | Body 400 | 21.6 px | 19.4 px | 2 / 30 | Sources, footnotes and disclaimers |
| `deck.footer` | Eyebrow 500 · wdth 87.5 · caps | 19.4 px | — | 1 / 8 | Running footer: company, date and slide number |

Titles, section dividers, headlines and statements balance their lines. Leads, body, bullets and quotes use pretty wrapping. Kicker and footer are set in capitals by CSS, so write them in sentence case.

The canonical values, with every limit, live in `deck.roles` in `tokens/pitchdog.system.tokens.json`. `deck/copy-contracts.json` repeats the limits for copy tools.

## Densities

**Present** is the default. The deck is shown while someone talks, and the audience reads from across a room: one idea per slide, and as little body copy as you can manage.

**Read** is for a deck that travels without you: sent ahead of a meeting, attached to an email, read on a phone. Set `data-pd-deck-density="read"` and nine roles step down one notch (headline, statement, lead, body, bullet, quote, label, data and source) while their line and word limits rise. Title, section, metric, kicker and footer stay the same so the deck still looks like itself.

## Size floor

No role sets below **1.8 % of the slide height** (19.4 px on a 1080 px slide). At present density every role except the running footer stays at or above **2 %** (21.6 px). The validator enforces both floors. If copy does not fit, cut words or split the slide; do not shrink the type.

## Templates

`deck/templates.json` lists ten slide formulas. Each names the roles it uses.

| Template | Formula | Roles |
| --- | --- | --- |
| `cover` | Kicker + title + presenter line | kicker, title, footer |
| `section` | Section marker + a chapter title of one to five words | kicker, section |
| `statement` | One sentence and nothing else | statement |
| `insight` | Claim + explanation + optional body + source | headline, lead, body, source |
| `metric` | One number + what it measures + where it came from | metric, label, source |
| `quote` | Pull quote + attribution | quote, label |
| `list` | Headline + three to five bullets | headline, bullet |
| `data` | Headline + table or chart with figures in `deck.data` | headline, label, data, source |
| `compare` | Headline + two labelled columns | headline, label, body |
| `close` | The ask + next step + contact | title, lead, footer |

## Writing for slides

1. Write the headline as the claim the slide proves, not as a topic label. "Revenue tripled in 2026", not "Revenue".
2. One idea per slide. If a slide needs two headlines, it is two slides.
3. Put the proof under the claim: lead first, then body only if the room needs it.
4. Every number gets a label and, when it is not yours, a source.
5. Keep bullets to five at present density and make each one fit on two lines.
6. Use Head italic for section dividers and quotes only. It is emphasis, not decoration.
7. Leave the footer alone. It is furniture: company, date and slide number.

## Numbers

PD Body and PD Head have proportional digits and no tabular-figures feature, so `font-variant-numeric: tabular-nums` does nothing in them. That is right for a hero metric, where each digit should take its natural width.

For anything that must line up (tables, chart axes, prices in a column) use `deck.data`. It is set in PD Eyebrow, which is monospaced: digits, letters and punctuation share one advance width at each width setting (dashes, ellipses and arrows are double width), so columns align with no OpenType features. Align numeric columns to the end.

## Export to PDF

The deck layer includes print rules: each canvas starts a new page, and the page is named `pd-deck-widescreen` (1920 × 1080 px) or `pd-deck-standard` (1440 × 1080 px) with no margin. In Chromium-based browsers, print and choose **Save as PDF**, and turn on **Background graphics** for coloured slides. The starter deck's **Save as PDF** button does exactly that.

For print, give the slide `inline-size: 100%` and remove decorative margins, shadows and rounded corners; the starter deck shows the pattern. Use one canvas per deck: the page size follows the slides' parent.

## Keynote, PowerPoint, Google Slides and Figma

Install the variable fonts from `pitchdog-font-handoff/02-NATIVE-VARIABLE/` first. The families appear as PD Head, PD Head Alt, PD Body, PD Body Alt and PD Eyebrow, with named instances such as *Medium Italic* (`docs/FONT-NAMING.md`). If an app does not list the named instances, install the static fonts from `03-STATIC-ANCHORS-NATIVE/` instead. Never install both.

Point sizes for each app's default slide size, rounded to whole points:

| Role | Keynote 1920 × 1080 | PowerPoint 13.33 × 7.5 in | Google Slides 10 × 5.625 in |
| --- | --- | --- | --- |
| `deck.title` | 102 pt | 51 pt | 38 pt |
| `deck.section` | 130 pt | 65 pt | 49 pt |
| `deck.headline` | 58 pt | 29 pt | 22 pt |
| `deck.statement` | 82 pt | 41 pt | 31 pt |
| `deck.lead` | 39 pt | 19 pt | 15 pt |
| `deck.body` | 30 pt | 15 pt | 11 pt |
| `deck.bullet` | 32 pt | 16 pt | 12 pt |
| `deck.quote` | 56 pt | 28 pt | 21 pt |
| `deck.metric` | 184 pt | 92 pt | 69 pt |
| `deck.kicker` | 24 pt | 12 pt | 9 pt |
| `deck.label` | 25 pt | 12 pt | 9 pt |
| `deck.data` | 25 pt | 12 pt | 9 pt |
| `deck.source` | 22 pt | 11 pt | 8 pt |
| `deck.footer` | 19 pt | 10 pt | 7 pt |

For any other slide size, multiply the 1080 px value by the slide height in points divided by 1080. For read density, use the read column above in the same way.

- **Keynote.** Use the Wide (1920 × 1080) theme size; pixel values are point values. Set tracking from the role's `tracking` (Keynote's character spacing is a percentage: −0.042em is −4.2 %).
- **PowerPoint.** Embed fonts when you send a `.pptx`, or send a PDF; otherwise the recipient sees a substitute font.
- **Google Slides.** Slides only offers fonts from Google Fonts, so the PD families cannot be used there. Build the deck in the browser or Keynote and share the PDF, or import finished slides as images.
- **Figma.** Use 1920 × 1080 frames and the px values above. `docs/figma-style-map.csv` lists a style for every role, plus a `Deck / Read / …` style for each read size.

## Files

| File | What it is |
| --- | --- |
| `dist/pitchdog-deck.css` | The deck layer (also bundled in `dist/pitchdog-system.css`) |
| `tokens/pitchdog.deck.tokens.json` | Deck canvases, densities, floor, roles and templates |
| `deck/canvas-contracts.json` | Canvas sizes and safe areas |
| `deck/copy-contracts.json` | Line, word and item limits per role, with read-density limits |
| `deck/templates.json` | The ten slide formulas |
| `deck/deck-starter.html` | A ten-slide starter with canvas, density and head-tone switches, a presenter mode and PDF export |

All of these except the starter are generated from `tokens/pitchdog.system.tokens.json` by `scripts/build_dist.py`.
