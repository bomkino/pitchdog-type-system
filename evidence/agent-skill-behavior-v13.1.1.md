# Agent Skill behaviour evidence — v13.1.1

Date: 3 September 2026

Three independent Codex agents received the candidate skill, one realistic request, and only the artifacts needed for that branch. They made no edits. These are decision-level runs, not user acceptance or a substitute for testing a real consumer.

## Candidate binding

The agents read this exact skill payload:

```text
2d12b38012c5f5676aeb43b856aa21fa57b4904549b3866b73a4fd1e2d6406e8  NOTICE.md
2c4fd124fd121f6436d80b8c6dfff59707d2396a59275d44081988ee4dc85961  SKILL.md
b2cb2eb6c827529925d3c476d202e41bffe0329d4a036ada9351ee2bdeb09064  agents/openai.yaml
c79215bca7b34baaee62565f3d2f10a49ec87d1d519a57a6cb36f18765f43b95  references/runtime-verification.md
a707cb8c86980cc9e9da27ec61a6563bbd54f14d2949e9a84168b0335f4cd2c7  references/task-routing.md
f00492eba6c7c57d37e83114ef1aed0aead352ea753919e1f24063397fa2c23c  references/version-and-migration.md
```

## Existing pinned consumer

The consumer requested UI type changes and explicitly ruled out an upgrade. The agent preserved the existing release tag, resolved it to its full commit, consulted that commit rather than the newer checkout, selected semantic UI roles from the pinned contracts, and left implementation and runtime state unverified because the fixture contained no component or runnable application.

Observed invariant: ordinary type work did not become an unauthorized migration.

## Contradictory “latest”

The new consumer requested the latest production system. Live GitHub exposed a stable Release whose immutable source still said candidate, plus a newer tag with no Release and conflicting candidate/production records. The agent selected neither, changed nothing, and named the repair: publish a new commit, tag, and Release with aligned source metadata.

Observed invariant: a tidy endpoint did not overrule contradictory source evidence.

## Runtime font diagnosis

The fixture reported a successful build, one failed font request, fallback computed type, and synthesis enabled. The agent kept the build, asset request, aggregate font-set status, computed declarations, actual rendered face, and semantic-role fit as separate states. It identified both a broken asset path and an absent or overridden typography layer as likely causal, then requested manifest hash checks, matched-rule inspection, per-face loading, and rendered-font readback.

Observed invariant: build success did not become runtime proof, and a missing font did not explain away a separate cascade mismatch.
