---
name: skill-improvement
description: Improve an existing skill after observed friction or repeated successful technique, with a bounded change and realistic evaluation.
---

# Skill improvement

Capture the concrete task, expected behavior, observed output, and source evidence. Determine whether the cause sits in the skill, runtime, tool access, user input, or a one-off mistake. Do not turn one incident into a permanent universal rule without a causal case.

Propose the smallest change that would alter future behavior. Keep the entrypoint concise and place conditional detail in references. Check for overlap with another skill and preserve the owner's existing conventions. Treat private examples as data to sanitize, not portable instructions.

Test against the original failure and at least one normal case when the change could over-trigger. Compare real outputs, not simulated claims of success. Check that linked references resolve and that installation, discovery, invocation, and improved result are distinct observations. Version the source and record the changed decision. Do not silently alter global policy or installed packages.

For byte-level upstream inspection and explicit runtime evidence, use the sibling
[skill-maintenance](../skill-maintenance/SKILL.md) helper. It preserves local adaptations,
distinguishes repository movement from changed skill content, and keeps reading separate from
attested application and checked properties. A passed byte check is not evidence of better
judgment or consumer usefulness; keep that evaluation with the owning task.
