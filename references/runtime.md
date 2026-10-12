# Host requirements

Use a file-capable agent with authorized read/write access to the selected root and Python 3.10+. Generator, inventory, relocation, verification, sparse XLSX and search use the standard library. Embedded PDF/XLSX extraction optionally uses PyMuPDF (or pypdf) and openpyxl. DOCX/PPTX/plain text use standard-library parsing. Missing dependencies are per-format gaps.

`requirements-extraction.txt` lists optional parser packages. When installation is authorized and useful, select an isolated environment for the station:

```text
python -m venv <environment-folder>
<environment-python> -m pip install -r <skill>/requirements-extraction.txt
```

Discover the actual executable; syntax depends on the host. Do not assume an account, machine path, bundled runtime, browser or model. Core construction works without external connectors. Web/account tasks require the host's actual tools and owner authorization.

Keep the whole skill folder together. For Codex, place it in the configured skills directory. For another file-capable agent, provide SKILL.md explicitly and follow the host's own discovery mechanism. Nested blueprint skills are methods available by reading their entries; automatic discovery is unverified until tested on that host.

Fleet role cards describe responsibility and scoped behavior. Real delegation requires an available executor and authorization. One assistant can work sequentially through roles; it must not claim those are independently running agents. Activation evidence, model choice, mounts and access tests stay in the recipient OS.


## Hosted maintenance and destination checks

Some hosted schedulers omit a worker ID from run context. Require the exact owner-approved configured ID, a fresh unique enabled cloud attachment, matching controller and account, and the same saved responsibility. If host-supplied identity is present, it must match. Missing optional metadata alone should not block an otherwise verified binding; absent or mismatched authority still stops work. Verify actual source access and immutable result readback after correcting startup. A source-only run or an already-synchronized publication does not establish a successful repair and changed-publication cycle.

Before filing through a connector, resolve the full destination ancestry and parent identity against the owning map, then verify them again after writing. Similar folder names under different roots are different destinations. A specifically authorized stray-folder sensor may inspect only that branch within existing budgets. Hash every candidate against the canonical original and preserve unique or conflicting files. Retain exact duplicates under the owning recovery rules; never expand a canonical-root executor to move external paths automatically. Reconcile prior receipts and the current destination before retrying, including preserved recovery folders.

Use original file bytes for governed methods and skill packages. Extracted Markdown may remove frontmatter or alter tables. Installed instructions, parser binaries, host discovery and actual task use are separate dependencies. Download signed files with shell tracing and terminal echo disabled; keep temporary credentials out of tool output and evidence.


Pinned dependencies require a complete approved change handoff. When a policy or governed method changes, identify the deployments that pin its raw bytes and reconcile those references in the same authorized delivery. A hosted hash mismatch must stop writes. An authorized repair compares the actual approved changes, preserves executor scope and prohibitions, archives the old deployment, updates only the dependent reference and reads it back on the scheduled surface. Never accept a new hash automatically or roll back an approved source merely to pass preflight. Record reference reconciliation separately from a subsequent successful hosted run.
