# Optional dependency setup

The skill works through a runtime's existing web tools; no CLI is bundled. Agent Reach upstream: https://github.com/Panniantong/Agent-Reach . Its `doctor --json` command can report installed backends if the CLI is present. Do not assume its output, platform count, or integrations before running it.

If a task specifically needs an unavailable channel, prefer the runtime's approved connector or browser. Install a CLI only when authorized and appropriate to the current host. Follow the upstream installation guide for current commands and license. Keep authentication in the tool's supported secure store, never in this package. Verify one read-only request after setup, and label any untested channel as unverified.

This portable adapter intentionally contains no cookies, API keys, account IDs, browser profiles, local config, or platform-specific command catalog that could go stale.
