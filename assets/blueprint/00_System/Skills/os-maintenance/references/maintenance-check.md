# Maintenance check for moves and runtime changes

1. Confirm current authority in the root map and owning contract.
2. Inventory affected paths, inbound references, generated outputs, external consumers, and case-folded destination collisions.
3. Preserve/version originals. Copy to destination, compare hashes or content and counts as appropriate, then update active references.
4. Verify the user-visible behavior in its actual runtime. A successful local write is only local evidence.
5. Record coverage and access limits separately. Append deliverable history in the owning project.
6. Stop when the accepted behavior works; do not expand into historical cleanup unless it affects current use or unique recovery.

For destructive or external effects, apply the owner's approval boundary before the effect.
