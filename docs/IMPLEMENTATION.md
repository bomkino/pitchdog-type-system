# Implementation

## Installed package

The installed package already includes all seven runtime WOFF2 files. Import the complete system once from your application entry point:

```js
import "@pitchdog/type-system/system.css";
```

No font-preparation step is required after package installation.

## Full Git checkout font maintenance

The following command is for maintainers working in a complete repository checkout. The `tools/` directory is deliberately excluded from the lean installed package.

Run:

```bash
python3 -m pip install -r tools/requirements.txt
python3 scripts/populate_fonts.py "/path/to/FontBlind-Final-2026-08-28-v13.zip" --replace
```

The script rebuilds the handoff from the source, applies the 2.0.0 name normalization (`docs/FONT-NAMING.md`), and writes `assets/fonts/` and the handoff fonts only if every file matches the committed SHA-256.

## Direct CSS use

For a copied checkout or non-JavaScript build, preserve the relative relationship between `dist/` and `assets/fonts/`, then link the complete stylesheet:

```html
<link rel="stylesheet" href="./dist/pitchdog-system.css">
```

## Website

```html
<h1 data-pd-type="display.hero">
  Your pitch’s <span data-pd-emphasis="head-italic">best friend.</span>
</h1>
```

Use explicit wrapping and measure contracts when a role alone does not express the content job:

```html
<p data-pd-type="lead.section" data-pd-wrap="pretty" data-pd-measure="intro">
  A short, important introduction.
</p>
```

Do not apply `pretty` to `body`, every paragraph or an entire interface. Use `docs/WEB-TEXT-WRAPPING.md` to choose between `balance`, `pretty`, `stable`, progressive `avoid-orphans` and normal wrapping.

## Productive context

```html
<section data-pd-type-context="productive">
  <h2 data-pd-type="heading.subsection">What it costs.</h2>
</section>
```

## Playful tone

```html
<section data-pd-type-tone="playful">
  <h2 data-pd-type="heading.section">Free help. No strings. No kidding.</h2>
</section>
```

## Interface

```html
<button class="pd-ui-button" data-pd-ui="action">
  Continue <span data-pd-arrow="ui" aria-hidden="true">→</span>
</button>
```

## Decks

```html
<main data-pd-deck-density="present">
  <section data-pd-deck-canvas="widescreen">
    <div data-pd-deck-safe>
      <h2 data-pd-deck="headline">Investors decide in the first four minutes.</h2>
      <p data-pd-deck="lead">So the claim goes on the slide, not in the speaker notes.</p>
    </div>
  </section>
</main>
```

Switch to `data-pd-deck-density="read"` for decks sent as a PDF. `docs/DECKS.md` covers canvases, sizes, printing and app point sizes; `deck/deck-starter.html` is a working ten-slide starter.

## Regenerating derived files

Semantic values change only in `tokens/pitchdog.system.tokens.json`. Then run:

```bash
python3 scripts/build_dist.py
```

It rewrites the split token files, the DTCG export, the TypeScript types, the role, canvas, copy and template contracts, the Figma style map, the social, YouTube and deck CSS, both system bundles and the specimen's inline CSS. The web and UI layers (`dist/pitchdog-typography.css`, `dist/pitchdog-ui.css`) are still authored by hand. `--check` fails if anything is stale; CI runs it. The minified bundle needs esbuild 0.28.2, fetched through `npx` or taken from `PD_ESBUILD`.

## Local standalone review from a full checkout

`pitchdog-typography-system.html` exists only in the complete Git repository. Open it there, choose the `assets/fonts/` folder or the release's `pitchdog-fonts-<tag>.zip` in the local loader, then build. The browser verifies the seven runtime hashes before embedding them into the downloaded review file.
