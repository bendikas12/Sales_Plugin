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
