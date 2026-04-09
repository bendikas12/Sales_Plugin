---
description: "Work with any HubSpot record — deal, contact, or company. Executes based on what you ask: full analysis, a specific question, or recent communications. Accepts a name, ID, or HubSpot URL."
argument-hint: "[deal/contact/company name, ID, or HubSpot URL]"
---

The user has invoked the HubSpot record skill. The argument (if provided) is: $ARGUMENTS

## Output rules — READ THIS FIRST

You **MUST** follow the output structure defined in Step 5 **exactly**. Do not add extra fields, tables, columns, or sections beyond what is specified there. If the user wants additional detail, they will ask for it explicitly. This is a hard constraint, not a suggestion.

## Step 1 — Resolve the record

**If `$ARGUMENTS` contains a HubSpot URL** (e.g. `https://app.hubspot.com/contacts/12345/record/0-3/67890`):
- Extract the object type from the URL path: `contacts` → Contact, `companies` → Company, `deals` → Deal
- Extract the record ID from the last numeric path segment
- Use `get_crm_objects` with the extracted ID

**If `$ARGUMENTS` is a name or search term:**
- If it looks like a person name or email → search objectType `Contact`
- If it looks like a company name → search objectType `Organization`
- Otherwise → search objectType `Object` (deal)
- Use `search_crm_objects` with a query filter

**If no argument is provided:**
- Check if there is a clear record being discussed in the current conversation (e.g. a deal name mentioned earlier)
- If yes, use that record
- If unclear, ask the user: "Which record would you like me to look up? Please share the name, ID, or HubSpot URL."

---

## Step 2 — Understand what the user wants

**Determine the intent from the request:**

- **"Analyze", "overview", "tell me about", "review"** → run the full structured report (Step 4)
- **Specific question** (e.g. "what's the expected transaction volume?", "who owns this?", "what stage is it in?", "what vertical is this?") → fetch only the relevant properties and answer directly, no full report needed
- **"Recent communications", "last emails", "what was discussed"** → fetch Email/Note/Call records separately (Step 4) and summarize

---

## Step 3 — Fetch the record

Use the appropriate HubSpot tool to retrieve the record:

- **First, call `get_crm_objects` without specifying a properties list** — this returns all default properties and lets you see the full data model before filtering. Use this to verify field names actually exist and contain data before presenting results.
- If you need to confirm whether a specific custom property exists, call `search_properties` with the objectType and a keyword.
- For properties you do request by name, use the verified field names from the property reference below.
- Resolve `hubspot_owner_id` using `search_owners` to show the owner's name, not just the ID. **Important:** To load the `search_owners` tool schema, use `ToolSearch` with the keyword query `owners` (not `search_owners`, which matches the wrong tool). Do NOT use the `select:` prefix with a hardcoded tool name — the tool's full name includes an MCP server prefix that varies by environment.

---

## Step 4 — Fetch recent communications (only for full analysis or when explicitly asked)

**Do NOT use objectType `Activity`** — it returns a validation error. Instead, query each activity type separately:
- `search_crm_objects` with objectType `Email`, filtered by association to the record
- `search_crm_objects` with objectType `Note`, filtered by association to the record
- `search_crm_objects` with objectType `Call`, filtered by association to the record

Merge and sort all results by date descending, take the most recent 10 across all types.
Extract: date, type (Email/Note/Call), direction (inbound/outbound), subject, body summary, sender/recipient.

---

## Step 5 — Output

### Full analysis output

**For a DEAL, output EXACTLY this structure and nothing else:**
```
## Deal: [Name]

| Field | Value | What it means |
|---|---|---|
| Deal Stage | ... | [see stage meanings below] |
| Pipeline | ... | Which sales pipeline |
| Expected Monthly Transaction Volume | ... | Estimated monthly revenue Pliant expects from this deal |
| Total Addressable Monthly Transaction Volume | ... | Full potential monthly spend this customer could bring |
| Trx Volume (Last 0–30 Days) | ... | Transaction volume in the last 30 days |
| Trx Volume (Last 31–60 Days) | ... | Transaction volume from 31 to 60 days ago |
| Trx Volume (Last 61–90 Days) | ... | Transaction volume from 61 to 90 days ago |
| Trx Volume (Last 0–180 Days) | ... | Transaction volume over the last 180 days |
| Close Date | ... | Target date to close the deal |
| Owner | ... | Pliant sales rep responsible |
| Vertical | ... | Industry vertical of the customer |
| Country | ... | Customer's country |

## Recent Communications
[Last 10 activities: Date | Type | Direction | Subject | Summary]

## Key Observations
- [2-4 bullets: current pipeline status, blockers, next steps, anything notable]
```

**Do NOT** include additional properties beyond those 12 fields listed above. Do NOT add supplementary tables (e.g. transaction volumes breakdown, utilization metrics). Do NOT add fields like credit product, customer tier, platform status, key account, JIRA key, onboarding status, or any other HubSpot properties not listed in the template.

