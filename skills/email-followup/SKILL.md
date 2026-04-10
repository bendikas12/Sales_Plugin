---
description: Draft a post-meeting follow-up email. Fetches the Fireflies transcript and HubSpot context, shows you the draft for review, then pushes it to Gmail as a ready-to-send draft.
argument-hint: [meeting or contact/company name]
allowed-tools: mcp__fireflies-mcp__fireflies_search mcp__fireflies-mcp__fireflies_list_transcripts mcp__fireflies-mcp__fireflies_get_transcript mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__search_crm_objects mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__get_crm_objects mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__search_owners mcp__claude_ai_Gmail__gmail_create_draft
---

The user has invoked the email follow-up skill. The argument (if provided) is: $ARGUMENTS

---

**Guard check:** If `$ARGUMENTS` is empty or the literal string `$ARGUMENTS`, ask the user: *"Which meeting or contact should I draft a follow-up for?"* — then wait for their response and use that as the search term throughout.

---

## Step 1 — Fetch Fireflies transcript

Search Fireflies for the most recent meeting transcript matching `$ARGUMENTS`:
- Use `fireflies_search` with the argument as the query, OR `fireflies_list_transcripts` and find the best title match
- If a match is found: call `fireflies_get_transcript` to retrieve the full transcript
  - Extract: meeting date, participants, summary, action items, key topics discussed
- If no match is found: say — *"No Fireflies transcript found for '$ARGUMENTS'. Please paste your meeting notes below and I'll use those instead."* — then wait for the user's notes before continuing

---

## Step 2 — Fetch HubSpot context

Search HubSpot for a contact or deal matching `$ARGUMENTS`:

**Search for a Contact first:**
- Use `search_crm_objects` with `objectType: "Contact"` and a query filter on `firstname + lastname` or `email`
- If found: fetch `firstname`, `lastname`, `email`, `jobtitle`, `hubspot_owner_id`
- Resolve `hubspot_owner_id` to a name using `search_owners`
- Also check for a deal: use `search_crm_objects` with `objectType: "Object"` and search query using the contact's company name, fetch `dealname`, `dealstage`, `pipeline`

**If no Contact found, search for a Deal:**
- Use `search_crm_objects` with `objectType: "Object"` and query on `dealname`
- If found: fetch `dealname`, `dealstage`, `pipeline`, `hubspot_owner_id`
- Resolve owner name via `search_owners`
- Fetch associated contact if available: `firstname`, `lastname`, `email`, `jobtitle`

**If neither Contact nor Deal is found:**
- Proceed without HubSpot data — note that the Gmail draft will have a blank recipient

**If both Fireflies AND HubSpot return nothing:**
- Stop and say: *"I couldn't find a Fireflies transcript or a HubSpot record for '$ARGUMENTS'. Please either paste your meeting notes or provide a HubSpot contact/deal name."*

---

## Step 3 — Determine tone

Use the deal stage to set the email tone:

| Deal stage | Tone |
|---|---|
| Solution Qualification / Demo conducted | Warm, curious, low-pressure — reference what was discussed, propose a clear next step |
| Pre-Onboarding / Submitted to credit | Practical and action-oriented — summarise what's needed, confirm next steps |
| Info requested / Info partially obtained | Helpful and nudging — remind without being pushy, make it easy to act |
| Submitted to partner bank / Account activated | Confident and forward-looking — celebrate progress, set expectations |
| Info fully obtained | Reassuring and patient — confirm all documents are received and share the expected next steps in the compliance timeline |
| Closed lost / Churned | Do not draft a standard follow-up — ask the user: "This deal is marked as lost/churned. What outcome are you trying to achieve with this email?" |
| No deal stage available | Default to warm + concise |

---

## Step 4 — Generate the email draft

Write a follow-up email using the Fireflies and HubSpot data collected above.

**Structure:**
1. **Opening** — one sentence referencing the meeting specifically (use the meeting date and a key topic)
2. **Summary** — 2–3 bullets recapping what was discussed (from transcript summary or user notes)
3. **Next steps** — bullet list of action items (use Fireflies action items if available; otherwise infer from transcript content)
4. **CTA** — one specific ask, e.g. "Does [day] work for a quick follow-up call?" or "Could you send over [document] by end of week?"
5. **Sign-off** — rep's name from HubSpot owner, or `[Your name]` as placeholder

**Subject line:** `Follow-up: [Company or Contact Name] — [Meeting Date]`
- If neither a company name nor contact name is available from HubSpot or Fireflies, use the raw `$ARGUMENTS` value as the name token.

Apply the tone determined in Step 3.

---

## Step 5 — Show draft for review

Display the email draft in full, preceded by a brief context summary:

```
**Context used:**
- Fireflies: [transcript title + date] / [Manual notes provided]
- HubSpot: [Contact name, job title, company] / [Deal name, stage] / [Not found]
- Recipient email: [email address] / [blank — not found in HubSpot]

---

**Draft:**

Subject: [subject line]

[email body]
```

Then say: *"Let me know if you'd like any changes — or say 'looks good' / 'push to Gmail' to create the draft."*

Wait for the user's response. If they request edits, apply them and show the revised draft. Repeat until approved.

---

## Step 6 — Push to Gmail

When the user signals approval — e.g. "looks good", "send it", "push to Gmail", "create draft", "yes", "go ahead", "perfect", "do it", or any other clear affirmation:

Use `gmail_create_draft` with:
- `to`: contact email from HubSpot (leave empty string `""` if not found)
- `subject`: the subject line from Step 4
- `body`: the email body from Step 4 (plain text, no Markdown formatting — convert any Markdown bullet syntax (`-`) to plain hyphens)

After creating the draft:
- If recipient email was found: confirm *"Gmail draft created. You can find it in your Drafts folder ready to send."*
- If recipient email was blank (not found in HubSpot): confirm *"Gmail draft created — but no recipient email was found in HubSpot. Open the draft in Gmail and add the To address before sending."*
