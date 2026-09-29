# Spacing

Type sizes say what matters; spacing says what belongs together. From 3.0.0 the system publishes a spacing scale for web pages and one for slides, and a flow contract that spaces a column of text by role.

Values live in `web.spacing` and `deck.spacing` in `tokens/pitchdog.system.tokens.json`.

## Web scale

Seven steps. The larger steps grow with the viewport between 360 and 1440 px wide.

| Step | Variable | At 360 px | At 1440 px |
| --- | --- | --- | --- |
| `2xs` | `--pd-space-2xs` | 4 px | 4 px |
| `xs` | `--pd-space-xs` | 8 px | 8 px |
| `s` | `--pd-space-s` | 12 px | 12 px |
| `m` | `--pd-space-m` | 16 px | 20 px |
| `l` | `--pd-space-l` | 24 px | 36 px |
| `xl` | `--pd-space-xl` | 40 px | 64 px |
| `2xl` | `--pd-space-2xl` | 64 px | 112 px |

Use the steps for any vertical rhythm a page needs: between sections, around cards, inside a hero. Interface controls keep their own geometry from the UI layer and its densities.

## Flow

Put `data-pd-flow` on the element that holds a column of text, such as an article, a card body or a section, and the system spaces its direct children:

```html
<article data-pd-flow>
  <p data-pd-type="metadata">CASE STUDY · FILM</p>
  <h1 data-pd-type="display.chapter">From first call to final file.</h1>
  <p data-pd-type="lead.section">Different stages. Same standard.</p>
  <p data-pd-type="body.reading">A good pitch does not simply present information…</p>
  <h2 data-pd-type="heading.subsection">What happens after you reach out</h2>
  <p data-pd-type="body.reading">Moodboard, sample slides, then a complete build…</p>
</article>
```

| Relationship | Space |
| --- | --- |
| Text after text | 1em of the following element (`--pd-flow-space` overrides it) |
| Before `display.hero`, `display.chapter`, `heading.section` | `2xl` |
| After them | `l` |
| Before `heading.subsection`, `quote.feature`, `metric` | `xl` |
| After them | `m` |
| Before `title.card`, `title.functional` | `l` |
| After `title.card` | `s` |
| After `title.functional` | `xs` |
| After `metadata` (a kicker above a heading) | `xs` |
| After `label` (a label above its value) | `2xs` |
| Before and after a figure, image, video, table, code block or rule | `l` |

The rule underneath: a heading sits closer to the text it introduces than to the text before it, so every heading has more space above than below. The validator holds the CSS to this table and to that rule.

Flow only sets the space between siblings. It never adds space before the first child or after the last, so the container's own padding stays in charge of its edges. Nest `data-pd-flow` for a column inside a column.

## Deck scale

Five steps, measured from the slide like deck type. On a 4:3 slide they set at 80 percent, as type does.

| Step | Variable | On a 1080-pixel slide | Use |
| --- | --- | --- | --- |
| `2xs` | `--pd-deck-space-2xs` | 13 px | Table cell padding |
| `xs` | `--pd-deck-space-xs` | 22 px | Between bullets, a kicker and its headline, a label and its value |
| `s` | `--pd-deck-space-s` | 35 px | Between a headline and its lead, and between the parts of a slide |
| `m` | `--pd-deck-space-m` | 56 px | Between groups |
| `l` | `--pd-deck-space-l` | 91 px | Between columns and regions |

The variables are declared on every `data-pd-deck-canvas`, so any element inside a slide can use them. `deck/deck-starter.html` uses nothing else for its gaps.

## In design tools

In Figma, create the web steps as number variables at their 1440 px values (4, 8, 12, 20, 36, 64, 112) and the deck steps at their slide values (13, 22, 35, 56, 91), and use them for auto-layout gaps. In Keynote, PowerPoint and Google Slides, multiply a deck step's 1080 px value by the slide height in points divided by 1080, as for type sizes.
