---
description: Draft a post-meeting follow-up email with broader context — multi-meeting synthesis, prior email thread awareness, engagement history, and the rep's own writing voice. Output renders in Claude for the rep to copy into Gmail. v2 of email-followup, running in parallel for A/B comparison.
argument-hint: [meeting or contact/company name]
---

The user has invoked the email follow-up v2 skill. The argument (if provided) is: $ARGUMENTS

---

**Guard check:** If `$ARGUMENTS` is empty or the literal string `$ARGUMENTS`, ask the user: *"Which meeting or contact should I draft a follow-up for?"* — then wait for their response and use that as the search term throughout.

---

## PREREQUISITE — Identify the sender (who is running this skill)

**Do this BEFORE fetching any Fireflies or HubSpot data**, so meeting-host names and deal-owner names cannot contaminate the identity. Resolve the sender's name + email and store it as `SENDER` — this is the person who will sign the draft in Step 6.

Priority (stop at the first that succeeds):
1. The authenticated Gmail user's profile (use the Gmail MCP's profile / `get_me` call if available) → take `name` and `email`
2. Else, the display name on the `From` header of the user's 3–5 most recent sent emails
3. Else, the local-part of the authenticated Gmail address, title-cased (e.g. `john.smith@acme.com` → "John Smith")
4. Else, **stop and ask the user directly**: *"I couldn't identify your name from Gmail. What name should I sign the email with?"* — then wait for their reply and use that verbatim

**Hard rules — never break these, no matter how tempting the signal looks:**
- `SENDER` is **NOT** the Fireflies meeting host, organizer, or recorder
- `SENDER` is **NOT** any internal participant name found in the Fireflies transcript
- `SENDER` is **NOT** the HubSpot deal or contact owner (`hubspot_owner_id` / `search_owners` result)
- `SENDER` is **NOT** inferred from any name that appears in the transcript, engagement history, or HubSpot record

`SENDER` only comes from the sources in the priority list above. If the priority list fails, you must ask the user — never guess.

---

## Step 1 — Fetch Fireflies transcripts (up to last 3, chronological)

Search Fireflies for recent meeting transcripts matching `$ARGUMENTS`:

- Use `fireflies_search` / `fireflies_list_transcripts` to find matching transcripts
- Select up to the **3 most recent** transcripts within the **last 90 days** that match the argument (by title, participant, or company)
- For each selected transcript, call `fireflies_get_transcript` and extract: meeting date, participants (name + email), summary, structured `action_items`, key topics
- **Order the transcripts oldest → newest** before using them downstream so the draft can reflect progression ("since our first call… on our last call…")
- If only one transcript matches, proceed with just that one
- If no transcript matches: say *"No Fireflies transcript found for '$ARGUMENTS'. Please paste your meeting notes below and I'll use those instead."* — then wait

Also detect the **transcript language** (from Fireflies metadata if available, else infer from the transcript text). Record it for Step 7.

---

## Step 2 — Resolve HubSpot contacts by email

