# Runtime verification

Use this branch after implementing, building, exporting, migrating, or diagnosing type work.

## Source and package

- In a full canonical checkout, run its repository verifier and inspect any reported mismatch rather than reducing the result to a pass count.
- In a package consumer, confirm the installed dependency or vendored tree resolves to the recorded commit. Compare its canonical token source, package exports, and generated contracts with the same paths in that commit; stop if the installed tree is patched or internally inconsistent.
- Read the runtime font manifest from the resolved version. Match each emitted file to its logical source record by byte size and SHA-256, allowing the consumer to fingerprint its URL. Separately trace each CSS URL to that emitted file and its network response.

## Web runtime

Build the real consumer. Confirm its output emits every font in the resolved runtime manifest, with no unexpected substitute. In a real browser, inspect the intended URL and representative semantic roles:

- font requests succeed and originate from the consumer's asset pipeline;
- `document.fonts` reports the required faces loaded;
- computed family, weight, posture, variation settings, size, line height, and wrapping trace to the selected canonical roles;
- browser rendered-font evidence identifies the face actually used for representative glyphs;
- fallback and blocked-font states remain usable;
- relevant viewport, zoom, text-spacing, language, and reduced-motion conditions do not clip, overflow, or shift dependent geometry.

Inspect rendered glyphs when posture, interpolation, or synthesis is at issue. A font request, `document.fonts`, or a computed family list alone does not prove the intended face rendered.

## Native and fixed-canvas runtime

Use the handoff manifest and current known-font details from the resolved source. Verify the target application registers the intended file and renders the intended variable instance. For exported media, inspect the final compressed artifact at its delivery size and preserve any platform or device checks that were not run.

## Evidence boundary

Record each checked surface and the exact artifact, URL, application, or commit observed. Keep source validation, package installation, emitted assets, font loading, computed styles, visual rendering, export, and user acceptance as separate claims.
