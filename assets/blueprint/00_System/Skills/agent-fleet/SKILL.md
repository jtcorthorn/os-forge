---
name: agent-fleet
description: Design and prepare a personal or company agent fleet inside an ICM workspace. Define a coordinator, task-specific specialists, context boundaries, deliverables, handoffs, model-capability policy and activation probes. Use when building an OS fleet or extending an existing fleet with a real new responsibility.
---

# Agent Fleet

Give the OS an explicit working organization. One coordinator owns the outcome; specialists own concrete jobs with scoped inputs and checkable outputs. A fleet may operate sequentially through one assistant or through separately executed agents when the host supports authorized delegation. State which mode actually occurred.

## Establish ownership and topology

Read root MAPA and the selected domain contracts. Personal coordination lives in `00_System/Agents/`. Company fleets live in their company's `_agents/`; personal fleet entries link to them without copying private company context. Real team/management restrictions require separate authorized mounts and effective-access checks. A folder called Management does not establish access control.

For a first useful implementation, one assistant may perform the task sequentially while unused cards remain prepared. Do not require independent workers, personalized personas or runtime setup for every role before delivering that result.

Keep the six supplied general roles as available methods: coordinator, architect, maintainer, designer, researcher and council. Add company leads/specialists only for jobs evidenced by the company's actual work. Libraries and empty speculative domains do not need personas. Named characters are optional and belong to the accountable operator; neutral role names are a useful default. Do not simulate real employees or invent an operator's approval.

## Required fleet artifacts

Use the recipient templates under `_templates/agents/`.

- Personal `00_System/Agents/FLEET.md` routes general roles and company-owned fleets.
- Each active company gets `_agents/FLEET.md` and a lead card plus one card per real specialist responsibility. Link the fleet from the company's map/entry, so a cold start discovers it.
- Each card records accountable human owner (or unknown), purpose, read scope, exclusive write scope, outputs, allowed actions, escalation conditions, skill routes, model-capability policy and actual runtime state/evidence.
- Record shared working posture: source-based claims, explicit assumptions, reversible local drafts and decisions by the accountable human. Specialist voice is expressed through what it checks first, not decorative personality.
- Use one handoff contract and one probe record. Keep evidence with the owning domain, not duplicated in a global memory.

The role card is authoritative for responsibility; the fleet table routes to it. Do not maintain competing config/registry copies of the same role details.

## Select roles and models economically

Start with the coordinator to identify goal, authority and acceptance. Use the relevant specialist when its contract helps. Broad system/ownership decisions need strong judgment; source-based analysis/writing needs a capable executor; bounded classification/formatting can use a smaller model when deterministic checks detect meaningful errors. Scripts do mass hashing, extraction, copying and comparisons.

Discover actual available models and user preferences. Choose the least costly capable option without inventing prices, model availability or identity. Record selected model/executor when verifiable. If no choice exists, keep a capability recommendation and use the available assistant honestly.

Delegate only when authorized and independent work justifies overhead. Assign each worker goal, inputs, write scope, permitted actions, acceptance evidence, budget/stop conditions and exact return format. Do not assign multiple writers to the same file. The coordinator integrates after rereading shared state. A handoff carries current authority, completed evidence, remaining work and exact next step; ask the human to relay messages only when no authorized coordination mechanism exists.

When working through one assistant, identify the current role when helpful, but do not describe role switching as independent agents, votes or verification. Deliver one coherent answer. Preserve source ownership when integrating specialist outputs.

## State, activation and probes

Use evidence-based states: `prepared` (card exists), `installed` (specific host discovers/loads it), `probed` (dated behavior observed), `in_use` (real dated output), `dormant`. Record executor, date, input, output and limitations for transitions; do not advance on a declaration alone.

Probe a cold start, task routing, sensitive-context boundary, delegation/handoff and failure/stop route. At least one actual task must reach a useful artifact in the allowed write scope. An agent that wrote the rules can run a warm smoke check; independent probes require another runtime/session with no inherited answer. Lack of an independent runtime is a clearly stated limit, not grounds to invent a pass.

Cards and prepared probes are sufficient to deliver a fleet ready for adoption. Autonomous execution, recurring scheduling, cloud mounts and external actions need actual mechanisms and explicit authority. Preparation does not deploy a background process.

Close useful outputs in their domain and append `_meta/BITACORA.md`. Expand the fleet only when a new observed job needs it; do not add agents merely to make an org chart look complete.
