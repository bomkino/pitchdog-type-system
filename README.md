# pitch.dog Type System

The canonical source of truth for pitch.dog fonts, type tokens, CSS roles, interface typography, social formats and YouTube typography.

Current release: **v13.1.1**

## Use it in an authorized project

These integration instructions describe mechanics for pitch.dog and its authorized collaborators; they do not grant a public licence to the surrounding system.

Pin the release. Do not depend on `main`.

```json
{
  "dependencies": {
    "@pitchdog/type-system": "git+https://github.com/bomkino/pitchdog-type-system.git#v13.1.1"
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

For web wrapping and reading measure, use the semantic roles or the explicit `data-pd-wrap` and `data-pd-measure` contracts. Do not put `text-wrap: pretty` on `body`, every paragraph, or an entire application shell. See `docs/WEB-TEXT-WRAPPING.md`.

Do **not** hotlink `raw.githubusercontent.com` URLs in a browser. GitHub is the source and distribution point, not the runtime CDN; each project serves the webfonts from its own build.

## What is authoritative

- `tokens/pitchdog.system.tokens.json` — canonical semantic source
- `dist/pitchdog-system.css` — complete production CSS
- `dist/pitchdog-system.ts` — typed anchors and role names
- `assets/fonts/` — seven exact runtime WOFF2 files
- `pitchdog-font-handoff-v13/` — web, native and static fallback handoff in the full Git repository; deliberately excluded from the web package
- `docs/SPECIFICATION.md` — full behaviour and role specification
- `docs/USING-IN-PROJECTS.md` — framework and non-JavaScript consumption

Variable fonts are authoritative. Static fonts are compatibility fallbacks. Never install the variable and static versions of the same family together.

## Codex Agent Skill

Authorized users can resolve the release tag to its full commit, then install the model-invoked skill from that commit:

```bash
pitchdog_release_commit="$(git ls-remote https://github.com/bomkino/pitchdog-type-system.git 'refs/tags/v13.1.1^{}' | cut -f1)"
if ! printf '%s' "$pitchdog_release_commit" | grep -Eq '^[0-9a-f]{40}$'; then
  echo "Could not resolve v13.1.1 to one full commit." >&2
  exit 1
fi
python3 /path/to/skill-installer/scripts/install-skill-from-github.py \
  --repo bomkino/pitchdog-type-system \
  --path skills/pitchdog-type-system \
  --ref "$pitchdog_release_commit" \
  --method download
```

Confirm the v13.1.1 GitHub Release records that commit and a skill-asset digest before installing. The skill must run whenever work touches typography, fonts, text hierarchy, semantic type roles, wrapping, measure, or rendered text. It resolves this repository at an immutable commit and keeps the canonical type values in `tokens/`, `dist/`, and `docs/` rather than copying them into the skill.

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

The surrounding type-system code, tokens, documentation, examples, artwork and pitch.dog branding remain all-rights-reserved material. See `LICENSE.md` and `FONT-LICENSE.md` for the exact scope.

This GitHub repository is publicly visible as of v13.1.1. Earlier release material may describe private distribution; that history does not change the all-rights-reserved status of the surrounding system or expand the font-only CC0 boundary.
