## Learned User Preferences

- Default to running the Critical Project Risk Radar workflow first when the user says to run radar.
- Use `openbot` as the canonical bot name and avoid deprecated names like clawdbot, clawd, or callbot.
- Keep project operations organized and consolidated rather than split across scattered locations.
- Keep ongoing project-status updates ready for Notion sync workflows, with Trade Show contacts tracked in Notion.
- Keep Trade Show and UGC tracking separated rather than mixing them into one Notion target.
- When the user asks for a direct answer or rundown, lead with the immediate answer first and avoid extra detours.
- When the user says "take over," execute end-to-end autonomously and only pause for true blockers.
- Prefer Telegram-first, one-tap UX for operational workflows (contact picking, call templates, follow-up actions) over command-heavy flows.
- Ensure outbound call workflows always provide clear in-chat feedback and easy status retrieval.
- When architecture confusion appears, explicitly confirm whether capabilities are the same runtime or a separate project, and map myOshee voice work to the Telegram `openbot` runtime.
- Before implementing new work, confirm what is already implemented and avoid re-implementing completed measures.
- When the user asks to hold off or avoid changes, provide verification/status checks without making code edits, and prioritize confirming work is saved/not regressed.

## Learned Workspace Facts

- The workspace centers on `flywithpeggs.com` and related self-hosted infrastructure operations.
- The active replacement host for Citadelle routing is `breathless-macbook-air.tail030c2b.ts.net`.
- The VPN network now includes a Raspberry Pi node named `altidor-pi`.
- Local AI orchestration relies on shell commands in `.zshrc` including `bugscan`, `find-code`, `mem-index`, and `zreload`.
- Local model tooling includes Ollama with `qwen3:8b` for audits and `nomic-embed-text` for embeddings.
- Incremental continual-learning state is tracked at `.cursor/hooks/state/continual-learning-index.json`.
- `openbot` includes separate Trade Show Intel and UGC workflows, and current operations are aligning each to distinct Notion databases.
- `openbot` is the single active runtime, with Telegram and Twilio acting as interfaces into the same core bot.
- Call feedback is expected both in Telegram and via call-history/status retrieval endpoints.
- The active Openbot web endpoint is `https://openbot.flywithpeggs.com`.
- Finance capability for myOshee (budget/debt/savings/stocks/crypto/credit) is an active build focus.
- The Telegram myOshee runtime codebase is under `/Users/peggs/Projects/openbot`.
