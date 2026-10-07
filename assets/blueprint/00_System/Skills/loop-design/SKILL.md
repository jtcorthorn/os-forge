---
name: loop-design
description: Decide whether recurring work merits automation, then design a bounded, observable flow with explicit owner, trigger, checks, and stop condition.
---

# Loop design

First test whether the work recurs often enough and has a stable enough input to justify automation. A one-off or relationship judgment may stay human-led. Estimate the effort saved and the new failure burden.

For a viable loop, specify: real trigger, authoritative input, accountable owner, allowed action, artifact or state change, quality check, failure route, and stop condition. Distinguish no new events from failed collection. Name the item key and check previous attempts before retrying, so external effects are not duplicated.

Set autonomy from verifiability, recoverability, authorization, and consequence. Make the smallest pilot that checks the full path. Record attempted actions separately from verified outcomes. Bound runtime, cost, retries, and alert volume. A pilot result does not grant deployment or scope expansion.

Use [references/loop-card.md](references/loop-card.md) to write a reviewable design. Do not claim monitoring or persistence until a trigger and executor are actually installed and observed.
