# Runtime verification

## Source and package

- When the source is a full canonical checkout rather than an installed package, run its repository verifier and inspect any reported mismatch rather than reducing the result to a pass count.
- In a package consumer, confirm the installed dependency or vendored tree resolves to the recorded commit. Compare its canonical token source, package exports, and generated contracts with the same paths in that commit; stop if the installed tree is patched or internally inconsistent.
- Read the runtime font manifest from the resolved version. Match each emitted file to its logical source record by byte size and SHA-256, allowing the consumer to fingerprint its URL. Separately trace each CSS URL to that emitted file and its network response.

## Web runtime

Build the real consumer. Confirm its output emits every font in the resolved runtime manifest, with no unexpected substitute. In a real browser, inspect the intended URL and representative semantic roles:

- font requests succeed and originate from the consumer's asset pipeline;
- `document.fonts` reports the required faces loaded;
- computed family, weight, posture, variation settings, size, line height, and wrapping trace to the selected canonical roles;
- browser rendered-font evidence identifies the face actually used for representative glyphs;
- fallback and blocked-font states remain usable;
- relevant viewport, zoom, text-spacing, language, and reduced-motion conditions do not clip, overflow, or shift dependent geometry;
- counted characters per rendered line of prose stay inside the target range `docs/WEB-TEXT-WRAPPING.md` gives at the pinned commit, at the widest viewport in scope. A `ch` value is not a character count, and a consumer rule that removes or widens a role's measure is a mismatch. This range is for web prose; fixed canvases are held to their copy contracts instead;
- where the pinned version publishes a flow contract, computed space between text blocks traces to it, and each heading sits closer to the text after it than to the text before it, counting a kicker as part of its heading. A consumer margin that overrides flow is a mismatch;
- no descender in a display line touches an ascender, accent or cap in the line below. Report a collision as a mismatch and propose rewording, or a break the wrapping document allows; the user approves copy changes, and changing the role is a governed exception.

Inspect rendered glyphs when posture, interpolation, or synthesis is at issue. A font request, `document.fonts`, or a computed family list alone does not prove the intended face rendered.

## Native and fixed-canvas runtime

When HTML is rendered to a fixed-canvas file (a social image, a thumbnail, a PDF deck), run the web runtime checks on the page and the checks below on the exported file.

Use the handoff manifest and current known-font details from the resolved source. Verify the target application registers the intended file and renders the intended variable instance. For exported media, inspect the final compressed artifact at its delivery size and preserve any platform or device checks that were not run. Delivery size is the size people see: a social post at phone-feed width, a thumbnail at its preview size, a slide on the screen or page it is shown on. Judge the smallest governed text there against the delivery sizes the surface document gives. Text that does not fit or is illegible at delivery size is a mismatch: propose cutting copy or moving it to another frame for the user to approve, and never shrink or enlarge a role locally to rescue it.

## Subtitles

Check a sample of cues in the exported video or the rendered page, including the longest and the fastest. Each cue stays within the line count and the characters per line its frame allows, each line has its own box with no gap between lines, and the reading speed from the cue timing stays within the limit `docs/SUBTITLES.md` gives. For a style without a box, check contrast on the brightest shot it sits over. For vertical video, inspect a frame at phone size with the platform's interface in mind. A text track styled by the player is `unverified` for size and position, not a mismatch.

## Evidence boundary

Record each checked surface and the exact artifact, URL, application, or commit observed. Keep source validation, package installation, emitted assets, font loading, computed styles, visual rendering, export, and user acceptance as separate claims.
