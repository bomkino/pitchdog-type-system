# Implementation

## Installed package

The private package already includes all seven runtime WOFF2 files. Import the complete system once from your application entry point:

```js
import "@pitchdog/type-system/system.css";
```

No font-preparation step is required after package installation.

## Full Git checkout font maintenance

The following command is for maintainers working in a complete repository checkout. The `tools/` directory is deliberately excluded from the lean installed package.

Run:

```bash
python3 tools/prepare_fonts.py "/path/to/FontBlind-Final-2026-08-28-v13.zip"
```

The tool verifies all seven files by SHA-256 before writing `assets/fonts/`.

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

## Local standalone review from a full checkout

`MAKE-STANDALONE-v13.html` exists only in the complete Git repository. Open it there, select the v13 font ZIP, then build. The browser verifies the seven source hashes before embedding them into the downloaded review file.
