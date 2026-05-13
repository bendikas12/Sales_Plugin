---
name: sales-dashboard-artifact
description: Install or refresh the rep's "Sales Dashboard" live artifact — a persistent Cowork view that self-refreshes HubSpot calls/emails/tasks/pipeline, Gmail unread, today's meetings, and the n8n-fed Overdue Deals & Spend Gap tables on demand. Use when the user asks for a live dashboard, an always-on dashboard, a self-refreshing dashboard, a dashboard artifact, or wants to install the sales dashboard tool. Once installed, the rep clicks Reload inside the artifact to pull fresh numbers — this skill only builds or updates the template.
---

The user wants the **Sales Dashboard** live artifact installed (or refreshed) in their Cowork. The argument (if provided) is: $ARGUMENTS

## What this skill does

It creates a single persisted artifact (id: `sales-dashboard`) that:
- On open, queries HubSpot, Gmail, Calendar, and n8n via `window.cowork.callMcpTool` and renders every metric the static `sales-dashboard` skill produces.
- Re-runs every fetch when the rep clicks **Reload** in the artifact header.
- Is fully transferable — the template carries no rep-specific data; the MCP tool names and the rep's identity are substituted into the template at install time, so every user installs it for themselves.

This skill is the live-artifact counterpart of the existing `sales-dashboard` skill (which writes a static HTML file on each run). Prefer this one when the rep wants a single bookmarkable tab inside Cowork rather than a file on disk.

## Output rules — READ THIS FIRST

- The HTML structure is **fixed**. Use `${CLAUDE_PLUGIN_ROOT}/skills/sales-dashboard-artifact/references/artifact-template.html` verbatim and only substitute the `{{TOKEN}}` placeholders defined below. Do not edit the styles, card layout, button labels, fetch logic, or hardcoded HubSpot constants (pipeline ID, excluded stage IDs, stage-entered timestamp property names) inside the template — those are the same for every Pliant rep and are version-controlled centrally.
- The artifact ID is **always** `sales-dashboard`. Never invent a different ID — the same ID across reps means each rep has exactly one dashboard artifact and re-running this skill updates it in place instead of creating duplicates.
- All MCP tool names and the rep's identity must be resolved at runtime per-install. Do not hardcode any tool ID or email you happen to see in this prompt or in another rep's installed artifact.

---

## Step 0 — Load the HubSpot glossary

Read `${CLAUDE_PLUGIN_ROOT}/references/hubspot-glossary.md` once before resolving anything. The template hardcodes the Sales pipeline ID, excluded stage IDs, and the three stage-entered timestamp property internal names — verify they still match the glossary. If the glossary has changed any of these IDs, update the constants in `references/artifact-template.html` and bump the plugin version. **Use the absolute `${CLAUDE_PLUGIN_ROOT}/...` path — never a bare `references/...` relative path.**

---

## Step 1 — Resolve the rep's identity

Resolve the invoker's Gmail identity. Store as `REP`:

Priority (stop at first that succeeds):
1. The Cowork `userEmail` context injected at the top of the conversation (look for a `# userEmail` block).
2. Gmail MCP `get_me` / profile call → take `name` + `emailAddress`.
3. `From` header on the 3 most recent sent messages + authenticated address.
4. Title-case the local-part of the authenticated Gmail address as a name fallback (e.g. `jane.doe@getpliant.com` → "Jane Doe").
5. If none work, stop and ask: *"I couldn't identify your Gmail account. What name and email should I wire the dashboard artifact to?"*

Do **not** fall back to any email or name you've seen in another session or in this prompt. Every HubSpot filter inside the artifact is keyed on the resolved owner ID — wrong rep = wrong numbers, silently.

Then resolve `REP.hubspot_owner_id` via the HubSpot `search_owners` tool keyed on `REP.email`. Load its schema with `ToolSearch` keyword `owners` (the MCP server prefix varies). If no HubSpot owner matches the email, stop and tell the rep: *"You don't have a HubSpot owner record — the dashboard can't filter activity to you. Ask RevOps to add you as an owner, then re-run."* Do not guess a different owner.

---

## Step 2 — Resolve the MCP tool names

The artifact needs six tools at runtime. Each MCP server prefix is a per-installation UUID and differs across reps. Use `ToolSearch` to resolve the current fully-qualified names — keyword queries shown in the table.

