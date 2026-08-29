# pitch.dog Type System v13 — Specification

## 1. Purpose

This system governs every recurring typographic job across:

- the pitch.dog website
- long-form editorial pages and dense operational content
- product and internal-tool interfaces
- social posts, stories, carousel slides and Open Graph cards
- YouTube thumbnails, Shorts covers, podcast covers, banners and end screens

It is a small semantic interface over a heavily tested runtime. Components consume roles. They do not invent typography.

## 2. Family architecture

| Voice | Family | Job |
|---|---|---|
| Story | PD Head | Heroes, chapters, section openings, feature quotations |
| Play | PD Head Alt | Off-Leash, PUMP, PAW, dogs, 404 and selected community moments |
| Explanation | PD Body | Sustained reading, interface copy, controls, dense information |
| Bridge | PD Body Alt | Hero propositions and larger explanatory text |
| Evidence | PD Eyebrow | Metadata, data, versions, formats, filenames and compact arrows |

## 3. Anchor-locked variable policy

Variable files remain the production authority. Static instances are not required for web delivery. The system nevertheless uses only the authentic source anchors for static production typography.

### Head and Head Alt

- Weight: `265, 300, 400, 500, 600, 700, 900`
- Italic: `0` or `1` for static states
- Continuous `ital` interpolation is allowed only for tested transitions and laboratory inspection

### Body and Body Alt

- Weight: `100, 250, 300, 400, 600, 700, 900`
- Roman and Italic are separate authentic variable files
- There is no halfway posture

### Eyebrow

- Weight: `100, 200, 300, 350, 400, 500, 600, 700, 800, 900`
- Width: `87.5` or `100`
- Italic: binary `0` or `1`

No component may request `575`, `92`, `460`, or another convenient-but-unauthentic intermediate value.

## 4. Weight decisions

- Display: Head 600
- Section hierarchy: Head 500
- Feature quote: Head 500 Italic
- Body and leads: Body/Body Alt 400
- Functional emphasis: Body 600
- Major numeric proof: Body 700
- Metadata and aligned data: Eyebrow 500
- UI badges and arrows: Eyebrow 600

This is heavier than an average agency system without becoming swollen. Larger type carries the brand; dense content stays calm.

## 5. Website roles

- `display.hero` — head 600; clamp(3.75rem, 1.42rem + 7.15vi, 8.5rem); line-height 0.88; expressive
- `display.chapter` — head 600; clamp(3.25rem, 1.65rem + 4.9vi, 7rem); line-height 0.91; expressive
- `heading.section` — head 500; clamp(2.75rem, 1.72rem + 3.15vi, 5.5rem); line-height 0.95; both
- `heading.subsection` — head 500; clamp(2.125rem, 1.52rem + 1.85vi, 3.75rem); line-height 0.99; both
- `title.card` — head 500; clamp(1.625rem, 1.34rem + .86vi, 2.375rem); line-height 1.05; both
- `title.functional` — body 600; clamp(1.1875rem, 1.11rem + .24vi, 1.4375rem); line-height 1.18; productive
- `lead.hero` — bodyAlt 400; clamp(1.5rem, 1.19rem + .96vi, 2.375rem); line-height 1.25; expressive
- `lead.section` — bodyAlt 400; clamp(1.25rem, 1.11rem + .43vi, 1.625rem); line-height 1.34; both
- `body.reading` — body 400; clamp(1.1875rem, 1.15rem + .12vi, 1.3125rem); line-height 1.58; both
- `body.default` — body 400; clamp(1.0625rem, 1.025rem + .12vi, 1.1875rem); line-height 1.52; both
- `body.compact` — body 400; clamp(1rem, .981rem + .06vi, 1.0625rem); line-height 1.45; productive
- `body.small` — body 400; clamp(.875rem, .856rem + .06vi, .9375rem); line-height 1.42; productive
- `quote.feature` — head 500; clamp(2.25rem, 1.36rem + 2.72vi, 4.75rem); line-height 1.0; expressive
- `label` — body 600; clamp(.875rem, .856rem + .06vi, .9375rem); line-height 1.2; productive
- `metadata` — eyebrow 500; clamp(.75rem, .731rem + .055vi, .8125rem); line-height 1.28; productive
- `data` — eyebrow 500; clamp(.8125rem, .77rem + .13vi, 1rem); line-height 1.3; productive
- `metric` — body 700; clamp(3.5rem, 1.74rem + 5.42vi, 7.75rem); line-height 0.84; expressive

## 6. Contexts

### Expressive

Heroes, project openings, major statements, editorial storytelling, quotes and proof.

### Productive

Services, process, pricing, FAQs, forms, archives and dense grids. Productive context moves middle-level display roles into the Body family to protect scan speed.

## 7. Tone

`data-pd-type-tone="playful"` swaps the active Head family to Head Alt for a complete section or template. It is not a per-glyph decoration switch.

## 8. Head italics

Head contains a real continuous `ital` axis. Version 13 loads one variable file and drives the axis explicitly:

```css
font-family: var(--pd-font-head);
font-style: normal;
font-variation-settings: "wght" 600, "ital" 1;
```

The explicit axis is intentional. It avoids the ambiguity that prevented the previous specimen from visibly entering the italic master.

## 9. Responsive behaviour

Every public role uses a bounded responsive formula. Display roles receive meaningful fluid growth. Body and UI roles move shallowly. No size depends only on a viewport or container unit. Root-relative limits preserve user control.

## 10. Dense content

Dense content is a first-class mode, not a fallback. It uses:

- Body 400
- Body 600 for genuine emphasis
- 64ch reading measure as a tested default
- 68–72ch for shorter operational copy
- 1.45–1.58 line-height by reading duration
- productive sans titles inside cards and tables
- Eyebrow only for literal data and metadata

## 11. Interface layer

The UI system contains fourteen roles and three density modes. Density changes spacing and control geometry before it changes typography. Default controls are 48 px tall. Coarse-pointer contexts never use the 40 px compact control geometry.

## 12. Media layers

Social and YouTube use canvas-relative roles because their typography belongs to a fixed export surface. They share families and anchor weights with the web but not its responsive formulas.

## 13. Arrows

The supported set is:

`← ↑ → ↓ ↔ ↕ ↖ ↗ ↘ ↙ ↩ ↪`

- Inline arrows inherit Body.
- Functional control arrows use Eyebrow 600 at width 100.
- Expressive arrows use Head 600.

## 14. Governance

The JSON token source is canonical. CSS, TypeScript, role contracts, component maps, Figma maps and specimens derive from it. Arbitrary family, weight, width, posture, size, line-height and tracking declarations are exceptions requiring a recorded rationale.
