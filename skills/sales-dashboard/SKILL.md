---
description: Render the rep's daily sales dashboard — HubSpot calls/emails this week & month, overdue HubSpot tasks, Gmail unread count, today's meetings (with customer-facing count), and open pipeline deals with total addressable volume. Uses a fixed HTML template overwritten each run so a scheduled job always produces the same file.
argument-hint: "[optional output path]"
---

The user has invoked the sales dashboard skill. The argument (if provided) is: $ARGUMENTS

## Output rules — READ THIS FIRST

- The dashboard HTML structure is **fixed**. Use `${CLAUDE_PLUGIN_ROOT}/skills/sales-dashboard/references/dashboard-template.html` verbatim and only substitute the `{{TOKEN}}` placeholders. Do not add, remove, or reorder tiles. If a metric can't be fetched, render `N/A` for that token — never invent a number and never restructure the template.
- Each run **overwrites** the same output file so the rep can bookmark it once and reopen it every morning to see fresh numbers. **Resolve the output path via a single Bash call, then pass the printed absolute path to the Write tool.** The Write tool does not expand `$HOME`, `${HOME}`, or `~` — it takes a literal path string, so you must resolve it first:
  ```bash
  P="$HOME/Desktop/Claude/Dashboard/sales-dashboard.html"
  mkdir -p "$(dirname "$P")"
  printf '%s' "$P"
  ```
  Run this one Bash call, capture stdout (something like `/Users/jane/Desktop/Claude/Dashboard/sales-dashboard.html`), and use that literal string as the `file_path` argument to Write. If the user passed a path in `$ARGUMENTS` (starts with `/`, `~`, or `./`), replace the first line with `P="<that argument>"` and run the same three lines. Never change the filename between runs; the stable bookmark depends on it.
- After writing the file, also print a plain-text summary of the same numbers to chat so the rep sees results without opening the file.
- This skill is personalised to the invoker. All metrics are scoped to **the person running the skill** — never aggregate across the team.

---

## Step 0 — Load the HubSpot glossary

Read `${CLAUDE_PLUGIN_ROOT}/references/hubspot-glossary.md` into working memory before doing anything else. The SessionStart hook normally injects this automatically, but when this skill is invoked outside a fresh session (scheduled job, resumed context after compaction, another agent environment) the hook may not have fired. Re-reading is cheap and guarantees every downstream step has the property glossary and pipeline / stage ID tables available. **Use the absolute `${CLAUDE_PLUGIN_ROOT}/...` path — never a bare `references/...` relative path, which resolves ambiguously depending on the caller's cwd.**

---

## Step 1 — Identify the rep (who is running this skill)

Resolve the invoker's Gmail identity before anything else. Store as `REP`:

Priority (stop at first that succeeds):
1. Gmail MCP profile / `get_me` → take `name` + `emailAddress`
2. `From` header display name on the 3 most recent sent messages + authenticated address
3. Title-case the local-part of the authenticated Gmail address (e.g. `jane.doe@getpliant.com` → "Jane Doe")
4. If none work, stop and ask: *"I couldn't identify your Gmail account. What name and email should I build the dashboard for?"*

**Hard rules:**
- `REP` is **never** a HubSpot deal owner name, a Fireflies host, or a contact in the CRM. It only comes from the Gmail identity sources above.
- Once resolved, resolve `REP.hubspot_owner_id` via `search_owners` keyed on `REP.email`. To load the owners tool schema, use `ToolSearch` with the keyword query `owners` (the MCP server prefix varies across environments). If no HubSpot owner matches the email, render HubSpot metrics as `N/A` and note it in the chat summary — do not guess a different owner.

---

## Step 2 — Compute the time windows

Use the rep's local timezone (infer from Gmail profile or Calendar; fall back to UTC if unavailable).

- `TODAY_START` = 00:00 local, today
- `TODAY_END` = 23:59:59 local, today
- `WEEK_START` = Monday 00:00 of the current ISO week
- `MONTH_START` = 1st of the current calendar month, 00:00
- `NOW` = current timestamp

Record these as timestamps for filter use. Also compute `GENERATED_AT` (ISO 8601, local tz) for the footer.

---

## Step 3 — Fetch metrics (run in parallel where possible)

### HubSpot calls
Use `search_crm_objects` with `objectType: "Call"` and filters:
- `hubspot_owner_id` = `REP.hubspot_owner_id`
- `hs_timestamp` ≥ `WEEK_START` → count → `CALLS_WEEK`
- Repeat with `hs_timestamp` ≥ `MONTH_START` → count → `CALLS_MONTH`

