# Using the type system in projects

## JavaScript projects

Install the private repository at an immutable release tag:

```bash
npm install "git+ssh://git@github.com/bomkino/pitchdog-type-system.git#v13.0.0"
```

Local installs require GitHub SSH access for the `bomkino` account. CI and cloud builds need their own read-only deploy key, GitHub App installation token, or narrowly scoped token stored in the platform's secret manager. Never put a token in `package.json`, a Git URL, browser code or committed `.npmrc`.

Import the complete system from the application entry point:

```js
import "@pitchdog/type-system/system.css";
```

This works with bundlers that process CSS asset URLs, including Vite and its framework integrations. Confirm the production build emits seven WOFF2 assets and that the network panel contains no font 404s.

## Git submodule

For a non-npm project:

```bash
git submodule add git@github.com:bomkino/pitchdog-type-system.git vendor/pitchdog-type-system
git -C vendor/pitchdog-type-system checkout v13.0.0
```

Copy `dist/` and `assets/fonts/` into the project's own static asset pipeline. Keep their relative relationship intact: CSS in `dist/` resolves fonts from `../assets/fonts/`.

## Design, video and native apps

The following folders exist in a full Git checkout or repository download. They are deliberately excluded from the lean web package:

- Variable desktop/native fonts: `pitchdog-font-handoff-v13/02-NATIVE-VARIABLE/`
- Static compatibility fallback: `pitchdog-font-handoff-v13/03-STATIC-ANCHORS-NATIVE/`
- Web variable fonts: `pitchdog-font-handoff-v13/01-WEB-VARIABLE/`
- Static web fallback: `pitchdog-font-handoff-v13/04-OPTIONAL-STATIC-WEB/`

Use variable fonts first. Remove the matching variable family before installing static anchors.

PD Eyebrow's 350 and 400 static files share internal names and can overwrite one another. Use the variable Eyebrow whenever possible. If static files are unavoidable, install only the single Eyebrow weight/posture needed and read `KNOWN-FONT-DETAILS.md` first.

## Caching

Font filenames may be content-hashed by the consuming app. Serve production WOFF2 files with long immutable caching only when the URL itself changes with the file hash.

## Private-source boundary

A private GitHub repository is not a browser CDN. Runtime webfonts inevitably become downloadable by visitors to any public website that uses them. Repository privacy protects the source collection and native handoff, not assets already shipped to a browser.

## Rights boundary

The font binaries are CC0 1.0 Universal and may be copied, modified and redistributed without attribution. The typography-system code, tokens, documentation, examples, artwork and pitch.dog branding are not CC0 and remain private. Keep `FONT-LICENSE.md` with font handoffs as provenance, but not as an additional CC0 condition.