---

**For a CONTACT, output EXACTLY this structure and nothing else:**
```
## Contact: [Name]

| Field | Value | What it means |
|---|---|---|
| Job Title | ... | Role at their company |
| Email | ... | Primary email address |
| Phone | ... | Primary phone number |
| Country/Region | ... | Contact's country or region |
| Owner | ... | Pliant rep responsible for this contact |

## Recent Communications
[Last 10 activities]

## Key Observations
- [2-4 bullets: relationship status, last contact, anything notable]
```

**Do NOT** include additional properties beyond those 5 fields listed above. Do NOT add fields like lifecycle stage, lead status, company associations, social profiles, or any other HubSpot properties not listed in the template.

---

**For a COMPANY, output EXACTLY this structure and nothing else:**
```
## Company: [Name]

| Field | Value | What it means |
|---|---|---|
| Domain | ... | Company website domain |
| Vertical | ... | Industry vertical |
| Sub-Vertical | ... | More granular segment within the vertical |
| Country/Region | ... | Company's country or region |
| Owner | ... | Pliant rep responsible |

## Recent Communications
[Last 10 activities]

## Key Observations
- [2-4 bullets: account status, engagement level, anything notable]
```

**Do NOT** include additional properties beyond those 5 fields listed above. Do NOT add fields like industry, revenue, employee count, HubSpot score, lifecycle stage, or any other HubSpot properties not listed in the template.

---

## Property reference

### Deal properties

| Property | HubSpot field name | What it means |
|---|---|---|
| Deal name | `dealname` | Name of the deal or opportunity |
| Deal stage (human-readable) | `name_of_deal_stage` | Current stage label in Pliant's sales pipeline (see stages below). Use this instead of `dealstage`, which returns an internal numeric ID. |
| Pipeline | `pipeline` | Which pipeline this deal belongs to |
| Expected monthly transaction volume | `expected_monthly_transaction_volume` | Estimated monthly revenue Pliant expects from this deal |
| Total addressable monthly transaction volume | `total_addressable_monthly_transaction_volume` | Full potential monthly spend this customer could bring to Pliant |
| Trx volume (last 0–30 days) | `trx_vol_last_0_to_30_days` | Transaction volume in the last 30 days |
| Trx volume (last 31–60 days) | `trx_vol_last_31_to_60_days` | Transaction volume from 31 to 60 days ago |
| Trx volume (last 61–90 days) | `trx_vol_last_61_to_90_days` | Transaction volume from 61 to 90 days ago |
| Trx volume (last 0–180 days) | `trx_vol_last_0_to_180_days` | Transaction volume over the last 180 days |
| Close date | `closedate` | Target date to close or activate the deal |
| Owner | `hubspot_owner_id` | Pliant sales rep responsible for the deal |
| Vertical | `vertical` | Industry vertical of the customer |
| Sub-Vertical | `sub_vertical` | More granular segment within the vertical |
| Country | `country` | Customer's country or region |

### Contact properties

| Property | HubSpot field name | What it means |
|---|---|---|
| First name | `firstname` | Contact's first name |
| Last name | `lastname` | Contact's last name |
| Email | `email` | Primary email address |
| Job title | `jobtitle` | Role at their company |
| Phone | `phone` | Primary phone number |
| Owner | `hubspot_owner_id` | Pliant rep managing the relationship with this contact |
| Country/Region | `country_region` | Contact's country or region |

### Company properties

| Property | HubSpot field name | What it means |
|---|---|---|
| Name | `name` | Company name |
| Domain | `domain` | Company website domain |
| Vertical | `vertical` | Industry vertical |
| Sub-Vertical | `sub_vertical` | More granular segment within the vertical |
| Country/Region | `country_region` | Company's country or region |
| Owner | `hubspot_owner_id` | Pliant rep responsible for this company |

---

## Pliant deal stage meanings

When a deal is at a given stage, interpret and explain it as follows:

| Stage | What it means |
|---|---|
| Solution Qualification / Demo conducted | Customer has landed in the CRM and initial demo has been conducted. Early qualification phase. |
| Pre-Onboarding | Client is in pre-onboarding. Platform registration (transaction link) is underway. Account has been created — waiting on customer to proceed. |
| Submitted to credit | All initial information has been provided and filled out. Pliant Compliance has started the credit assessment. |
| Info requested | Compliance documents have been requested. Waiting on the customer to submit. |
| Info partially obtained | Some compliance documents have been received. Waiting on customer to provide the remaining documents. |
| Info fully obtained | All compliance documents have been received. Pliant Compliance is continuing the full assessment. |
| Submitted to partner bank | Customer has been pre-checked and approved internally. Deal has been submitted to the partner bank for final review. |
| Account activated | Account is ready to use. Cards can be issued. Deal is live. |
| Closed lost | Deal has dropped out of the pipeline. Check the loss reason property if available. |
| Churned | Customer was active but decided to leave Pliant. |