### HubSpot emails sent
Use `search_crm_objects` with `objectType: "Emails"` (HubSpot engagement type). **All filters below must be ANDed inside a single filter group**:
- `hubspot_owner_id` EQ `REP.hubspot_owner_id`
- `hs_email_direction` EQ `"EMAIL"` — this is the enum value for **Outgoing**. Do not omit or substitute. Other values (`INCOMING_EMAIL`, `FORWARDED_EMAIL`, `DRAFT_EMAIL`) must not be counted.
- `hs_timestamp` GTE `WEEK_START` (epoch milliseconds) → set `limit: 1` and read `total` from the response → `EMAILS_WEEK`
- Repeat the request with `hs_timestamp` GTE `MONTH_START` (epoch milliseconds) → read `total` → `EMAILS_MONTH`

All timestamps must be passed as **epoch milliseconds** computed in the rep's local timezone.

### HubSpot overdue tasks
Use `search_crm_objects` with `objectType: "Task"` and filters:
- `hubspot_owner_id` = `REP.hubspot_owner_id`
- `hs_task_status` ≠ `COMPLETED`
- `hs_timestamp` < `NOW` (task due date in the past)
- Count → `OVERDUE_TASKS`

### Gmail unread
Use the Gmail MCP `list_messages` / equivalent with query `is:unread in:inbox category:primary` (fall back to `is:unread in:inbox` if category filtering isn't supported). Use `resultSizeEstimate` or the unread count from the INBOX label if the MCP exposes it directly (cheaper than listing messages). → `UNREAD_EMAILS`

### Calendar meetings today
Use the Google Calendar MCP to list events on the rep's primary calendar between `TODAY_START` and `TODAY_END`.
- Exclude cancelled events and all-day OOO blocks.
- `MEETINGS_TODAY` = total count.
- A meeting is **customer-facing** if it has at least one attendee whose email domain is **not** `@getpliant.com` and is not `resource.calendar.google.com` (room resources). Exclude declines. Count → `CUSTOMER_FACING_MEETINGS`.

### HubSpot sales pipeline
Use `search_crm_objects` with `objectType: "Object"` (deal). **All filters ANDed in a single filter group**:
- `hubspot_owner_id` EQ `REP.hubspot_owner_id`
- `pipeline` EQ `"16177355"` (Sales Pipeline — see `${CLAUDE_PLUGIN_ROOT}/references/hubspot-glossary.md`)
- `dealstage` NOT IN (`"16177379"`, `"16258181"`, `"30637484"`) — these are **Account activated**, **Closed Lost**, **Churned** respectively. Filter on the numeric `dealstage` ID, not on the `name_of_deal_stage` text label: IDs are stable across label renames and localisations. These IDs are hardcoded here on purpose — do not attempt to look them up or guess them.
- Request properties: `dealname`, `dealstage`, `name_of_deal_stage`, `total_addressable_monthly_transaction_volume` (the label is needed to render the by-stage chart — IDs are for filtering, labels are for display)
- Set `limit: 100` and paginate using the `after` cursor until every page is fetched. After the first response, note `total`; after the loop, assert `len(all_deals) == total` before summing. If the assertion fails, re-fetch once; if it still fails, render `PIPELINE_DEALS` and `TAM_VOLUME` as `N/A` and note the reason in the chat summary.

**Sum `TAM_VOLUME` programmatically — never by hand.** After all pages are concatenated into a single JSON array of deal objects, pipe that array into a Python one-liner and use its stdout verbatim. Do **not** read individual property values into your own reasoning and add them up — that's how we got a wrong total last time.

```bash
python3 -c '
import json, sys
deals = json.load(sys.stdin)
total = sum(float(d.get("properties", {}).get("total_addressable_monthly_transaction_volume") or 0) for d in deals)
print(int(total))
' <<< "$DEALS_JSON"
```

(Equivalent jq works too: `jq '[.[] | (.properties.total_addressable_monthly_transaction_volume // 0 | tonumber)] | add'`.)

Then:
- `PIPELINE_DEALS` = length of the concatenated deals list (same as `total` from the first page).
- `TAM_VOLUME` = the integer printed by the script above, formatted with the rep's currency if known (else EUR) and thousand separators, e.g. `€1,245,000`. Null / missing values are treated as 0 by the script — don't warn, some deals legitimately have no TAM yet.

**Also compute `PIPELINE_STAGE_DATA_JSON` — the data for the by-stage chart.** Same rule: do it programmatically, don't hand-pick. Pipe the same concatenated deals JSON through this script and use its stdout verbatim:

```bash
python3 -c '
import json, sys
from collections import defaultdict

# Canonical funnel order for the Sales Pipeline. Stages not in this list
# (newly-added HubSpot stages, renames) are appended after these, sorted
# alphabetically, so nothing is silently dropped.
STAGE_ORDER = [
    "Discovery / Demo Scheduled",
    "Solution Qualification / Demo conducted",
    "Business Case Validation",
    "Commercial Alignment",
    "Pre-Onboarding",
    "Submitted to credit",
    "Info requested",
    "Info partially obtained",
    "Info fully obtained",
    "Submitted to partner bank",
]

deals = json.load(sys.stdin)
by_stage = defaultdict(float)
for d in deals:
    props = d.get("properties", {}) or {}
    stage = props.get("name_of_deal_stage") or "Unknown"
    tam = float(props.get("total_addressable_monthly_transaction_volume") or 0)
    by_stage[stage] += tam

# Emit EVERY canonical stage, with 0 if no deals land there — the rep
# needs to see the empty stages in the chart so the funnel shape is
# obvious. Unknown stages (renames / newly-added) are appended sorted.
known = [(s, by_stage.get(s, 0.0)) for s in STAGE_ORDER]
unknown = sorted((s, v) for s, v in by_stage.items() if s not in STAGE_ORDER)
ordered = known + unknown

print(json.dumps([{"stage": s, "tam": int(v)} for s, v in ordered]))
' <<< "$DEALS_JSON"
```

`PIPELINE_STAGE_DATA_JSON` is the raw JSON array printed by the script (e.g. `[{"stage":"Discovery / Demo Scheduled","tam":0},{"stage":"Solution Qualification / Demo conducted","tam":120000}, ...]`). It's inlined **verbatim** into the template's `<script>` block as a JS literal — do not wrap it in quotes, do not pretty-print, do not hand-edit the labels. The script always emits every canonical stage, so an empty pipeline still renders all 10 stage labels on the X axis at height 0 — the rep needs to see the full funnel shape even when stages are empty.

---

## Step 4 — Render the dashboard

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/sales-dashboard/references/dashboard-template.html`.
2. Substitute every `{{TOKEN}}`. Full list:
   - `{{REP_NAME}}`, `{{REP_EMAIL}}`
   - `{{DATE}}` — `YYYY-MM-DD`
   - `{{GENERATED_AT}}` — ISO 8601 with timezone
   - `{{CALLS_WEEK}}`, `{{CALLS_MONTH}}`
   - `{{EMAILS_WEEK}}`, `{{EMAILS_MONTH}}`
   - `{{OVERDUE_TASKS}}`
   - `{{UNREAD_EMAILS}}`
   - `{{MEETINGS_TODAY}}`, `{{CUSTOMER_FACING_MEETINGS}}`
   - `{{PIPELINE_DEALS}}`, `{{TAM_VOLUME}}`
   - `{{PIPELINE_STAGE_DATA_JSON}}` — raw JSON array, inlined as a JS literal (no surrounding quotes)
3. Write the result to the **absolute path resolved in the Output rules** (the `echo`ed value from the bash block). Use the Write tool — it overwrites existing files by design, which is what the rep's bookmark relies on. Do not re-derive the path here; reuse the one already computed.

---

## Step 5 — Print a chat summary

After writing, print exactly this block so the rep sees the numbers inline:

```
Sales Dashboard — <REP_NAME> — <DATE>

HubSpot activity
  Calls logged     week <CALLS_WEEK>   month <CALLS_MONTH>
  Emails sent      week <EMAILS_WEEK>  month <EMAILS_MONTH>
  Overdue tasks    <OVERDUE_TASKS>

Inbox & calendar
  Unread emails    <UNREAD_EMAILS>
  Meetings today   <MEETINGS_TODAY>  (customer-facing: <CUSTOMER_FACING_MEETINGS>)

Sales pipeline
  Active deals     <PIPELINE_DEALS>
  TAM volume       <TAM_VOLUME>

Written to: <output path>
```

If any metric failed to fetch, replace its value with `N/A` and add a final line `Note: <reason>` (one line per failed metric). Do not retry failed fetches more than once.
