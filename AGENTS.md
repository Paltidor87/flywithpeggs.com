## Learned User Preferences

- Default to running the Critical Project Risk Radar workflow first when the user says to run radar.
- Use `openbot` as the canonical bot name; treat `clawdbot`, `clawd`, and `callbot` as legacy labels only—files or UI may still use old names, but the only active bot is openbot.
- Keep project operations organized and consolidated rather than split across scattered locations.
- Keep ongoing project-status updates ready for Notion sync workflows, with Trade Show contacts and UGC tracked in separate Notion targets.
- When the user asks for a direct answer or rundown, lead with the immediate answer first, avoid extra detours, and for dashboard troubleshooting inspect the live on-screen UI state before prescribing steps.
- When the user says "take over," execute end-to-end autonomously and only pause for true blockers.
- Prefer Telegram-first, one-tap UX for operational workflows (contact picking, call templates, follow-up, clear in-chat call feedback, and easy status retrieval) over command-heavy flows.
- When architecture confusion appears, explicitly confirm whether capabilities are the same runtime or a separate project, and map myOshee voice work to the Telegram `openbot` runtime.
- Before implementing new work, confirm what is already implemented and avoid re-implementing completed measures.
- When the user asks to hold off or avoid changes, provide verification or status checks without making code edits, and prioritize confirming work is saved and not regressed.
- When the user has stacked or partially committed local edits, prefer safe merges and explicit regression checks before committing instead of resets that drop in-progress work.
- Prefer concise, factual responses without human roleplay, heavy emotional framing, or unnecessary apologies.

## Learned Workspace Facts

- The workspace centers on `flywithpeggs.com` and related self-hosted infrastructure operations. Treat **`/Users/peggs/Projects/openbot`** as part of the same operational picture as this repo—do not treat the workspace folder as a hard boundary when answering about bots, Twilio, or infra.
- The active replacement host for Citadelle routing is `breathless-macbook-air.tail030c2b.ts.net`. SSH **`breathlessserver`** (Tailscale `100.123.242.58`, user `breathlessserver`) is the same Mac used for Citadelle-style home infra.
- **Production VPS (“citadelle”):** **`root@187.77.15.53`** (public). SSH config may use **`vps`** (same host) and **`vps-ts`** (Tailscale **`100.106.193.70`**). **Openbot** runs in **Docker** (`openbot` container) on host port **8090**; public **`https://openbot.flywithpeggs.com`** depends on Cloudflare Tunnel **`openbot-tunnel`** being healthy (another tunnel does not substitute). This VPS is **not** the breathless Mac and **not** the Altidor IVR Node app on port 3000.
- **Twilio Altidor IVR** (welcome + press 1/2/3 menu, **not** Openbot LLM voice): Node app on **breathlessserver** at `~/twilio-voice-app/twilio-voice-app/index.js`, listens on **port 3000**; Twilio primary URL shape **`http://69.124.82.203:3000/twilio/voice`** → `/twilio/menu`. **Openbot** inbound Twilio is different: **`https://openbot.flywithpeggs.com/webhook/voice`** in `openbot/main.py`. Do not conflate the two or repoint the IVR number to Openbot without explicit intent.
- Notion runbook page for the IVR (host, paths, restart): `https://www.notion.so/32dae7c4c41181f48a39ef9946d21d9a` (child of **PROJECT CITADELLE**).
- The VPN network includes a Raspberry Pi **`altidor-pi`**. On the LAN it is **`peggs@altidor-pi.local`** (mDNS). That Pi runs **Altidor Sentinel** (Python under `/home/peggs/Altidor_Sentinel`) and is **not** the host for the Node Twilio IVR on port 3000—that IVR runs on **breathlessserver** as above.
- Local AI orchestration uses `.zshrc` helpers including `bugscan`, `find-code`, `mem-index`, and `zreload`, plus Ollama with `qwen3:8b` for audits and `nomic-embed-text` for embeddings.
- Continual-learning transcript index state for this workspace is stored at `.cursor/hooks/state/continual-learning-index.json`.
- `openbot` includes separate Trade Show Intel and UGC workflows, aligning each to distinct Notion databases; it is the single preferred runtime for multi-capability behavior, with Telegram and Twilio as interfaces into the same core bot rather than parallel duplicate bots per feature.
- Call feedback is expected both in Telegram and via call-history or status retrieval endpoints.
- Telephony work is Twilio-first for now; deeper 3CX extension integration is deferred until it is worth revisiting.
- The Telegram myOshee runtime codebase lives under `/Users/peggs/Projects/openbot`, including ongoing finance-oriented myOshee work (budget, debt, savings, stocks, crypto, credit).
