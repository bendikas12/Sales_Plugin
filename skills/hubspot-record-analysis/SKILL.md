---
description: Work with any HubSpot record — deal, contact, or company. Executes based on what you ask: full analysis, a specific question, or recent communications. Accepts a name, ID, or HubSpot URL.
argument-hint: [deal/contact/company name, ID, or HubSpot URL]
allowed-tools: mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__get_user_details mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__search_crm_objects mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__get_crm_objects mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__search_properties mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__get_properties mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__search_owners
---

The user has invoked the HubSpot record skill. The argument (if provided) is: $ARGUMENTS

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
- **"Recent communications", "last emails", "what was discussed"** → fetch Activity records only (Step 3) and summarize

---

## Step 3 — Fetch the record

Use the appropriate HubSpot tool to retrieve the record:

- Fetch **all important properties** for the object type (see property reference below)
- Resolve `hubspot_owner_id` using `search_owners` to show the owner's name, not just the ID

---

## Step 4 — Fetch recent communications (only for full analysis or when explicitly asked)

Use `search_crm_objects` with objectType `Activity`, filtered by association to the record.
- Sort by date descending, limit to last 10
- Extract: date, activity type (email/call/note), direction (inbound/outbound), subject, body summary, sender/recipient

---

## Step 5 — Output

### Full analysis output

**For a DEAL:**
```
## Deal: [Name]

| Field | Value | What it means |
|---|---|---|
| Deal Stage | ... | [see stage meanings below] |
| Pipeline | ... | Which sales pipeline |
| Expected Transaction Volume | ... | Estimated revenue Pliant expects from this deal |
| Total Addressable Transaction Volume | ... | Full potential spend this customer could bring |
| Close Date | ... | Target date to close the deal |
| Owner | ... | Pliant sales rep responsible |
| Vertical | ... | Industry vertical of the customer |
| Sub-Vertical | ... | More granular segment within the vertical |
| Country/Region | ... | Customer's country or region |

## Recent Communications
[Last 10 activities: Date | Type | Direction | Subject | Summary]

## Key Observations
- [2-4 bullets: current pipeline status, blockers, next steps, anything notable]
```

**For a CONTACT:**
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

**For a COMPANY:**
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

---

## Property reference

### Deal properties

| Property | HubSpot field name | What it means |
|---|---|---|
| Deal name | `dealname` | Name of the deal or opportunity |
| Deal stage | `dealstage` | Current stage in Pliant's sales pipeline (see stages below) |
| Pipeline | `pipeline` | Which pipeline this deal belongs to |
| Expected transaction volume | `expected_transaction_volume` | Estimated revenue Pliant expects to generate from this deal |
| Total addressable transaction volume | `total_addressable_transaction_volume` | Full potential spend this customer could bring to Pliant |
| Close date | `closedate` | Target date to close or activate the deal |
| Owner | `hubspot_owner_id` | Pliant sales rep responsible for the deal |
| Vertical | `vertical` | Industry vertical of the customer |
| Sub-Vertical | `sub_vertical` | More granular segment within the vertical |
| Country/Region | `country_region` | Customer's country or region |

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
