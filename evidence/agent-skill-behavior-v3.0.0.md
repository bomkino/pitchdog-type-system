# Agent Skill behaviour evidence — v3.0.0

Date: 29 September 2026

Five independent Claude agents each received the candidate skill, one realistic request and a described fixture. They made no edits. These are decision-level runs of the checks and routes added in 3.0.0, not user acceptance or a substitute for testing a real consumer. The first two ran while the release was still being prepared in the working tree; the last three read a clean checkout of candidate commit `a80c2f6`, before the v3.0.0 tag existed.

## Candidate binding

Runs 1 and 2 (blog template, social slide):

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
93c68159a50489b59ce86b3cc6221976210648ffd46d52e72fa6e39a1fc307eb  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
bbc376ee8c46bbf26fd5a962248866d8ddc508bae9a3db739806f697abd37f5a  references/runtime-verification.md
e96050d2b88d89eff417ce8537998dcba2f8fa4564dc3f8e5004e22a0d208a10  references/task-routing.md
13cdc981412da6323a263651eb9150b15212ef308694d7f257135406d1b27a81  references/version-and-migration.md
```

Runs 3 to 5 (reel subtitles, article spacing, deck review), at commit `a80c2f68d3bcd63927fafe1aae6b045b1a2a79f2`:

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
8156ef1fd556108388b3859db97bcca66d6bfa3c5613f8cbe6297719eda76682  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
90a40e27655ffc52bee48410f7fc428ebd97cf13c0c98db98634b5566b5748c9  references/runtime-verification.md
0be6323f4aa6f275fc0b2b8217e5dfa9a11d04cc31fe94c099fc6d99d14563ac  references/task-routing.md
13cdc981412da6323a263651eb9150b15212ef308694d7f257135406d1b27a81  references/version-and-migration.md
```

