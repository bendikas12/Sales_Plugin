# Pliant Sales Plugin

A Claude Code plugin for the Pliant sales team. Adds AI-powered skills and commands for prospecting, deal prep, meeting research, and daily pipeline visibility — all wired into HubSpot, Gmail, and internal tools.

**Current version:** 0.3.1

---

## Skills

Skills are invoked automatically when Claude detects a relevant task, or explicitly via the `/skill` command.

| Skill | What it does |
|-------|-------------|
| **contact-company-enrichment** | Enrich a prospect's company (domain, HQ phone) and contact (email, direct dial, LinkedIn, job title). Company enrichment runs first to scope the person lookup. Routes through Amplemarket → Clay/n8n → web search. Outputs a clean copy-paste block for manual entry in HubSpot — never updates CRM automatically. |
| **meeting-prep** | Generate a pre-meeting brief in minutes: company snapshot, contact intel, tailored discovery questions, pain points, and an opening insight. Uses web research + HubSpot context. |
| **hubspot-record-analysis** | Work with any HubSpot record (deal, contact, or company). Accepts a name, ID, or HubSpot URL. Runs a full analysis or answers a specific question about the record. |
| **email-followup-v2** | Draft a post-meeting follow-up email. Multi-meeting synthesis, prior email thread awareness, engagement history, and the rep's own writing voice. Output renders in Claude for copy into Gmail. |
| **sales-dashboard** | Render the rep's daily sales dashboard: HubSpot calls/emails this week & month, overdue tasks, Gmail unread count, today's meetings, and open pipeline deals with expected volume. |
| **pliant-design** | Apply Pliant's official brand colors, typography, and shape language to any artifact. Use when producing branded outputs or slides. |

---

## Commands

| Command | What it does |
|---------|-------------|
| `/dashboard` | Open the daily sales dashboard (same as the sales-dashboard skill). |
| `/deal-summary` | Summarise a deal from HubSpot — timeline, contacts, next steps. |

---

## Hooks

| Hook | Trigger |
|------|---------|
| **load-hubspot-glossary** | Loads the HubSpot property glossary at session start so Claude knows deal/contact field names without being asked. |
| **load-guru-guidance** | Routes internal company knowledge questions (policies, processes, playbooks) to the Guru connector automatically. |

---

## Installation

This plugin is distributed via the Pliant internal marketplace. In Claude Cowork:

1. Go to **Settings → Plugins**
2. Find **Pliant Sales Plugin**
3. Click **Install** (or **Update** if already installed)

To update to the latest version, click **Update** in the plugin panel — Claude Code checks the `marketplace.json` version to detect new releases.

---

## Contributing

- **Branch policy:** never push directly to `main` — always open a PR from a feature branch
- **Versioning:** bump `version` in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` with every change; update `CHANGELOG.md` at the same time
- **Semantic versioning:** PATCH for bug fixes/tweaks, MINOR for new skills or commands, MAJOR for breaking changes

See [CHANGELOG.md](CHANGELOG.md) for release history.
