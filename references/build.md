# Build or continue an OS

1. Resolve the owner's root; read existing maps/contracts. Inspect original folders and current outputs. Preserve existing human-authored records, active generators and business boundaries. For a new owner, agree one useful first result and the minimum evidence needed to accept it. Check actual read/write access. Without a broader requested scope, use only the sources needed for that task, keep originals in place and work through the current assistant. A family relationship does not grant access to another recipient's root or account.
2. Inventory explicit source paths before adding generated material:

```text
python <skill>/scripts/inventory.py --root <root> --source "Source folder" --source "Other folder" --output <root>/00_System/Intake/sources_YYYY-MM-DD.csv
```

Use a new filename for another run. Read errors are incomplete coverage. Do not inventory the whole root: backups, generated notes and extraction would become false originals. Technical sidecars are not evidence of missing original photos.

3. Copy `assets/instance.example.json` into recipient Intake; set a single-line `owner`. Infer the owner's working language from the conversation. Set `entry_language` to `en` or `es` for the supplied human entry guide. For another language, use a starter and translate it locally; translate other human-facing starter documents as needed. Technical system contracts remain English. Set `external_intake=true` when sources exist, and create recipient-owned Intake `MAPA.md`/`CONTEXT.md` with inventory, coverage and domain routes. With no sources, use `false` and choose one useful first task without inventing personal facts.
4. Infer company boundaries and useful workflows. Keep coherent existing subtrees; avoid path-length overflow. Preserve and merge existing root instructions rather than blindly replacing them.
5. Add local routes through `append`, a mapping from an existing blueprint-relative path to additional Markdown. It cannot add arbitrary new blueprint files. Then preview and apply:

```text
python <skill>/scripts/forge.py deploy --config <root>/00_System/Intake/instance.json --target <root>
python <skill>/scripts/forge.py deploy --config <root>/00_System/Intake/instance.json --target <root> --apply
```

Every unmanaged collision blocks the entire apply, including identical bytes. Preserve originals before an approved control replacement. Never manufacture a baseline to silence a conflict. Subsequent managed updates archive predecessors; unchanged upstream content preserves local edits. Both local and upstream changes require an explicit merge.

The recipient must be outside this skill and its ancestors. Private data never enters the public package. If deployment is blocked by a control collision, preparation inside the recipient can continue.

6. For physical organization use [organization](organization.md); for deeper evidence processing use [extraction](extraction.md). A map over scattered folders is insufficient when actual moves were requested.
7. Build the fleet using the [bundled method](../assets/blueprint/00_System/Skills/agent-fleet/SKILL.md). Keep six general roles available as prepared methods, then add only evidenced company specialists. A first implementation can use the coordinator and relevant method sequentially in one assistant; do not require separate runtime setup or personalized cards for every role before useful work. Include a routing table, role cards, delegated-work template, model policy and probes. Names/personas are optional owner decisions; libraries do not need agents.
8. Reuse valid notes and add small source-linked knowledge around real questions. Keep raw extraction separate from knowledge and current records. Do not produce a note per file solely to increase document count.
9. Verify active structure:

```text
python <skill>/scripts/forge.py verify --target <root>
```

This checks managed files and local Markdown links, not original hashes, Office dependencies, cloud access or semantic accuracy. Check meaningful properties separately. Retain historical snapshots in root `_archive/` so obsolete links are not mistaken for active routes.

10. Walk entry -> domain contract -> actual source -> useful answer or editable artifact. Compare one consequential synthesis with original content, verify original bytes, and exercise fleet routing/handoff. Deliver entry guide, knowledge/fleet routes, coverage and station requirements. Append owning history. For continuation, ask a fresh session to find the saved result from the root entry and domain map without giving its file path. Record missing runtime access as unverified rather than simulating a pass. Stop when the agreed acceptance passes; optional cleanup and dormant roles do not block use. Reopen for material new evidence or changed requirements.
