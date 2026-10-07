---
name: agent-reach
description: Retrieve public web and platform evidence using the authorized tool available in the current runtime. Use for internet research, URLs, social discussion, video transcripts, and developer sources.
---

# Agent Reach: portable retrieval router

This package is a portable adapter to the Agent Reach method, not an installed CLI or account configuration. Before retrieval, inspect the tools actually available and the account or browser surface authorized for this task. An unavailable backend is a coverage limit; do not imply that another backend ran.

## Route

- General web or a URL: use the runtime web search/open tool; prefer direct publisher pages. For a cited page, capture its URL, publisher, publication/update date, and retrieval date.
- Developer questions: use the official docs or source repository first. Search issues only when the question concerns observed behavior or workarounds.
- Social platforms: use the platform connector or permitted browser session. Read actual posts and dates; search snippets alone support only a search-result claim.
- Video or podcast: use an official transcript when available. If transcription is generated, label it as such and spot-check consequential passages.
- A source behind login or unavailable in this runtime: ask only for access that materially changes the result, or continue with an explicitly narrower claim.

For broad research, select channels by the question. Cross-check independent sources and record missing channels. Do not treat popularity, repeated syndication, or multiple search hits as independent confirmation. Use read-only retrieval unless the user separately authorizes posting, messaging, following, or other external effects.

Read [references/channel-checks.md](references/channel-checks.md) for platform-specific verification and [references/dependency-setup.md](references/dependency-setup.md) when setting up an optional CLI or connector. Never copy cookies, tokens, browser profiles, or machine-specific configuration into the skill package.