From the most recent transcript, collect external attendee emails (exclude the rep's own domain).

For each attendee email:
- Use `search_crm_objects` with `objectType: "Contact"` and filter on `email` equals the attendee's address — this returns a unique contact (no name ambiguity)
- Fetch: `firstname`, `lastname`, `email`, `jobtitle`, `hubspot_owner_id`, associated company
- Resolve `hubspot_owner_id` to a name via `search_owners`

If a transcript attendee has no email, fall back to a name search for that one attendee only.

Also look up the associated deal:
- Use `search_crm_objects` with `objectType: "Object"` on the company or `dealname` derived from `$ARGUMENTS` / the contact's company
- Fetch: `dealname`, `name_of_deal_stage`, `pipeline`, `hubspot_owner_id`

**If neither a Contact nor Deal is found AND no Fireflies transcript was found in Step 1:** stop and say *"I couldn't find a Fireflies transcript or a HubSpot record for '$ARGUMENTS'. Please paste your meeting notes or provide a HubSpot contact/deal name."*

If HubSpot has no matches but Fireflies does, proceed — the recipient emails come from the transcript.

---

## Step 3 — Pull HubSpot engagement history (cost-bounded)

Fetch engagements on the deal / primary contact with these filters to keep token cost low:

- **Recency:** last 90 days only
- **Count cap:** top 10 most recent engagements
- **Type priority:** prefer `Note` and `Call` engagements first; include `Email` only if there's room under the cap
- **Email truncation:** for email engagements, keep subject + first ~200 characters of body only
- **Pre-summarize immediately:** compress all fetched engagements into a **5-bullet relationship memo** (objections raised, stakeholders mentioned, pricing discussed, commitments made, current status). Use only the memo in Step 6, not the raw engagement data — this keeps edit iterations cheap.

If no engagements exist (new relationship), skip silently.

---

## Step 4 — Check for prior Gmail thread

Search Gmail for the most recent thread with the primary recipient's email (or their company domain), limited to the **last 30 days**:

- If a thread is found: capture the subject line and the last 1–2 messages (truncated to ~300 chars each). Use this as context so the draft references the ongoing conversation naturally.
- If no thread: proceed without prior-thread context.

This is context-only — we are **not** pushing a reply draft to Gmail. Output stays in Claude.

---

## Step 5 — Sample rep's writing voice (last 5 sent emails)

Read the user's **last 5 sent emails** from their Gmail `Sent` folder (or equivalent). Extract lightweight style signals:

- Greeting style (e.g. "Hi [name]," vs "Hey [name]," vs "Hello [name],")
- Average sentence length and paragraph density
- Sign-off phrase (e.g. "Best," / "Cheers," / "Thanks,")
- Formality level and contraction usage
- Any recurring closing phrases

Store these as a short voice profile for Step 6. **This step only affects tone/phrasing — it does not determine the sender's name. The sender was already locked in the PREREQUISITE step as `SENDER`. Do not overwrite `SENDER` here.**

**If the user has no prior sent emails**: skip silently and fall back to the professional baseline only. No prompt.

---

## Step 6 — Generate the email draft

Write a follow-up email using the data gathered in Steps 1–5.

**Tone:**
- **Baseline (always applied):** professional, concise, no slang, no emojis, no over-familiarity
- **Voice overlay:** layer the rep's voice profile from Step 5 on top of the baseline. If no profile exists, use baseline only.
- **Do not** vary tone by deal stage.

**Structure:**
1. **Opening** — reference the meeting(s) specifically. If multiple transcripts were found in Step 1, reflect the progression across them.
2. **Summary** — 2–3 bullets recapping what was discussed (synthesize across transcripts if multiple). Draw on the engagement-history memo (Step 3) for relevant prior context.
3. **Next steps** — use **only** the structured `action_items` from Fireflies. If none exist, write: `- No action items captured — add manually.`  **Do not infer action items from transcript prose.**
4. **Sign-off** — use the sign-off phrase from the voice profile (Step 5), followed by `SENDER.name` from the PREREQUISITE step. **Do NOT use any name from the Fireflies transcript (host, organizer, recorder, or any participant). Do NOT use the HubSpot deal/contact owner. Do NOT use any name that appears in the engagement history.** `SENDER.name` is the only valid source for the sign-off name. It will always be resolved, because the PREREQUISITE step either found it in Gmail or asked the user directly.

**Subject line:** `Follow-up: [Company Name] x Pliant`
- If no company/contact name is available, use the raw `$ARGUMENTS` value.

**Recipients:**
- `To`: primary contact (the main attendee from the most recent transcript, resolved in Step 2)
- `CC`: other external attendees from the transcript who have emails

---

## Step 7 — Language

Draft the email in the language detected in Step 1 (Fireflies transcript language). If detection failed, use the language the rep has been using in the current Claude session. Apply the voice overlay from Step 5 regardless of language (the stylistic signals translate).

---

## Step 8 — Render the full email in Claude

Display the email to the user in this format:

```
**Context used:**
- Fireflies: [N transcript(s): title + date each, oldest → newest] / [Manual notes provided]
- HubSpot: [Contact name(s), job title(s), company] / [Deal name, stage] / [Not found]
- Engagement memo: [5 bullets from Step 3, or "none"]
- Prior Gmail thread: [subject + date] / [none]
- Voice profile: [brief — e.g. "Hi + short sentences + 'Cheers,' sign-off"] / [baseline only — no prior sent emails]
- Signing as: `SENDER.name <SENDER.email>` — resolved in the PREREQUISITE step
- Language: [detected language]

---

**Draft:**

To: [primary email]
Cc: [other attendee emails, or "none"]
Subject: [subject line]

[email body]
```

Then say: *"Let me know if you'd like any changes, or copy this into Gmail when you're happy with it."*

If the user requests edits, apply them and re-render. Repeat until approved. **Do not push to Gmail** — v2 outputs the email in Claude only; the rep copies it over themselves.
