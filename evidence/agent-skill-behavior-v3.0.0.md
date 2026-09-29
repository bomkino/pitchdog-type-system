# Agent Skill behaviour evidence — v3.0.0

Date: 29 September 2026

Two independent Claude agents received the candidate skill, one realistic request and a described fixture. They made no edits. These are decision-level runs of the rendered-type checks added in 3.0.0, not user acceptance or a substitute for testing a real consumer. Both ran while the 3.0.0 release was still being prepared in the working tree.

## Candidate binding

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
93c68159a50489b59ce86b3cc6221976210648ffd46d52e72fa6e39a1fc307eb  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
bbc376ee8c46bbf26fd5a962248866d8ddc508bae9a3db739806f697abd37f5a  references/runtime-verification.md
e96050d2b88d89eff417ce8537998dcba2f8fa4564dc3f8e5004e22a0d208a10  references/task-routing.md
13cdc981412da6323a263651eb9150b15212ef308694d7f257135406d1b27a81  references/version-and-migration.md
```

The shipped skill differs from this payload only by the wording repairs listed under "Changes after the runs".

## Blog template before launch

A consumer pinned to v3.0.0 asked for its blog template to be verified before launch. An unlayered app rule removed the paragraph measure inside a 960 px column, the developer's note said "paragraphs look fine", and the hero headline's p touched the f on the line below.

The agent routed through the web branch to `docs/WEB-TEXT-WRAPPING.md` because the work sets paragraphs. It marked `body.reading` as a mismatch: the consumer rule overrides the role's measure and the lines exceed the character ceiling. The next check it named was to remove the override without changing the role, then count characters per rendered line at several widths. It marked the hero as a mismatch and proposed rewording or rebreaking the copy, noting that a line-height change would be a governed exception. It kept font loading, installed package and fallback states `unverified`, and it failed closed on source resolution because the release was still half-built in the working tree.

Observed invariant: "looks fine" and matching computed styles did not stand in for a counted line length or a visual collision check.

## Social slide that does not fit

A consumer pinned to v3.0.0 had a 1080 × 1350 carousel slide with 78 words of `social.body` overflowing the safe area. The designer proposed a local 22 px override because it was "still readable on my 27-inch monitor", and the user asked for the slide to be made to fit and exported.

The agent refused the override and did not export. It cited the 62-word limit in the copy contract, "Never shrink type to rescue excessive copy" in the social document, and the skill's rule against local role changes. It worked out that the override would show at about 8 px in a phone feed, against about 13 px for the governed role. It offered to cut the copy or move it to the caption or another slide, and it asked the user to choose, because wording and carousel structure are the user's call. It also failed closed on source resolution for the same half-built working tree.

Observed invariant: a size judged on a desktop monitor did not stand in for delivery size, and a fit problem stayed a copy problem.

## Changes after the runs

- `docs/WEB-TEXT-WRAPPING.md` now states one target, 45 to 75 characters per line with 80 as the ceiling. The first run had to choose between several figures.
- A consumer rule that *removes* a role's measure now counts as a mismatch too, not only one that widens it.
- A display-line collision is reported as a mismatch with a proposed rewording or an allowed break, and the user approves copy changes. The first run was unsure whether a diagnosis may edit copy, and whether rebreaking conflicted with the wrapping document's limits on manual breaks.
- `docs/SOCIAL-TYPOGRAPHY.md` gives hard delivery minimums (11 px body, 8.5 px for the smallest roles at phone width), and the skill judges against "the delivery sizes the surface document gives". The second run found only approximate figures.
- A delivery-size failure is a mismatch with a proposal the user approves, rather than "a finding against the copy or the role".

Both runs also asked how to treat a dirty working tree, what "migration state" means when there is no migration, and which runtime list applies to HTML rendered to PNG. Those sentences predate 3.0.0 and were left for a separate pass.
