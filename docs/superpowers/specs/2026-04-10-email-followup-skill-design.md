# Email Follow-up Skill — Design Spec

**Date:** 2026-04-10
**Status:** Approved

---

## Overview

A Claude Code skill that drafts a post-meeting follow-up email for a Pliant sales rep. The rep invokes it with a meeting or contact name; the skill fetches the Fireflies transcript and HubSpot context, generates a draft, shows it for review, then pushes it directly to Gmail as a draft.

---

## Invocation

```
/email-followup <meeting or contact name>
```

Example: `/email-followup Acme Corp`

---

## Flow

1. **Fetch Fireflies** — search for the most recent transcript matching the argument name
   - Found → extract summary, action items, next steps, participants
   - Not found → prompt rep to paste meeting notes; proceed with those
2. **Fetch HubSpot** — search for matching contact or deal by name
   - Found → extract contact name, email, job title, company, deal stage, owner, last 3 activities
   - Not found → proceed with transcript/notes only; leave Gmail recipient blank
   - Both sources missing → block and ask for at least one
3. **Generate draft** — produce email using both sources; apply adaptive tone (see below)
4. **Show in Claude** — display draft + brief context summary; rep can request edits
5. **Push to Gmail** — when rep signals approval (e.g. "looks good", "send it", "push to Gmail"), create Gmail draft with recipient, subject, and body pre-filled; confirm draft URL back in Claude

---

## Tools Used

| Step | MCP Tool | Purpose |
|---|---|---|
| Fireflies search | `mcp__fireflies-mcp__fireflies_search` / `fireflies_list_transcripts` | Find most recent matching transcript |
| Fireflies detail | `mcp__fireflies-mcp__fireflies_get_transcript` | Full text, action items, summary |
| HubSpot search | `mcp__hubspot-prod__hubspot-search-objects` | Find contact or deal by name |
| HubSpot detail | `mcp__hubspot-prod__hubspot-list-associations` + `hubspot-batch-read-objects` | Deal stage, company, owner, recent activities |
| Gmail draft | `mcp__claude_ai_Gmail__gmail_create_draft` | Create pre-filled draft |

---

## Adaptive Tone Logic

| Deal stage | Tone |
|---|---|
| Solution Qualification / Demo conducted | Warm, curious, low-pressure — reference what was discussed, propose a clear next step |
| Pre-Onboarding → Submitted to credit | Practical and action-oriented — summarize what's needed, confirm next steps |
| Info requested / Info partially obtained | Helpful and nudging — remind without being pushy, make it easy to act |
| Submitted to partner bank → Account activated | Confident and forward-looking — celebrate progress, set expectations |
| No deal stage found | Default to warm + concise |

---

## Email Structure

1. **Opening** — one-sentence personal reference to the meeting
2. **Summary** — 2–3 bullet recap of what was discussed
3. **Next steps** — clear action items (sourced from Fireflies action items when available)
4. **CTA** — one specific ask (e.g. "Does Thursday work for a follow-up call?")
5. **Sign-off** — rep's name (from HubSpot owner field, or left as placeholder)

**Subject line format:** `Follow-up: [Company/Contact Name] — [Meeting Date]`

---

## HubSpot Properties Used

| Property | Field name |
|---|---|
| Contact first + last name | `firstname`, `lastname` |
| Contact email | `email` |
| Job title | `jobtitle` |
| Company name | via association |
| Deal stage | `dealstage` |
| Deal owner | `hubspot_owner_id` (resolved to name via `search_owners`) |

---

## Fallback Behaviour

| Scenario | Behaviour |
|---|---|
| No Fireflies transcript found | Prompt rep to paste notes; proceed with those |
| No HubSpot record found | Proceed with transcript only; Gmail recipient left blank |
| No Fireflies + no HubSpot | Block — ask rep to provide at least one source |
| Fireflies found but no action items | Generate next steps from transcript content only |

---

## Future Enhancement (out of scope for v1)

**BDR writing style matching** — analyse the rep's past sent emails to infer their tone, phrasing, and vocabulary, and apply it to generated drafts. This will make emails feel authentically written by the rep rather than generic AI output.

---

## Skill File

- Path: `skills/email-followup/SKILL.md`
- Allowed tools: Fireflies MCP, HubSpot MCP (prod), Gmail MCP
