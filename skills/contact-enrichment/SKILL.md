---
name: contact-enrichment
description: Enrich a prospect's contact data via Amplemarket (email, direct dial, LinkedIn, job title) with Clay/n8n and web search fallbacks. Use when prospecting a new contact and you need their contact details.
---

# Contact Enrichment Skill

## Purpose
Given a person's name and company (or a LinkedIn URL), find their email, direct dial phone, LinkedIn URL, and job title.
Sources in order: Amplemarket → n8n/Clay → Web search.
Output is a structured brief. HubSpot is never updated automatically.

## Input
Ask the user for (if not already provided):
- First name + Last name + Company name
- OR a LinkedIn URL directly (skips Amplemarket person search, goes straight to n8n/Clay)
- (Optional) Company domain

---

## Step 1 — Amplemarket Person Enrichment

Use `mcp__amplemarket__find_person` with `reveal_email: true`.

If no result or empty response, try `mcp__amplemarket__search_people` using company name and person name.

**Retry rule**: if the response says "Enrichment is still processing", retry up to 3 times before moving on.

Capture:
- `email` — work email address
- `phone` — **direct dial only** (personal mobile or direct work line). If the number is a company HQ/switchboard, do NOT capture it as a person phone — store it as `companyPhone` for Step 2 reference only.
- `linkedin_url` — LinkedIn profile URL
- `job_title` — current title

If the user provided a LinkedIn URL directly as input, skip Step 1 and go to Step 3.

---

## Step 2 — Amplemarket Company Enrichment

Use `mcp__amplemarket__find_company` with domain (preferred) or company name.

Capture only:
- `company_domain`
- `company_phone` — HQ/switchboard (shown in brief for reference, never written to HubSpot contact)

---

## Step 3 — n8n/Clay Fallback

**Trigger when**: Step 1 returned no email AND no direct dial (a LinkedIn URL alone is not enough to skip this step).

Also trigger here directly if the user provided a LinkedIn URL as input (skipping Step 1).

### 3a — POST to n8n webhook

**URL**: `https://getpliant.app.n8n.cloud/webhook/contact-enrichment`

**Body**:
```json
{
  "firstName": "<first name>",
  "lastName": "<last name>",
  "company": "<company name>",
  "domain": "<company domain or empty string>",
  "linkedinUrl": "<LinkedIn URL if available, else omit>",
  "email": "<email if available, else omit>"
}
```

n8n responds immediately with `{"message":"Workflow was started"}`. Clay runs in background (1–5 min).

Routing inside n8n (automatic):
- `linkedinUrl` present → Clay enriches from LinkedIn → returns `{found, email, phone}`
- `email` present → Clay enriches from email → returns `{found, phone, linkedin}`
- Neither → returns `{found: false}` immediately

### 3b — Find the execution ID

Immediately after the POST, list the most recent executions:

```
n8n_executions(action="list", workflowId="fIdH8yhvewzFWN0p", limit=1)
```

Take `executions[0].id` — that's the execution just started.

### 3c — Poll for result

```
n8n_executions(action="get", id="<executionId>", mode="summary")
```

- `status == "waiting"` → Clay hasn't responded yet — poll again (max 6 min / ~15 polls)
- `status == "success"` → done, read output (see 3d)
- `status == "error"` or 6 min elapsed → fall through to Step 4

### 3d — Read result

```
n8n_executions(action="get", id="<executionId>", mode="filtered", nodeNames=["Relevant Info", "Relevant info", "Not Found Result"])
```

The Set node output contains:
- `found` — boolean or string `"true"`/`"false"`
- `email` — work email (LinkedIn path)
- `phone` — direct dial
- `linkedin` — LinkedIn URL (email path)
- `source` — `"clay-linkedin"` | `"clay-email"` | `"no-linkedin-or-email-provided"`

If `found` is false or source is `"no-linkedin-or-email-provided"`, move to Step 4.

---

## Step 4 — Web Search Fallback

**Trigger when**: Step 3 returned nothing, timed out, or was skipped (no LinkedIn URL, no email to pass).

Run web searches to find contact data from public sources:
1. `"{first name} {last name}" "{company}" email` — look for email address
2. `"{first name} {last name}" "{company}" phone OR contact` — look for direct phone number
3. `"{first name} {last name}" "{company}" LinkedIn` — look for LinkedIn profile URL
4. `site:{company_domain} "{first name} {last name}"` — look for contact page, team page, or bio

Extract from results:
- Email address (from team pages, press releases, directory listings)
- Phone number (direct line or mobile — flag clearly if it might be a switchboard)
- LinkedIn profile URL

**If a LinkedIn URL or email is found via web search**:
→ Re-run Step 3 with that LinkedIn URL or email in the webhook body. Label results as "Clay (via web search)".

**If Step 3 also finds nothing after web search**:
→ Report what was found from web search alone and label source as "Web search (unverified)".

---

## Output

Always show two blocks at the end.

**Block 1 — Research summary** (sources for reference):
```
Name:        [First Last]
Job Title:   [title] — [source]
Email:       [email] — [source]
Phone:       [phone] — [source]
LinkedIn:    [url] — [source]
Domain:      [domain]
HQ Phone:    [company phone] ← reference only, do NOT copy to contact
```

**Block 2 — HubSpot copy-paste** (values only, no sources, ready to paste):
```
📋 COPY TO HUBSPOT

Email:      [value or leave blank]
Phone:      [direct dial only — leave blank if not found]
LinkedIn:   [url or leave blank]
Job Title:  [title or leave blank]
```

No extra text in Block 2. Just the four lines. User copies them directly into HubSpot contact properties.

---

## Rules
- **Never update HubSpot** — not automatically, not after any prompt. Output only.
- Direct dial only in Phone — never HQ/switchboard number
- Always label source in Block 1
- Retry `reveal_email` up to 3x before falling back
- If web search finds a LinkedIn URL or email, always re-route through n8n/Clay before stopping
