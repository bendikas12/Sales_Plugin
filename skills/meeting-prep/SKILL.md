---
description: "Generate a meeting prep brief in minutes — company snapshot, contact intel, tailored discovery questions, pain points, and an opening insight. Uses web research + HubSpot context."
argument-hint: "[contact name] at [company name]"
---

The user has invoked the meeting prep skill. The argument (if provided) is: $ARGUMENTS

---

**Guard check:** If `$ARGUMENTS` is empty or the literal string `$ARGUMENTS`, ask the user: *"Who are you meeting? Please share the contact name and company — e.g. 'Florian Korner at NOSTA'."* — then wait for their response and use that throughout.

---

## Step 1 — Parse input

Extract:
- **Contact name** — the person the user is meeting (e.g. "Florian Korner")
- **Company name** — the company they represent (e.g. "NOSTA")

The expected format is `[contact name] at [company name]`. If only one is provided:
- If just a company name → proceed without a specific contact; skip contact-specific steps
- If just a person name → ask: *"Which company is [name] at?"* and wait for the answer

If the user provides extra context (e.g. "replacing their current card provider", "CFO", "multi-country logistics"), save it as **meeting context** — this will inform the Discovery Questions and Pain Points sections.

---

## Step 2 — Research the company (web)

Use `WebSearch` to research the company. Run 2–3 searches to build a complete picture:

1. `"[company name]"` — general overview
2. `"[company name] news [current year]"` — recent developments
3. `"[company name] revenue employees"` — size and scale (if not clear from search 1)

From the results, use `WebFetch` on the most relevant pages (company website, Crunchbase, press articles) to extract:

- **What they do** — core business, products/services, value proposition
- **Size** — employee count, revenue (if available), funding stage
- **HQ and markets** — where they're based, which countries/regions they operate in
- **Recent news** — anything from the last 6 months: funding rounds, product launches, expansions, leadership changes, partnerships
- **Industry** — sector, vertical, any niche positioning

Summarize findings concisely. Do not include raw search results in the output.

---

## Step 3 — Fetch HubSpot context

Search HubSpot for any existing records related to this company and contact.

**Search for the Company:**
- Use `search_crm_objects` with `objectType: "Organization"` and query on the company name
- If found: fetch `name`, `domain`, `vertical`, `sub_vertical`, `country_region`, `hubspot_owner_id`, `notes_last_updated`
- Resolve owner name via `search_owners`

**Search for a Deal:**
- Use `search_crm_objects` with `objectType: "Object"` and query on the company name
- If found: fetch `dealname`, `name_of_deal_stage`, `pipeline`, `expected_monthly_transaction_volume`, `total_addressable_monthly_transaction_volume`, `closedate`, `hubspot_owner_id`

**Search for the Contact:**
- Use `search_crm_objects` with `objectType: "Contact"` and query on the contact name
- If found: fetch `firstname`, `lastname`, `email`, `jobtitle`, `phone`, `country_region`

**Fetch recent communications** (if a deal or contact was found):
- Query `Email`, `Note`, and `Call` objectTypes filtered by association to the record
- Take the most recent 5 across all types
- Extract key themes, objections, requests, or context mentioned in the communications

**If nothing is found in HubSpot:** That's fine — proceed with web research only. Note in the output that no CRM record was found.

Save any useful CRM context — deal stage, recent conversation themes, known pain points from notes — as **CRM intel** for use in later steps.

---

## Step 4 — Research the contact (web)

Use `WebSearch` to research the contact:

1. `"[contact name]" "[company name]" LinkedIn` — LinkedIn profile
2. `"[contact name]" "[company name]"` — any other mentions (articles, talks, interviews)

From the results, use `WebFetch` on the most relevant pages to extract:

- **Current role** — job title, responsibilities, how long they've been in this role
- **Career path** — previous roles and companies, progression pattern
- **Background** — education, notable achievements, areas of expertise
- **Public presence** — any articles, podcast appearances, conference talks, LinkedIn posts

If the contact cannot be found online, note this and work with whatever is available from HubSpot (job title, email history).

---

## Step 5 — Generate the Meeting Prep Brief

Using all research from Steps 2–4, generate the brief in **exactly** this structure:

---

```
# Meeting Prep Brief: [Contact Name] at [Company Name]

---

## 1. Company Snapshot

**What they do:** [1–2 sentence summary of the business]

**Size:** [employee count, revenue/funding if known]

**HQ & Markets:** [headquarters location, countries/regions they operate in]

**Recent news:**
- [Bullet 1 — most relevant recent development]
- [Bullet 2 — second item if available]

---

## 2. Contact Intel

**Role:** [current job title at company]

**Background:** [2–3 sentences covering career path, previous roles, expertise areas]

**Tenure:** [how long in current role, if known]

**Notable:** [anything distinctive — public talks, articles, board seats, specializations]

---

## 3. Discovery Questions

Based on what we know about [company] and [contact's role]:

1. [Question targeting a strategic priority or challenge the company likely faces — informed by company research]
2. [Question about their current setup/process relevant to what Pliant offers — informed by contact's role]
3. [Question about decision-making or evaluation criteria — informed by deal stage or context]

---

## 4. Pain Points to Probe

Based on [mention the source: deal context / industry research / meeting context provided]:

- **[Pain point 1]:** [1 sentence — why this is likely a pain point and how to surface it]
- **[Pain point 2]:** [1 sentence]
- **[Pain point 3]:** [1 sentence]

---

## 5. Opening Insight

> "[One specific, impressive talking point that shows you did your homework — reference a recent company event, a metric, a market trend relevant to them, or something from the contact's background.]"

**Why this works:** [1 sentence explaining why this opener builds credibility]

---

## 6. CRM Context

| Field | Value | Source |
|---|---|---|
| Vertical | [vertical] | Company |
| Sub-Vertical | [sub_vertical] | Company |
| Country | [country_region] | Company |
| Deal | [dealname] — [deal stage] | Deal |
| Last Activity | [notes_last_updated] | Company |
| Owner | [resolved owner name from hubspot_owner_id] | Company |
```

**Section 6 is conditional:** Only include it if Step 3 found an active deal (not Closed lost or Churned). If no active deal exists, omit Section 6 entirely from the output — do not show an empty table or a placeholder.

---

## Guidelines for generating the brief

- **Be specific, not generic.** Every section should contain details unique to this company and contact. Avoid filler like "They are a leading company in their industry."
- **Discovery questions must be tailored.** Don't use generic sales questions. Each question should reference something specific from the research (a recent expansion, their tech stack, a pain point from CRM notes, their role's priorities).
- **Pain points should be grounded.** If the user provided meeting context (e.g. "replacing provider"), use it. If HubSpot notes mention specific challenges, reference them. If neither exists, infer from industry research — but flag that these are inferred.
- **The opening insight should be memorable.** It should be something the contact wouldn't expect a sales rep to know — a recent company milestone, a specific metric from their annual report, a trend affecting their exact sub-industry.
- **Keep it scannable.** The rep will read this in 2–3 minutes before walking into the meeting. Short sentences, bullets, bold labels.

---

## After delivering the brief

Say: *"Your meeting prep brief is ready. Want me to adjust any section, dig deeper on a specific topic, or draft an opening email to [contact name]?"*
