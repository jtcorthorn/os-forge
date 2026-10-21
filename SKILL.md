---
name: os-forge
description: Build or extend a personal operating system from owner-provided files. Organize originals into an ICM workspace, extract searchable evidence, integrate source-linked knowledge, and prepare a personal and company agent fleet. Use when someone wants their own folder-based OS or wants to continue an existing one.
---

# OS Forge

Turn the owner's files into an independent personal operating system they can keep building from their own station. Deliver navigable evidence, useful knowledge, editable records and a fleet with explicit roles and handoffs. This is a knowledge workspace, not a bootable computer OS.

## Compose the methods

This skill orchestrates the workflow. It does not replace its specialist methods.

- **ICM Architect** is the structural foundation. Read the [bundled skill](assets/blueprint/00_System/Skills/icm-architect/SKILL.md), then its relevant form and migration references. Its MIT license travels with it. If the host already provides another version, choose and record one authority rather than silently mixing versions.
- **Agent Fleet** is a required construction stage. Read [the portable fleet method](assets/blueprint/00_System/Skills/agent-fleet/SKILL.md) to build the personal fleet and company-owned specialists, access scope, handoffs, model policy and activation evidence.
- For research, design, documents, spreadsheets, memory or recurring work, select only the relevant method from the [portable library](assets/blueprint/00_System/Skills/MAPA.md). These are on-demand methods, not dependencies that all need to be loaded or installed.

The supplied library makes the package self-contained. Standard skill folders use `SKILL.md`; links declare composition. Do not invent a host-specific automatic dependency resolver or claim a nested skill was automatically activated.

## Start with the owner and existing work

Resolve the target root and read its maps, contracts and rules before writing. Inspect actual supplied sources; preserve useful existing records and generators. Ask only for missing facts that change correctness, authority or ownership. Infer domains from evidence rather than copying another person's business structure.

One authoritative home per fact. Company evidence belongs to that company; personal health, identity and finance remain in their personal domains. Unknown relationships stay unknown. Private sources, configs and extraction outputs stay in the recipient root, outside this public skill repository.

Read [build](references/build.md) for the end-to-end workflow; [organization](references/organization.md) for authorized physical moves; [extraction](references/extraction.md) for evidence processing. Follow the owner's existing authorization. A scaffold request alone does not authorize moves; an explicit reorganization request does. Prepare an exact migration map and recovery path before moving. Do not introduce repeated approval gates for already authorized technical steps.

## First useful implementation

For a new owner without a broader approved scope, start with one useful task and only its necessary sources. Keep originals in place. The neutral scaffold and prepared role cards can be generated together; do not require a full digital-life inventory, account connections, separate agents or specialist customization before the first result. Use the current assistant sequentially. Adapt to the owner's existing commitments when a broader build or reorganization was explicitly requested.

Confirm actual read/write capability before promising construction. A chat-only surface can prepare a proposal or files for download, but cannot certify a local deployment. Keep each recipient's root and accounts separate, including within a family; sharing the neutral method grants no access to another person's records.

## Use the factory and deterministic tools

`assets/blueprint/` contains neutral maps, contracts, personal domains, templates, memory, portable methods and six general fleet roles. Adapt it with an owner configuration inside the recipient's Intake folder; see [the example](assets/instance.example.json). Configure actual company routes and fleets from evidence. Existing local work is not disposable.

Resolve every helper from this skill's absolute directory, regardless of shell working directory. `<skill>` and `<root>` in examples are notation, not executable values. Discover the host's Python, tools and models; never assume a particular drive, account or model.

| Need | Helper |
|---|---|
| Preview/apply a conflict-aware deployment | `scripts/forge.py` |
| Inventory explicitly named originals | `scripts/inventory.py` |
| Preview/back up/relocate an exact file plan | `scripts/relocate_sources.py` |
| Compare inventory with actual original bytes | `scripts/verify_sources.py` |
| Extract text and stored spreadsheet cells | `scripts/extract_sources.py` |
| Recover sparse XLSX cells | `scripts/extract_sparse_xlsx.py` |
| Search bounded excerpts with source locators/hashes | `scripts/search_extracted.py` |

See [runtime requirements](references/runtime.md). Use deterministic helpers for mass processing; reserve model context for domain judgment and source-based synthesis. Delegate only when authorized and useful; one writer per scope. Preserve originals and prior controls. No deduplication/deletion, business-model recalculation, external publication, account connection or scheduler activation is implied.

## Accept and deliver

Deliver `EMPIEZA_AQUI.md` in the owner's language, a knowledge entry, a fleet entry, reproducible local search and a concise coverage/exception record. Claims link to originals with dates/versions and exact page, paragraph, sheet/cell or slide locators. Keep proposals, unsigned drafts, historical reports, stored calculations and current confirmed facts distinct.

Require original-byte verification for supplied originals, active navigation and one useful task walk. With no supplied files, record that coverage explicitly and complete an owner-chosen task without inventing personal facts. A new session should find the saved result through the entry and domain map, without a hint containing its exact path; if no new session is available, record continuation as unverified. Reopen only for a changed requirement or material new evidence. Do not hold a useful first implementation for historical cleanup or optional fleet expansion. Probe the fleet's routing, context boundaries and handoff behavior; report warm smoke tests separately from independent runtime probes. Role cards are prepared assets, not proof of autonomous workers.

Report inventory, extraction, interpretation, runtime adoption and effective access separately. Images, scans, video and inaccessible pointers remain explicit gaps. Append the owning `_meta/BITACORA.md`, then close. Later intake processes only new/changed owner inputs, updates affected knowledge and preserves prior decisions.
