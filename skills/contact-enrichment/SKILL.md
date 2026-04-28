---
name: contact-enrichment
description: Enrich a prospect's contact data via Amplemarket (email, direct dial, LinkedIn, job title) then optionally update HubSpot. Use when prospecting a new contact and you need their contact details.
---

# Contact Enrichment Skill

## Purpose
Given a person's name and company, find their email, direct dial phone, LinkedIn URL, and job title.
Primary source: Amplemarket. Fallback: n8n/Clay enrichment workflow. Then optionally update HubSpot.

## Input
Ask the user for (if not already provided):
- First name + Last name
- Company name
- (Optional) Company domain

---

## Step 1 — Amplemarket Person Enrichment

Use `mcp__amplemarket__find_person` with `reveal_email: true`.

If no result or empty response, try `mcp__amplemarket__search_people` using company name and person name.

**Retry rule**: if the response says "Enrichment is still processing" or similar, retry up to 3 times before moving on.

Capture from the result:
- `email` — work email address
- `phone` — **direct dial only** (personal mobile or direct work line). If the number found is a company HQ/switchboard number, do NOT capture it as the person's phone — store it separately as `companyPhone` for reference only.
- `linkedin_url` — LinkedIn profile URL
- `job_title` — the person's current title

**Phone rule**: only set `directDial` if the phone is confirmed as a direct/mobile number. A company main line must never be written to the contact's phone field in HubSpot.

---

## Step 2 — Amplemarket Company Enrichment

Use `mcp__amplemarket__find_company` with domain (preferred) or company name.

Capture only:
- `company_domain` — the company's website domain
- `company_phone` — HQ/switchboard number (shown for reference only, never written to the contact record in HubSpot)

---

## Step 3 — n8n/Clay Fallback (if Step 1 returns no useful data)

Trigger when: Amplemarket returned no email AND no direct dial (LinkedIn URL alone is not enough to skip fallback).

Make an HTTP POST to the n8n enrichment webhook:

**URL**: `https://getpliant.app.n8n.cloud/webhook/contact-enrichment`

**Body**:
```json
{
  "firstName": "<first name>",
  "lastName": "<last name>",
  "company": "<company name>",
  "domain": "<company domain or empty string>",
  "linkedinUrl": "<LinkedIn URL if found by Amplemarket, else omit>",
  "email": "<email if found by Amplemarket, else omit>"
}
```

**Routing logic inside n8n** (handled automatically):
- If `linkedinUrl` is in the body → Clay enriches from LinkedIn → returns `{found, email, phone, source: "clay-linkedin"}`
- If `email` is in the body → Clay enriches from email → returns `{found, phone, linkedin, source: "clay-email"}`
- If neither → returns `{found: false, source: "no-linkedin-or-email-provided"}`

**Wait for the response** — n8n holds the connection until Clay responds (up to 5 minutes). If it times out, note it in the output and skip the fallback result.

Merge the n8n response fields into the contact data, labelling source as "Clay (via n8n)".

---

## Step 4 — Show Results and Confirm HubSpot Update

Display the structured brief (see format below), then ask:

> "Update HubSpot with this data? Type **yes** to update existing record, **create** to create a new contact, or **no** to skip."

- **yes** → search HubSpot for an existing contact by email or name+company. If found, update it silently, then confirm what was written.
- **create** → create a new HubSpot contact with the enriched fields. Confirm the created record URL.
- **no** → skip HubSpot entirely.

**Fields to write to HubSpot contact** (only if data is present):
- `email` — work email
- `phone` — direct dial only (never HQ number)
- `hs_linkedin_profile_url` — LinkedIn profile URL
- `jobtitle` — job title

Never write `companyPhone` to the contact's phone field.

---

## Step 5 — Structured Output Brief

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name:         [First Last]
Job Title:    [title or "not found"]
Email:        [email] — source: [Amplemarket / Clay / not found]
Direct Dial:  [phone or "not found"]
LinkedIn:     [url or "not found"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPANY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Domain:       [domain or "not found"]
HQ Phone:     [company phone or "not found"] ← reference only, not written to HubSpot

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HUBSPOT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Updated ✓ / Created ✓ / Skipped]
```

---

## Rules Summary
- Never add HQ/switchboard number to a contact's phone field — direct dial only
- Always retry `reveal_email` up to 3x before falling back to n8n
- Always label the source of each data point (Amplemarket / Clay / not found)
- Show the brief first, then ask before touching HubSpot
- Company phone (HQ) is displayed in the brief for reference but never written to the contact
