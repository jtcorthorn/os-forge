# Build or continue an OS

1. Resolve the owner's root, read its maps and contracts and use the setup questions in [SKILL.md](../SKILL.md). Present the starting structure and ask only about open choices. Preserve working folders, owner-authored instructions, generators and business boundaries. Check actual read/write access. Agree on one useful first result and the minimum sources needed. A family relationship does not grant access to another recipient's root or account.
2. Inventory explicit source paths before adding generated material:

```text
python <skill>/scripts/inventory.py --root <root> --source "Source folder" --source "Other folder" --output <root>/00_System/Intake/sources_YYYY-MM-DD.csv
```

Use a new filename for another run. Read errors are incomplete coverage. Do not inventory the whole root: backups, generated notes and extraction would become false originals. Technical sidecars are not evidence of missing original photos.

3. Copy `assets/instance.example.json` into recipient Intake; set a single-line `owner`. Infer the owner's working language from the conversation. Set `entry_language` to `en` or `es` for the supplied human entry guide. For another language, use a starter and translate it locally; translate other human-facing starter documents as needed. Technical system contracts remain English. Set `external_intake=true` when sources exist, and create recipient-owned Intake `MAPA.md`/`CONTEXT.md` with inventory, coverage and domain routes. With no sources, use `false` and choose one useful first task without inventing personal facts.
4. Set `domains` to the starter folders the owner wants, with their preferred display names. Omit the field to keep all legacy starters. An empty object creates just the common workspace and its playbooks. The example shows accepted folder keys; other starters are `10_Finances`, `40_Health`, `50_Learning`, `60_Travel`, `70_Records` and `90_Archive`. Display names change the maps and keep starter paths stable. Use the existing templates to create custom areas and link them from the root map. Keep coherent existing subtrees, including a differently named entry that its owner has declared and consumers still use. Apply actual renames through the authorized migration method.
5. Add local routes through `append`, a mapping from a selected blueprint-relative path to additional Markdown. Include a short owner-specific setup section in `EMPIEZA_AQUI.md` with the live areas, their first result and working links. Every appended path must be part of the rendered blueprint. Then preview and apply:

```text
python <skill>/scripts/forge.py deploy --config <root>/00_System/Intake/instance.json --target <root>
python <skill>/scripts/forge.py deploy --config <root>/00_System/Intake/instance.json --target <root> --apply
```

Every unmanaged collision blocks the entire apply, including identical bytes. For an existing unmanaged workspace, use the rendered blueprint in a temporary recipient as a source of starter files. Integrate the necessary routes into the actual owning maps, preserve existing instructions and copy only missing files within scope. Never manufacture a baseline to silence a conflict. Managed updates archive predecessors; unchanged upstream content preserves local edits. A removed starter leaves any deployed files in place. Both local and upstream changes require an explicit merge.

The recipient must be outside this skill and its ancestors. Private data never enters the public package. If deployment is blocked by a control collision, preparation inside the recipient can continue.

6. For physical organization use [organization](organization.md); for deeper evidence processing use [extraction](extraction.md). A map over scattered folders is insufficient when actual moves were requested.
7. Configure assistant and capability routes using the [bundled method](../assets/blueprint/00_System/Skills/agent-fleet/SKILL.md). Start with the current assistant loading the skill and owning contract directly. Add a dedicated agent only for an evidenced responsibility with its own mandate, context, continuity or review need. Record the role, handoff and probe when that responsibility calls for one.
8. Reuse valid notes and add small source-linked knowledge around real questions. Keep raw extraction separate from knowledge and current records. Do not produce a note per file solely to increase document count.
9. Verify active structure for a managed build:

```text
python <skill>/scripts/forge.py verify --target <root>
```

This checks managed files and local Markdown links in the standard areas. Walk the new routes in custom or unmanaged areas using the [maintenance playbook](../assets/blueprint/00_System/Skills/os-maintenance/SKILL.md). Check original hashes, Office dependencies, effective access and accuracy where the task calls for them. Retain historical snapshots in root `_archive/`.

10. Walk entry -> domain contract -> actual source -> useful answer or editable artifact. Compare one consequential synthesis with original content, verify original bytes, and exercise direct skill routing and any applicable handoff. Deliver the entry guide, knowledge and assistant routes, coverage and station requirements. Append owning history. For continuation, ask a fresh session to find the saved result from the root entry and domain map without giving its file path. Record missing runtime access as unverified rather than simulating a pass. Stop when the agreed acceptance passes; optional cleanup and dormant roles do not block use. Reopen for material new evidence or changed requirements.