The shipped skill differs from these payloads only by the repairs listed under each "Changes after" section. Shipped:

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
8156ef1fd556108388b3859db97bcca66d6bfa3c5613f8cbe6297719eda76682  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
af63d6f7ace7e50234f53e7a3974b6d8f148bd3c69ff956363296882eae09f7e  references/runtime-verification.md
968a230180310541541f4db429fd99c9f138870eed0ab05a75537b304187ab1f  references/task-routing.md
1fa5d52276d1fff677b9fd91dcc38df0b236565f52826b9e38c920ca85405d21  references/version-and-migration.md
```

## Blog template before launch

A consumer pinned to v3.0.0 asked for its blog template to be verified before launch. An unlayered app rule removed the paragraph measure inside a 960 px column, the developer's note said "paragraphs look fine", and the hero headline's p touched the f on the line below.

The agent routed through the web branch to `docs/WEB-TEXT-WRAPPING.md` because the work sets paragraphs. It marked `body.reading` as a mismatch: the consumer rule overrides the role's measure and the lines exceed the character ceiling. The next check it named was to remove the override without changing the role, then count characters per rendered line at several widths. It marked the hero as a mismatch and proposed rewording or rebreaking the copy, noting that a line-height change would be a governed exception. It kept font loading, installed package and fallback states `unverified`, and it failed closed on source resolution because the release was still half-built in the working tree.

Observed invariant: "looks fine" and matching computed styles did not stand in for a counted line length or a visual collision check.

## Social slide that does not fit

A consumer pinned to v3.0.0 had a 1080 × 1350 carousel slide with 78 words of `social.body` overflowing the safe area. The designer proposed a local 22 px override because it was "still readable on my 27-inch monitor", and the user asked for the slide to be made to fit and exported.

The agent refused the override and did not export. It cited the 62-word limit in the copy contract, "Never shrink type to rescue excessive copy" in the social document, and the skill's rule against local role changes. It worked out that the override would show at about 8 px in a phone feed, against about 13 px for the governed role. It offered to cut the copy or move it to the caption or another slide, and it asked the user to choose, because wording and carousel structure are the user's call. It also failed closed on source resolution for the same half-built working tree.

Observed invariant: a size judged on a desktop monitor did not stand in for delivery size, and a fit problem stayed a copy problem.

## Changes after runs 1 and 2

- `docs/WEB-TEXT-WRAPPING.md` now states one target, 45 to 75 characters per line with 80 as the ceiling. The first run had to choose between several figures.
- A consumer rule that *removes* a role's measure now counts as a mismatch too, not only one that widens it.
- A display-line collision is reported as a mismatch with a proposed rewording or an allowed break, and the user approves copy changes. The first run was unsure whether a diagnosis may edit copy, and whether rebreaking conflicted with the wrapping document's limits on manual breaks.
- `docs/SOCIAL-TYPOGRAPHY.md` gives hard delivery minimums (11 px body, 8.5 px for the smallest roles at phone width), and the skill judges against "the delivery sizes the surface document gives". The second run found only approximate figures.
- A delivery-size failure is a mismatch with a proposal the user approves, rather than "a finding against the copy or the role".

Both runs also asked how to treat a dirty working tree, what "migration state" means when there is no migration, and which runtime list applies to HTML rendered to PNG. Before runs 3 to 5, the skill gained a rule that uncommitted changes in a canonical checkout are never a pin, migration state became `not applicable` when the pin does not change, and HTML rendered to a fixed-canvas file now gets the web checks on the page and the fixed-canvas checks on the file. None of the later runs raised these again.

## Subtitles for a vertical reel

A video team's notes pinned the system to commit `a80c2f6` for a 1080 × 1920 Reel cut in DaVinci Resolve. The editor had set yellow subtitles on a black box in PD Body SemiBold at 48 px, 120 px from the bottom, and said "48 px fits more words per line". One cue ran three lines in 1.2 seconds; another showed one word for 7.5 seconds. The user asked what to change before export.

The agent kept the locked commit as the pin, ran the verifier (523 passed) and routed through the shared, subtitle, native-file and review branches. It named yellow on black as the governed `cinema` style, raised the size to the frame's 67 px, and cited "never shrink the type" against 48 px, noting that keeping it would be a governed exception. It found the three-line cue over every limit (lines, characters, words, reading speed) and proposed a three-cue split and an earlier out-point for the long cue, stating that wording and timing belong to the transcript or the user, so it would propose and not edit. It kept font registration, style values and the other cues `unverified` and the exported frame `blocked`, since nothing was exported yet.

Observed invariant: a size chosen to fit more words stayed a copy problem, and copy and timing stayed the user's call.

## Spacing on a case-study page

A Next.js article pinned to the same commit set its own margins on headings, paragraphs and figures, giving each `h2` 64 px above and below. The developer asked whether raising the heading's line height to 1.3 would attach it to the text that follows.

The agent traced the cause to the app's unlayered margins overriding the system's layered flow rules, proposed `data-pd-flow` with the three margin rules removed, and listed the expected gap for each pair from the tokens. It refused the line-height change as a governed exception and explained that extra leading is added above and below equally, so it cannot attach a heading to what follows. It then failed closed: the narrow-viewport line heights and tracking in the hand-authored CSS were not recorded in the canonical tokens.

Observed invariant: a spacing complaint was answered with the spacing contract, not by changing a role.

## Deck review before a pitch

A 16:9 deck set in Google Slides, to be presented live and then emailed as a PDF, used a 24 pt headline, 11 pt body with 95 words on one slide, 7 pt sources and ad hoc gaps of 4 and 30 pt. The user asked whether the type was ready.

The agent answered "not ready". It found that Google Slides cannot load the PD families, so the deck shows a substitute font whatever its sizes; that 11 pt was the 2.x present size and 7 pt was below both densities; that 95 words exceed the present-density limit; and that the gaps matched no deck step. It proposed a present version and a read version, a rebuild in the starter deck or Keynote, and cut or split copy, all for the user to approve. It kept the rendered face, the PDF fonts and delivery size `unverified` with a next check for each.

Observed invariant: sizes that looked plausible in points were checked against the governed density, the font actually rendered, and the room.

## Changes after runs 3 to 5

- The narrow-viewport line heights and tracking are now canonical tokens (`narrowViewport` on the roles it changes, `web.narrowViewport` for the breakpoint), and the validator holds the CSS to them.
- A kicker takes the space before its heading, and a heading after a figure keeps its own larger space above. The runtime check counts a kicker as part of its heading. The spacing run found both cases breaking the "closer to the text after it" rule.
- `docs/SPACING.md` now covers headings that open a wrapper and warns that unlayered consumer margins override flow.
- The deck spacing token note and `docs/SPACING.md` agree (bullets and paragraphs `xs`, a headline to whatever follows `s`). `docs/DECKS.md` says limits are per element, covers a deck that is presented and then sent, and rounds point sizes without dropping below the floor.
- Task routing no longer offers Google Slides sizes as a way to set PD type; a Slides deck is a font mismatch.
- `docs/SUBTITLES.md` says the frame's character limit wins over the role's 42, that 16 words is per subtitle, that every character counts toward reading speed, where the bottom distance is measured, which line height and tracking to set when burning in, that the style list is advice, and what size subtitles show at on a phone. The vertical cue moved to 30 % up and 76 % wide, clear of the Reels and TikTok interface, with 24 characters per line; the guides behind that are recorded in `docs/RESEARCH-SOURCES.md`, and the subtitle route asks for a refresh when the platforms change.
- `version-and-migration.md` treats a locked commit with no published tag as a pin and reports the missing tag.
- The README says the font handoff keeps the version of the last release that changed a font.
