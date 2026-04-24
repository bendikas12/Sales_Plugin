## 0.15.3 - 2026-04-24
- Changed: sales-dashboard's spend-gap n8n call now sends an empty `chatInput` (`{ "type": "chat", "chatInput": "", "email": "<REP.email>" }`). The workflow is dedicated to spend-gap rows, so any prompt string is noise — only the rep email actually matters.

## 0.15.2 - 2026-04-24
- Fixed: sales-dashboard's spend-gap n8n input payload now includes the invoker's email directly in the input object (`{ "type": "chat", "chatInput": "biggest spend gap", "email": "<REP.email>" }`) so the workflow knows which rep to filter the Google Sheet for. Previously the email was passed only as a separate tool argument, which the workflow didn't receive.

## 0.15.1 - 2026-04-24
- Fixed: sales-dashboard's spend-gap n8n call was passing `chatInput: "Give me my biggest spend gap companies"` — the workflow's chat-trigger node routes on the literal phrase `"biggest spend gap"` and returned empty for the long form. SKILL.md now specifies the exact trigger string and explicitly warns not to paraphrase it.

## 0.15.0 - 2026-04-24
- Added: sales-dashboard renders a "Biggest Spend Gap — Companies" table at the bottom of the page (below the Pipeline-by-stage chart), fed by n8n workflow `WpHzZ6nsAERzp2H5` (production mode) scoped to the invoker's email (`REP.email`, never hardcoded). Polls `get_execution` with `includeData: false` until `status != "running"`, then fetches `includeData: true, nodeNames: ["Get row(s) in sheet"]` and renders five columns: Name, Spending Gap, Hubspot Exp Monthly Trx Vol, Org Activation Date, Max Utilization. Rows transformed programmatically into `{{SPEND_GAP_ROWS_HTML}}` (never hand-typed) with case-insensitive header matching so minor sheet renames don't break the table. Chat summary gains a matching top-10 block. Renders `N/A` if the n8n MCP is unavailable or the workflow doesn't finish with status `success`.

## 0.14.0 - 2026-04-23
- Changed: sales-dashboard pipeline card and by-stage chart now sum `expected_monthly_transaction_volume` (rep-forecasted) instead of `total_addressable_monthly_transaction_volume` (ceiling). UI labels switched from "Total addressable volume" to "Expected volume". Token renamed `{{TAM_VOLUME}}` → `{{EXPECTED_VOLUME}}`; the by-stage chart JSON key renamed `tam` → `expected` and the Chart.js dataset label renamed accordingly. Chat summary now prints `Expected volume` instead of `TAM volume`. Removed the "Note on field choice" paragraph from the skill since all three volume metrics (pipeline card + submitted-to-credit + activated) now use the same underlying field.

## 0.13.1 - 2026-04-23
- Updated: Switched in dashboard skill from it to look for "Object: Object" to "Object: Deal" which is now correct

