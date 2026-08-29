# YouTube typography

Research checked: 28 August 2026.

## Current platform contracts

- Standard video thumbnails: 3840 × 2160 recommended, 16:9, with at least 640 px width.
- Shorts thumbnails: 2160 × 3840 recommended, 9:16.
- Podcast playlist covers: 1:1.
- Channel banner: 2560 × 1440 recommended; minimum upload 2048 × 1152; at the minimum size, the central text/logo safe area is 1235 × 338.
- Standard 16:9 end screens can contain up to four elements and occupy the final 5–20 seconds.

Official sources are recorded in `docs/RESEARCH-SOURCES.md`.

## Roles

- `youtube.title` — head 700; maximum 2 lines / 7 words
- `youtube.titleCompact` — head 600; maximum 3 lines / 11 words
- `youtube.kicker` — eyebrow 700; maximum 1 lines / 6 words
- `youtube.support` — bodyAlt 600; maximum 2 lines / 12 words
- `youtube.badge` — body 700; maximum 1 lines / 4 words
- `youtube.credit` — body 600; maximum 1 lines / 7 words
- `youtube.arrow` — head 700; maximum 1 lines / 1 words

## Thumbnail rules

1. The title and image must tell one combined story.
2. Use 2–7 words when possible.
3. Keep the main title to two lines. Use the compact title only when the idea genuinely needs three.
4. Put branding and episode information in the kicker, not the title.
5. Keep the lower-right duration area clear.
6. Make the title readable at roughly 10–15% of the full canvas size.
7. Avoid repeating the exact video title unless the repetition improves comprehension.
8. Use Head 700 only here and in other fixed-canvas situations where compression demands more authority.
9. Use arrows as composition, not clickbait punctuation.
10. Build genuinely different A/B variants, not tiny cosmetic changes.

## Template grammar

- `tutorial` — Kicker + two-line title + one visual action; example: HOW WE BUILD / A PITCH DECK
- `critique` — Programme badge + diagnosis + marked detail; example: WHY THIS DECK FAILS
- `beforeAfter` — Split proof + BEFORE → AFTER; example: BEFORE → AFTER
- `process` — Episode marker + promise + artifact; example: ONE WEEK. ONE DECK.
- `opinion` — One hard statement + small qualifier; example: STOP USING TEMPLATES.
- `caseStudy` — Project name + outcome + visual proof; example: HOW WE WON THE ROOM
