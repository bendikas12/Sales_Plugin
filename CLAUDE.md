# Claude Code Rules for Sales Plugin

## Branch policy
- NEVER push directly to `main`
- Always create a feature branch for changes (e.g. `feat/add-email-skill`, `fix/hook-format`)
- Branch names should be descriptive and kebab-case
- Only merge to `main` when the user explicitly approves

## Before starting any work
- Always run `git pull origin main` first to sync with latest changes
- Check existing skills/hooks before adding new ones to avoid duplication

## Versioning
- Bump `version` in `.claude-plugin/plugin.json` with every change set
- **Also bump the matching `version` in `.claude-plugin/marketplace.json` (inside the `sales-plugin` entry) to the same value** — Claude Code resolves plugin updates from the marketplace entry, so if this isn't bumped, clients won't pick up the new version
- Update `CHANGELOG.md` at the same time, using the format:
  ```
  ## x.x.x - YYYY-MM-DD
  - Added / Fixed / Changed: description
  ```
- Use semantic versioning: MAJOR.MINOR.PATCH
  - PATCH (0.1.1): bug fixes, wording tweaks
  - MINOR (0.2.0): new skills, hooks, commands
  - MAJOR (1.0.0): breaking changes or major restructure

## Guru — company knowledge source

Whenever the user asks about internal company knowledge — Pliant policies, processes, playbooks, product details, sales enablement, onboarding/compliance procedures, internal FAQs, or anything that would live in an internal wiki — you MUST use the Guru connector (MCP tools prefixed with `guru`) to search Guru before answering. Do not answer from general knowledge or assumptions for these topics. Use this agent ID `da16cc80-6e0c-43cb-b933-797c652a17a1`

This does NOT apply to HubSpot CRM data (deals, contacts, companies, pipeline) — that stays on the HubSpot connector.

## Plugin structure
- Skills go in `skills/<skill-name>/SKILL.md`
- Hooks go in `hooks/hooks.json`
- Commands go in `commands/`
- Shared references go in `references/`
- Never put skills/hooks/commands inside `.claude-plugin/` — only `plugin.json` and `marketplace.json` go there
