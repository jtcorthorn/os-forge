# OS maintenance checklist

## Review an active area

1. Use the root and area maps to find one important record. Open the source, check which decision or version is current and compare it with the result the OS presents.
2. For a handoff, follow the trigger, responsible person or assistant, intended output and receiving destination. Read back the expected result at the destination. Reconcile an uncertain outcome before retrying so a retry cannot duplicate the delivery.
3. Check apparent layout issues against the owner's documented convention and the consumers that rely on it. Record a valid local convention with its source and reason. Ask the owner about an undeclared convention before proposing a move.
4. Add a short entry in the owning history with the date, checked route, observed evidence, owner and next action. State which areas or systems were inaccessible. On a repeat review, identify new, resolved and still-open findings.

## Repair a move or runtime change

1. Confirm current authority in the root map and owning contract.
2. Inventory affected paths, inbound references, generated outputs, external consumers, and case-folded destination collisions.
3. Preserve/version originals. Copy to destination, compare hashes or content and counts as appropriate, then update active references.
4. Verify the user-visible behavior in its actual runtime. A successful local write is only local evidence.
5. Record coverage and access limits separately. Append deliverable history in the owning project.
6. Stop when the accepted behavior works; do not expand into historical cleanup unless it affects current use or unique recovery.

For destructive or external effects, apply the owner's approval boundary before the effect.

## Rehearse recovery

When the change could interrupt an important route, restore the previous version into a temporary copy. Check content or hashes and walk the restored route. Note the backup, recovery steps and observed result. Leave the live workspace untouched during the rehearsal.
