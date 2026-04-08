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
- Update `CHANGELOG.md` at the same time, using the format:
  ```
  ## x.x.x - YYYY-MM-DD
  - Added / Fixed / Changed: description
  ```
- Use semantic versioning: MAJOR.MINOR.PATCH
  - PATCH (0.1.1): bug fixes, wording tweaks
  - MINOR (0.2.0): new skills, hooks, commands
  - MAJOR (1.0.0): breaking changes or major restructure

## Plugin structure
- Skills go in `skills/<skill-name>/SKILL.md`
- Hooks go in `hooks/hooks.json`
- Commands go in `commands/`
- Never put skills/hooks/commands inside `.claude-plugin/` — only `plugin.json` and `marketplace.json` go there
