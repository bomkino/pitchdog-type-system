# pitch.dog Type System

The private source of truth for pitch.dog fonts, type tokens, CSS roles, interface typography, social formats and YouTube typography.

Current release: **v13.0.0**

## Use it in a project

Pin the release. Do not depend on `main`.

```json
{
  "dependencies": {
    "@pitchdog/type-system": "git+ssh://git@github.com/bomkino/pitchdog-type-system.git#v13.0.0"
  }
}
```

Then load the complete system once:

```js
import "@pitchdog/type-system/system.css";
```

For a deliberately split build, load the font registration and typography foundation first, then optional layers:

```js
import "@pitchdog/type-system/fonts.css";
import "@pitchdog/type-system/typography.css";
import "@pitchdog/type-system/ui.css";
import "@pitchdog/type-system/social.css";
import "@pitchdog/type-system/youtube.css";
```

`ui.css`, `social.css` and `youtube.css` are not standalone; they consume variables declared by `typography.css`.

The CSS resolves the seven canonical WOFF2 files from this package. Your app's bundler should copy and fingerprint them with the rest of its assets.

Do **not** hotlink private `raw.githubusercontent.com` URLs in a browser. They need authentication, and placing a GitHub token in client-side CSS would leak it. GitHub is the source and distribution point; each project serves the webfonts from its own build.

## What is authoritative

- `tokens/pitchdog.system.tokens.json` — canonical semantic source
- `dist/pitchdog-system.css` — complete production CSS
- `dist/pitchdog-system.ts` — typed anchors and role names
- `assets/fonts/` — seven exact runtime WOFF2 files
- `pitchdog-font-handoff-v13/` — web, native and static fallback handoff in the full Git repository; deliberately excluded from the web package
- `docs/SPECIFICATION.md` — full behaviour and role specification
- `docs/USING-IN-PROJECTS.md` — framework and non-JavaScript consumption

Variable fonts are authoritative. Static fonts are compatibility fallbacks. Never install the variable and static versions of the same family together.

## Repository maintenance

These commands and the full font handoff exist in a complete Git checkout, not the lean package installed into web projects.

```bash
python3 scripts/verify_repository.py
```

The verifier rejects missing or altered runtime fonts, unexpected font locations, broken package exports, malformed JSON, a damaged full handoff, and system-contract regressions.

To populate a fresh checkout from the accepted source archive:

```bash
python3 scripts/populate_fonts.py /path/to/FontBlind-Final-2026-08-28-v13.zip
```

It also accepts the already-generated `pitchdog-font-handoff-v13.zip`.

## Release discipline

- Pin projects to an immutable tag or commit.
- Patch: fixes that preserve font metrics and role contracts.
- Minor: additive roles or tokens.
- Major: any font binary, metric, axis, family-name or existing role change that can reflow layouts.
- Never commit source archives, access tokens, `.npmrc`, or `.env` files.

PD Eyebrow's v13 native binaries still identify internally as `Untitled`; its 350/400 static anchors also collide by name. Web CSS aliases the family safely. Desktop and native consumers must read `docs/KNOWN-FONT-DETAILS.md` before using static fallbacks.

## Rights

Font binaries in `assets/fonts/` and `pitchdog-font-handoff-v13/` are dedicated under **CC0 1.0 Universal**. They may be used, changed and redistributed without an attribution requirement; keep `FONT-LICENSE.md` with handoffs as a provenance best practice.

The surrounding type-system code, tokens, documentation, examples, artwork and pitch.dog branding remain private, all-rights-reserved material. See `LICENSE.md` and `FONT-LICENSE.md` for the exact scope.