## 0.13.0 - 2026-04-23
- Added: sales-dashboard now shows a **"Last 30 days — funnel throughput"** section with three new cards placed between the existing Sales pipeline grid and Pipeline by stage chart: **Demos scheduled** (count), **Submitted to credit** (sum of `expected_monthly_transaction_volume`), and **Account activated** (sum of `expected_monthly_transaction_volume`). All three filter on the deal's stage-entered timestamp — a deal that entered the stage in the window counts even if it has since moved on (throughput, not snapshot). Sales Pipeline only; Pliant-custom `deal_stage_timestamp_*` properties resolved at runtime via `search_properties` (internal-name prefix + label match). New template tokens `{{DEMO_SCHEDULED_30D}}`, `{{SUBMITTED_CREDIT_30D_VOL}}`, `{{ACCOUNT_ACTIVATED_30D_VOL}}`. Chat summary gained a matching `Last 30d throughput` block.
- Added: `references/hubspot-glossary.md` now lists every Sales Pipeline stage (rows marked `TODO_FILL_IN` for stages whose `dealstage` IDs haven't been captured yet), plus a new "Stage-entered timestamp properties" table for the three `deal_stage_timestamp_*` internal names used by the dashboard (rows marked `TODO_DISCOVER_AT_RUNTIME` until a skill run resolves and caches them back).
- Note: the two new volume metrics sum `expected_monthly_transaction_volume` (rep-forecasted), deliberately different from the existing pipeline TAM card which stays on `total_addressable_monthly_transaction_volume` (ceiling). Both are surfaced — do not swap.

## 0.12.0 - 2026-04-23
- Added: sales-dashboard Calls card now shows a rolling **last 30 days vs prior 30 days (days 31–60 ago)** comparison alongside the existing week / month counts, with a signed percentage delta coloured green (up) / red (down) so reps can see call-volume trend at a glance. Two additional `search_crm_objects` fetches are added for the rolling windows — the existing `CALLS_WEEK` / `CALLS_MONTH` buckets are calendar-anchored (ISO Monday / 1st of month) and cannot be reused to derive a rolling 30-day count. No extra requests beyond the two new buckets; all other metrics unchanged. Plain-text chat summary gained a matching `Calls trend` line. Template adds tokens `{{CALLS_LAST_30}}`, `{{CALLS_PRIOR_30}}`, `{{CALLS_DELTA_PCT}}`, `{{CALLS_DELTA_CLASS}}` inside the existing Calls card — card count, position, and section layout unchanged.

## 0.11.3 - 2026-04-22
- Fixed: sales-dashboard was still not landing on the rep's local Desktop when run under Claude Code on the web — `$HOME` resolved inside the cloud sandbox, not on the user's Mac. Output-path resolution now (1) honours an explicit `$ARGUMENTS` path if supplied, (2) otherwise calls `request_cowork_directory` to mount `~/Desktop` on the user's real filesystem and writes to `<mounted>/Claude/Dashboard/sales-dashboard.html`, (3) resolves the final string via the same `P=...; mkdir -p; printf` Bash block before passing to Write. Filename stays stable so the bookmark keeps working.

## 0.11.0 - 2026-04-21
- Added: new `SessionStart` hook `load-guru-guidance.sh` that injects a system message telling Claude to use the Guru connector (MCP) whenever the user asks about internal company knowledge — policies, processes, playbooks, product details, sales enablement, onboarding / compliance procedures, internal FAQs, or anything that would live in an internal wiki. Explicitly scoped to exclude HubSpot CRM data, which stays on the HubSpot connector. If no Guru tool is available in the session, Claude is instructed to tell the user rather than guess.
- Changed: `hooks/hooks.json` now registers both `load-hubspot-glossary.sh` and `load-guru-guidance.sh` on `SessionStart` (matcher `startup|resume`).

## 0.10.1 - 2026-04-21
- Changed: `pliant-design` now forbids dark backgrounds entirely. Pliant Black, Dark Charcoal, Pliant Gray (`#404c52`), and the Dark tint column are reclassified as element colors (text, icons, borders, small shapes, chips) — never backgrounds for pages, sections, slides, cards, or modals. Backgrounds are restricted to White or light neutrals (Pliant Gray 1 / Gray 2).
- Changed: removed the CaaS "Dark Charcoal as main background" guidance. Tech feel is now achieved via dark elements on light surfaces, not an inverted canvas.
- Changed: Text Color Rules table dropped the Black / Dark-background rows and now documents text-on-dark only for dark *elements* (chips/icons/shapes) sitting on a light page. Per-artifact HTML/PPTX sections explicitly prohibit setting dark `background-color` / slide fills.
- Changed: Pliant Black usage in the Primary Colors table is now "text, logos, small element fills — never a background" (the swag-background exception is removed).

## 0.10.0 - 2026-04-21
- Changed: renamed `pliant-brand-guidelines` skill to `pliant-design` (directory + SKILL.md `name` frontmatter). Auto-invocation description updated to match.
- Added: shape & corners section to `pliant-design` — Pliant visuals use rounded corners, never sharp. Documents a radius scale (chips 6px, buttons/inputs 10px, cards/tables 16px, hero/modals 24px, pills 9999px, images 12–16px), nesting rules (children ≤ parent), and a hard "no 0px corners on branded surfaces" rule. Per-artifact guidance now specifies radii for HTML, `MSO_SHAPE.ROUNDED_RECTANGLE` with adjustments ~0.1/~0.15 for PPTX, and `roundRect` preset geometry for DOCX shapes.

## 0.9.0 - 2026-04-21
- Added: `pliant-brand-guidelines` skill with Pliant's official color palette (primaries, secondaries, tints, neutrals), typography rules (Pangea headlines, Maison Neue body), text-color contrast rules, and application guidance for HTML / PPTX / DOCX outputs. Auto-invoked whenever the user asks for Pliant branding, corporate identity, brand colors, or visual identity on any artifact.

## 0.8.2 - 2026-04-21
- Fixed: pipeline-by-stage chart now always shows every canonical stage label on the X axis, with height 0 if no deals are in that stage. Previously the Python grouping filtered empty stages out, so the chart hid parts of the funnel — the rep couldn't see where the gaps were.
- Fixed: dashboard still wasn't landing on the Desktop. Root cause: the previous bash block used `${ARGUMENTS:-...}` and `eval echo`, which fought with Claude Code's pre-substitution of `$ARGUMENTS` and was ambiguous enough that the model sometimes passed an unresolved `${HOME}/...` string to Write. Rewrote as a single deterministic bash call (`P="$HOME/..."; mkdir -p "$(dirname "$P")"; printf '%s' "$P"`) whose stdout is the absolute path. Skill now captures that stdout and passes it verbatim to Write. No more `eval`, no more parameter expansion guesswork.

## 0.8.1 - 2026-04-21
- Fixed: pipeline-by-stage chart was dropping Discovery / Demo Scheduled, Business Case Validation, and Commercial Alignment into the unknown-stages bucket at the far right. Glossary and skill `STAGE_ORDER` now match HubSpot funnel order: Discovery / Demo Scheduled → Solution Qualification / Demo conducted → Business Case Validation → Commercial Alignment → Pre-Onboarding → Submitted to credit → Info requested → Info partially obtained → Info fully obtained → Submitted to partner bank.
- Fixed: dashboard was not landing at `~/Desktop/Claude/Dashboard/`. The Write tool does not expand shell variables, so the literal `${HOME}/...` string was being passed through. Skill now resolves `$HOME` / `~` / `$ARGUMENTS` via bash (`eval echo`) once and passes the concrete absolute path to Write. `mkdir -p` is unified into the same bash block.

## 0.8.0 - 2026-04-21
- Added: sales-dashboard now renders a bar chart of total addressable volume by deal stage, below the existing pipeline cards. Y axis is summed `total_addressable_monthly_transaction_volume`, X axis is deal stages in canonical funnel order (Solution Qualification → Pre-Onboarding → Submitted to credit → Info requested → Info partially obtained → Info fully obtained → Submitted to partner bank). Unknown / newly-added stages are appended sorted so nothing is silently dropped. Chart is Chart.js 4.4.1 via CDN, matches the dashboard's dark theme. Data is computed programmatically from the same paginated deal set used for TAM — no manual transcription.
- Added: new `{{PIPELINE_STAGE_DATA_JSON}}` template token, inlined verbatim as a JS literal in the template's `<script>` block.
- Changed: sales-pipeline deal fetch now also requests `name_of_deal_stage` (needed for chart labels — `dealstage` IDs are for filtering, labels are for display).

## 0.7.3 - 2026-04-21
- Changed: sales-dashboard default output path is now `${HOME}/Desktop/Claude/Dashboard/sales-dashboard.html` so reps can bookmark the file once and reopen it every morning for fresh numbers. Skill runs `mkdir -p` on the parent directory before writing so the `Claude/Dashboard/` folders are created automatically on first run. `$ARGUMENTS` path override still works.

## 0.7.2 - 2026-04-21
- Fixed: sales-dashboard pipeline filter was excluding the wrong deals. The skill now filters on `dealstage` NOT IN (`16177379`, `16258181`, `30637484`) — Account activated / Closed Lost / Churned — hardcoded directly in the skill so it never depends on glossary lookup. IDs are stable, text labels aren't.
- Fixed: sales-dashboard TAM summation. Step 3 now paginates all deal results, concatenates them, and sums `total_addressable_monthly_transaction_volume` with a `python3` one-liner (jq equivalent documented). Explicitly forbids the previous failure mode of reading values out of the JSON by eye and retyping them. Asserts `len(deals) == total` before summing.
- Fixed: glossary and template paths. Replaced bare `references/...` paths with absolute `${CLAUDE_PLUGIN_ROOT}/...` ones (matching the hooks convention), and added a Step 0 that re-reads the glossary so the skill works even when the SessionStart hook hasn't fired (scheduled jobs, resumed contexts).
- Added: `Deal stage ID lookup` table in `references/hubspot-glossary.md` covering the three excluded stages. Other stages can be filled in as future skills need them.

## 0.7.1 - 2026-04-21
- Fixed: sales-dashboard emails-sent count. The `hs_email_direction EQ "EMAIL"` filter is now a hard requirement (no fallback), and the search is specified as a single ANDed filter group against `objectType: "Emails"`. Reads `total` with `limit: 1` instead of paginating. Documents the other direction enum values (`INCOMING_EMAIL`, `FORWARDED_EMAIL`, `DRAFT_EMAIL`) as explicitly-not-counted, and requires `hs_timestamp` to be passed as epoch milliseconds. Without this, the previous fallback path let Claude drop the direction filter and over-count.

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
