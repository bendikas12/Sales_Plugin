## 0.7.0 - 2026-04-21
- Added: `sales-dashboard` skill and `/dashboard` command. Renders a fixed HTML dashboard (template at `skills/sales-dashboard/references/dashboard-template.html`) with the invoker's HubSpot calls & emails (this week / this month), overdue HubSpot tasks, Gmail unread count, today's meetings (total + customer-facing), open Sales Pipeline deal count, and summed total addressable monthly transaction volume (excludes Account activated / Churned / Closed lost). Rep identity is resolved from Gmail only, then mapped to a HubSpot owner — team-wide aggregation is never done. Output path is stable (`$HOME/sales-dashboard.html` by default, overridable via argument) so a daily scheduled run overwrites the same file.

## 0.6.4 - 2026-04-21
- Changed: email-followup-v2 no longer invents a CTA. Removed the "CTA" item from the email structure and the associated `[INSERT CALENDLY LINK]` token + Calendly placeholder render line. The draft ends after the Next steps bullets (from Fireflies `action_items`) and the sign-off. Removes the default "let's schedule a demo" ask that was surfacing on post-demo follow-ups.

## 0.6.3 - 2026-04-21
- Fixed: email-followup-v2 sign-off was still picking up the Fireflies meeting host instead of the actual skill invoker. Identity capture is now a PREREQUISITE step that runs before any Fireflies/HubSpot data is fetched, with an explicit anti-pattern list (not the Fireflies host / organizer / participant, not the HubSpot owner, not engagement-history names) and a hard-stop ask of the user if Gmail identity can't be resolved. Step 5 now only captures writing voice; sign-off in Step 6 references the locked `SENDER` value.

## 0.6.2 - 2026-04-21
- Fixed: synced `marketplace.json` version with `plugin.json` — both now at 0.6.2. Without this, Claude Code clients read the stale marketplace version and never pick up new plugin updates.
- Changed: CLAUDE.md Versioning section now requires bumping both `plugin.json` and `marketplace.json` in lockstep for every change set.

## 0.6.1 - 2026-04-21
- Fixed: email-followup-v2 sign-off now uses the authenticated Gmail user (the person running the skill), not the HubSpot deal/contact owner. Step 5 now also captures rep identity, with fallbacks: Gmail profile → From-header display name on sent mail → title-cased local-part → `[Your name]`. "Signing as" line added to the rendered context summary.

## 0.6.0 - 2026-04-20
- Added: email-followup-v2 skill — parallel v2 of email-followup for A/B comparison. Adds multi-meeting synthesis (up to 3 transcripts, chronological), prior Gmail thread awareness, cost-bounded HubSpot engagement memo, email-based contact lookup, multi-recipient To/CC, structured-only action items (no inference), Calendly placeholder token, rep voice sampling from last 5 sent emails, Fireflies-based language detection. Renders email in Claude instead of pushing to Gmail.

## 0.5.0 - 2026-04-15
- Added: meeting-prep skill — generates a full meeting preparation brief with company snapshot, contact intel, discovery questions, pain points, and opening insight using web research + HubSpot context

## 0.3.0 - 2026-04-10
- Added: email-followup skill — drafts post-meeting follow-up emails using Fireflies transcript + HubSpot context, with Gmail draft push
## 0.4.4 - 2026-04-09
- Added: pipeline ID lookup table to glossary — maps all 6 pipeline IDs to human-readable names (Pre-Sales Pipeline, Sales Pipeline, Referrer, Partner Team, Banking, Insurance)
- Fixed: marked `pipeline` field type as `enumeration` with note that it returns an ID

## 0.4.3 - 2026-04-09
- Fixed: replaced inline `cat` hook with dedicated `hooks/load-hubspot-glossary.sh` script
- Fixed: hook now returns structured JSON with `systemMessage` for proper context injection
- Fixed: use `$CLAUDE_PLUGIN_ROOT` (correct plugin env var), matcher `startup|resume`, error handling, and status message

## 0.4.2 - 2026-04-09
- Fixed: corrected SessionStart hook JSON structure — added required `matcher` level and `type: "command"` field
- Fixed: use `$CLAUDE_PROJECT_DIR` for glossary path so it resolves correctly regardless of working directory

## 0.4.1 - 2026-04-09
- Fixed: moved glossary loading from CLAUDE.md rule to SessionStart hook, so the property glossary is injected into every session automatically (CLAUDE.md wasn't being read at session start)
- Changed: reverted CLAUDE.md HubSpot property resolution section — no longer needed with hook approach

## 0.4.0 - 2026-04-09
- Added: `references/hubspot-glossary.md` — shared property glossary with verified field names, types, and common aliases for deals, contacts, and companies
- Added: CLAUDE.md rule to always consult the glossary before using `search_properties`, so ad-hoc HubSpot queries resolve correct field names without triggering a skill

## 0.3.0 - 2026-04-09
- Added: hubspot-record-analysis — deal analysis now includes transaction volume history properties: `trx_vol_last_0_to_30_days`, `trx_vol_last_31_to_60_days`, `trx_vol_last_61_to_90_days`, `trx_vol_last_0_to_180_days`

## 0.2.2 - 2026-04-09
- Fixed: hubspot-record-analysis — added hard output constraints so the AI follows the template exactly and does not add extra fields/tables for deals, contacts, or companies
- Fixed: hubspot-record-analysis — search_owners ToolSearch now uses portable keyword query instead of hardcoded MCP server UUID, so it works across all environments

## 0.2.1 - 2026-04-09
- Fixed: hubspot-record-analysis — corrected field names to `expected_monthly_transaction_volume` and `total_addressable_monthly_transaction_volume`
- Fixed: hubspot-record-analysis — use `name_of_deal_stage` instead of `dealstage` to get human-readable stage label
- Fixed: hubspot-record-analysis — Activity objectType unsupported; now queries Email, Note, Call separately and merges results
- Fixed: hubspot-record-analysis — skill now fetches record without properties first to discover schema before presenting results

## 0.2.0 - 2026-04-08
- Added: hubspot-record-analysis skill — analyze deals, contacts, or companies by name, ID, or HubSpot URL

## 0.1.1 - 2026-04-08
- Changed: renamed plugin from "nexus" to "sales-plugin"

## 0.1.0 - 2026-04-08
- Initial release: sales-dashboard, deal-prep, email-followup skills
