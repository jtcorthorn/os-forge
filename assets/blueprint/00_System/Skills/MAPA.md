# Portable skills library

Status: packaged on 2026-10-03; not installed or runtime verified. These are methods for the recipient OS. Each folder contains a `SKILL.md` entrypoint; read only the relevant skill and its linked references.

| Need | Skill |
|---|---|
| Structure a folder-based workspace or map a system | [ICM architect](icm-architect/SKILL.md) (complete MIT-licensed package) |
| Prepare personal/company roles, context boundaries and handoffs | [Agent Fleet](agent-fleet/SKILL.md) |
| Retrieve web, social, developer, or media evidence | [Agent Reach](agent-reach/SKILL.md) (portable adapter) |
| Research and trace claims to sources | [Evidence research](evidence-research/SKILL.md) |
| Create a visual direction | [Visual design](visual-design/SKILL.md) |
| Build documents, spreadsheets, slides, or PDFs | [Documents](document-craft/SKILL.md), [Spreadsheets](spreadsheet-craft/SKILL.md), [Presentations](presentation-craft/SKILL.md), [PDFs](pdf-craft/SKILL.md) |
| Decide whether and how to automate recurring work | [Loop design](loop-design/SKILL.md) |
| Pressure-test a consequential decision | [Decision council](decision-council/SKILL.md) |
| Match an author's voice or explain technical work | [Writing calibration](writing-calibration/SKILL.md), [Explain clearly](explain-clearly/SKILL.md) |
| Capture knowledge or hand off work | [Knowledge capture](knowledge-capture/SKILL.md), [Task checkpoint](task-checkpoint/SKILL.md) |
| Improve a skill or maintain an OS | [Skill improvement](skill-improvement/SKILL.md), [OS maintenance](os-maintenance/SKILL.md) |

## Runtime dependencies

| Capability | Package state | Runtime check |
|---|---|---|
| Markdown skills and ICM templates | Packaged | Host must discover/read the library |
| Web and social retrieval | Adapter packaged | Inspect authorized connectors, browser, or optional Agent Reach CLI per channel |
| Document, spreadsheet, presentation, PDF editing | Methods packaged | Inspect native editors/libraries, fonts, renderers, and target format support |
| Scheduled execution or background monitoring | Design method packaged | Needs a real trigger, executor, authorization, and observed run |
| Cross-session memory or knowledge store | Capture method packaged | Needs an authoritative destination and write permission |

No package includes credentials, account configuration, installed binaries, vendor-bundled runtime, or a claim of app installation. See [PROVENANCE.md](PROVENANCE.md) for portable source and license notes.