| Purpose | Suffix | ToolSearch query | Token |
| --- | --- | --- | --- |
| HubSpot — search any CRM object (Call/Emails/Task/Deal) | `search_crm_objects` | `hubspot search_crm_objects` | `HS_SEARCH_CRM_TOOL` |
| HubSpot — search owners by email | `search_owners` | `hubspot search_owners` | `HS_SEARCH_OWNERS_TOOL` |
| Gmail — search threads | `search_threads` | `gmail search_threads` | `GMAIL_SEARCH_TOOL` |
| Google Calendar — list events | `list_events` | `calendar list_events` | `CAL_LIST_EVENTS_TOOL` |
| n8n — execute a workflow | `execute_workflow` | `n8n execute_workflow` | `N8N_EXECUTE_TOOL` |
| n8n — get execution status / data | `get_execution` | `n8n get_execution` | `N8N_GET_EXECUTION_TOOL` |

Verify each resolved tool starts with `mcp__` and ends with the expected suffix. If any of HubSpot's two tools, Gmail, or Calendar can't be found, stop and tell the rep which connector is missing — they need to install it in Cowork settings before the artifact can work. The two n8n tools are optional: if n8n isn't installed, still install the artifact but pass empty strings for those two tokens — the Overdue Deals and Spend Gap tables will render `N/A` and the rest of the dashboard works fine.

`HS_SEARCH_OWNERS_TOOL` is listed in the `mcpTools` array so Cowork allows owner lookups if a future template version moves owner resolution into the artifact itself. Today's template resolves the owner once at install (Step 1) and inlines `HUBSPOT_OWNER_ID` — but keeping `search_owners` in the artifact's permission list lets us iterate without re-installing for every rep.

---

## Step 3 — Render the template

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/sales-dashboard-artifact/references/artifact-template.html`.
2. Substitute every `{{TOKEN}}` exactly once:
   - `{{REP_NAME}}` — the rep's display name from Step 1.
   - `{{REP_EMAIL}}` — lowercased.
   - `{{HUBSPOT_OWNER_ID}}` — numeric owner ID from Step 1.
   - `{{HS_SEARCH_CRM_TOOL}}`, `{{HS_SEARCH_OWNERS_TOOL}}` — from Step 2.
   - `{{GMAIL_SEARCH_TOOL}}` — from Step 2.
   - `{{CAL_LIST_EVENTS_TOOL}}` — from Step 2.
   - `{{N8N_EXECUTE_TOOL}}`, `{{N8N_GET_EXECUTION_TOOL}}` — from Step 2 (empty strings allowed if n8n isn't installed).
3. Write the rendered HTML to a workspace file (e.g. `/sessions/<session>/sales-dashboard.html`). Do **not** write directly into the artifacts directory — `create_artifact` / `update_artifact` reads from the path you pass and persists it itself.

Do **not** modify the hardcoded JS constants inside the template (`SALES_PIPELINE_ID`, `EXCLUDED_STAGE_IDS`, `DEMO_TS_PROP`, `SUBMITTED_TS_PROP`, `ACTIVATED_TS_PROP`, `STAGE_ORDER`). If any of those need to change, update the file in this repo and bump the plugin version — don't patch them per-install.

---

## Step 4 — Install (or update) the artifact

Check whether the artifact already exists:

1. Call `list_artifacts`.
2. If an entry with `id: "sales-dashboard"` exists → call `update_artifact` with that id, the rendered file path, and `update_summary: "Refresh sales-dashboard template"`.
3. Otherwise → call `create_artifact` with:
   - `id: "sales-dashboard"`
   - `html_path`: the rendered file path
   - `description: "Live sales dashboard — HubSpot calls/emails/tasks, pipeline by stage, Gmail unread, today's meetings, n8n overdue-deals and spend-gap tables. Self-refreshing via Reload button."`
   - `mcp_tools`: the six fully-qualified names from Step 2 in this exact order: `[HS_SEARCH_CRM_TOOL, HS_SEARCH_OWNERS_TOOL, GMAIL_SEARCH_TOOL, CAL_LIST_EVENTS_TOOL, N8N_EXECUTE_TOOL, N8N_GET_EXECUTION_TOOL]`. Skip any that resolved to empty strings.

Pass the tool list to `mcp_tools` even on update — Cowork uses this list to gate `window.cowork.callMcpTool` from inside the artifact. Omitting one will make the corresponding card fail at runtime with a permissions error.

---

## Step 5 — Confirm in chat

Print exactly this block (substituting values):

```
Sales Dashboard artifact installed.
  Wired to: <REP_EMAIL>  (HubSpot owner <HUBSPOT_OWNER_ID>)
  Connectors: HubSpot, Gmail, Google Calendar, n8n
  Open it from the Cowork sidebar — click Reload to refresh every card.
```

If you updated rather than created, replace the first line with `Sales Dashboard artifact refreshed.` If n8n wasn't installed and you passed empty strings, add a line `Note: n8n connector missing — Overdue Deals and Spend Gap tables will render N/A.`

Do not paste the rendered HTML into chat. Do not pre-fetch metrics in chat — the whole point is that the artifact does its own fetching on open / Reload.
