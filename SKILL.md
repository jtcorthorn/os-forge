---
name: os-forge
description: Build or extend a personal operating system from owner-provided files. Organize originals into an ICM workspace, extract searchable evidence, integrate source-linked knowledge, and configure a general assistant with shared skills and add dedicated agents where needed. Use when someone wants their own folder-based OS or wants to continue an existing one.
---

# OS Forge

Build a personal OS around the owner's work. Use the bundled ICM Architect method to give their files, projects, businesses and routines clear routes, ownership and a way to grow.

## Start with a short setup conversation

For a new OS or a structural change, show a proposed structure before writing. Use the owner's language. Offer starter areas such as projects, businesses, finance, travel and a library. Include other areas only when they fit the person's work. Explain in one sentence what goes where.

Ask together about the decisions still open:

1. Which areas would you keep, drop, rename or add?
2. Where should the OS live? Which existing folders or routes already work and should stay in place? Which areas are private or shared, and with whom?
3. What is the first task you want to do with your OS?

Use answers already provided and ask only for decisions still needed. Confirm the proposed structure with the owner when those choices are open. A clear request with the structure and scope already agreed is enough to proceed. For a routine task in an existing OS, use its current maps and skip setup.

## Compose the methods

This skill orchestrates the workflow. Load each applicable method directly in the assistant doing the work.

- **ICM Architect** is the structural foundation. Read the [bundled skill](assets/blueprint/00_System/Skills/icm-architect/SKILL.md), then its relevant form and migration references. Its MIT license travels with it. If the host already provides another version, choose and record one authority rather than silently mixing versions.
- **Agent Fleet** defines task routing and ownership. Read [the portable fleet method](assets/blueprint/00_System/Skills/agent-fleet/SKILL.md) to choose shared methods, optional specialist consultation or dedicated agents. One general assistant is the default.
- **OS maintenance** explains how to check routes, verify completed handoffs, preserve deliberate local conventions and rehearse recovery. Leave the [maintenance playbook](assets/blueprint/00_System/Skills/os-maintenance/SKILL.md) accessible from the owner's guide.
- For research, design, documents, spreadsheets, memory or recurring work, select only the relevant method from the [portable library](assets/blueprint/00_System/Skills/MAPA.md). These are on-demand methods, not dependencies that all need to be loaded or installed.

The supplied library makes the package self-contained. Standard skill folders use `SKILL.md`; links declare composition. Do not invent a host-specific automatic dependency resolver or claim a nested skill was automatically activated.

## Start with the owner and existing work

Resolve the target root and read its maps, contracts and rules before writing. Inspect the supplied sources and preserve useful existing records and generators. When a local convention differs from the starter, check the owner's contract and consumers that rely on it before proposing a change.

One authoritative home per fact. Company evidence belongs to that company; personal health, identity and finance remain in their personal domains. Unknown relationships stay unknown. Private sources, configs and extraction outputs stay in the recipient root, outside this public skill repository.

Read [build](references/build.md) for the end-to-end workflow; [organization](references/organization.md) for authorized physical moves; [extraction](references/extraction.md) for evidence processing. Follow the owner's existing authorization. A scaffold request alone does not authorize moves; an explicit reorganization request does. Prepare an exact migration map and recovery path before moving. Do not introduce repeated approval gates for already authorized technical steps.

## First useful implementation

For a new owner without a broader approved scope, start with one useful task and only its necessary sources. Keep originals in place. Use the current assistant and the relevant shared skill. Generate the neutral scaffold, then finish one useful task before expanding the inventory, connecting accounts or provisioning dedicated agents. Adapt to the owner's existing commitments when a broader build or reorganization was explicitly requested.

Confirm actual read/write capability before promising construction. A chat-only surface can prepare a proposal or files for download, but cannot certify a local deployment. Keep each recipient's root and accounts separate, including within a family; sharing the neutral method grants no access to another person's records.

## Use the factory and deterministic tools

`assets/blueprint/` contains neutral maps, contracts, personal domains, templates, memory, portable methods and optional role guides. Select and label the starter areas through the recipient's Intake configuration. See [the example](assets/instance.example.json). Use the existing templates and maps for additional areas. Configure company routes and register only roles with assigned responsibilities.

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

Deliver `EMPIEZA_AQUI.md` as the owner's short operating guide. Add their actual areas, where to put new material, how to resume their first project and what to ask the assistant to run the maintenance and Agent Fleet playbooks. Link working paths in the recipient OS. Include a knowledge entry, an assistant and capability entry, reproducible local search and concise coverage. Link claims to the dated original and its exact locator. Keep proposals, unsigned drafts, historical reports, stored calculations and current confirmed facts distinct.

Require original-byte verification for supplied originals, active navigation and one useful task walk. With no supplied files, record that coverage explicitly and complete an owner-chosen task without inventing personal facts. A new session should find the saved result through the entry and domain map, without a hint containing its exact path; if no new session is available, record continuation as unverified. Reopen only for a changed requirement or material new evidence. Do not hold a useful first implementation for historical cleanup or optional fleet expansion. Probe direct skill selection, context boundaries and any specialist handoff the owner needs. Record warm smoke checks, fresh-session behavior and real task results separately.

Report inventory, extraction, interpretation, runtime adoption and effective access separately. Images, scans, video and inaccessible pointers remain explicit gaps. Append the owning `_meta/BITACORA.md`, then close. Later intake processes only new/changed owner inputs, updates affected knowledge and preserves prior decisions.
