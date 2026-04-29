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

POST to the n8n enrichment webhook:

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

Routing inside n8n (automatic):
- `linkedinUrl` present → Clay enriches from LinkedIn → returns `{found, email, phone}`
- `email` present → Clay enriches from email → returns `{found, phone, linkedin}`
- Neither → returns `{found: false}`

Wait for the response (sync, up to 5 minutes). If it times out or returns `found: false`, move to Step 4.

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

## Output Brief

Always display this at the end, regardless of how much was found. Label every field with its source.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name:         [First Last]
Job Title:    [title or "not found"]
Email:        [email] — [Amplemarket / Clay (LinkedIn) / Clay (email) / Clay (via web search) / Web search (unverified) / not found]
Direct Dial:  [phone or "not found"] — [source]
LinkedIn:     [url or "not found"] — [source]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPANY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Domain:       [domain or "not found"]
HQ Phone:     [company phone or "not found"] ← reference only

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COPY TO HUBSPOT MANUALLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Email:        [value] → property: email
Phone:        [direct dial only] → property: phone
LinkedIn:     [url] → property: hs_linkedin_profile_url
Job Title:    [title] → property: jobtitle

⚠️  Do not copy HQ phone to the contact's phone field.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Rules
- Never update HubSpot — not automatically, not after prompting. Output only.
- Direct dial only in the phone field — never HQ/switchboard
- Always label the source of every data point
- Retry `reveal_email` up to 3x before falling back
- If web search finds a LinkedIn URL or email, always re-route through n8n/Clay before stopping
