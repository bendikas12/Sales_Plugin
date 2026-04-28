# Email Follow-up Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the `email-followup` skill that drafts a post-meeting follow-up email by fetching a Fireflies transcript and HubSpot context, showing the draft for review, then pushing it to Gmail.

**Architecture:** A single `SKILL.md` file containing step-by-step instructions for Claude to follow when invoked. No executable code — the skill is a prompt that orchestrates three MCP integrations (Fireflies, HubSpot, Gmail) sequentially.

**Tech Stack:** Claude Code skill (Markdown), Fireflies MCP, HubSpot MCP (UUID-based OAuth), Gmail MCP

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `skills/email-followup/SKILL.md` | **Overwrite** (currently empty) | Full skill logic: fetch → generate → review → push |
| `.claude-plugin/plugin.json` | **Modify** | Bump version `0.2.0` → `0.3.0` |
| `CHANGELOG.md` | **Modify** | Add `0.3.0` entry |

---

## Task 1: Write the email-followup SKILL.md

**Files:**
- Overwrite: `skills/email-followup/SKILL.md`

> Note on HubSpot tools: the working HubSpot MCP uses UUID-based tool names (`mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__*`), not `mcp__hubspot-prod__*` (which returns 401). Use the UUID format below — it matches the existing `hubspot-record-analysis` skill.

- [ ] **Step 1: Write the SKILL.md**

Replace the empty `skills/email-followup/SKILL.md` with the full content below:

```markdown
---
description: Draft a post-meeting follow-up email. Fetches the Fireflies transcript and HubSpot context, shows you the draft for review, then pushes it to Gmail as a ready-to-send draft.
argument-hint: [meeting or contact/company name]
allowed-tools: mcp__fireflies-mcp__fireflies_search mcp__fireflies-mcp__fireflies_list_transcripts mcp__fireflies-mcp__fireflies_get_transcript mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__search_crm_objects mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__get_crm_objects mcp__65af63f1-c198-41c6-a145-1c45ebb0e415__search_owners mcp__claude_ai_Gmail__gmail_create_draft
---

The user has invoked the email follow-up skill. The argument (if provided) is: $ARGUMENTS

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
- Also check for an associated deal: use `search_crm_objects` with `objectType: "Object"` filtered by contact association, fetch `dealname`, `dealstage`, `pipeline`

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

When the user signals approval (e.g. "looks good", "send it", "push to Gmail", "create draft"):

Use `gmail_create_draft` with:
- `to`: contact email from HubSpot (leave empty string `""` if not found)
- `subject`: the subject line from Step 4
- `body`: the email body from Step 4 (plain text)

After creating the draft, confirm: *"Gmail draft created. You can find it in your Drafts folder ready to send."*
```

- [ ] **Step 2: Verify the file was written correctly**

Open `skills/email-followup/SKILL.md` and confirm:
- Frontmatter block is present with `description`, `argument-hint`, and `allowed-tools`
- 6 numbered steps are present
- No empty sections

- [ ] **Step 3: Commit**

```bash
git add skills/email-followup/SKILL.md
git commit -m "feat: implement email-followup skill"
```

---

## Task 2: Bump version and update changelog

**Files:**
- Modify: `.claude-plugin/plugin.json`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update plugin.json**

Change `version` from `"0.2.0"` to `"0.3.0"`:

```json
{
  "name": "sales-plugin",
  "description": "Pliant Sales Team productivity plugin — daily dashboard, deal prep, email follow-ups",
  "version": "0.3.0"
}
```

- [ ] **Step 2: Update CHANGELOG.md**

Prepend a new entry at the top of the file:

```markdown
## 0.3.0 - 2026-04-10
- Added: email-followup skill — drafts post-meeting follow-up emails using Fireflies transcript + HubSpot context, with Gmail draft push
```

- [ ] **Step 3: Commit**

```bash
git add .claude-plugin/plugin.json CHANGELOG.md
git commit -m "chore: bump version to 0.3.0"
```

---

## Task 3: Manual smoke test

> No automated tests exist for skill files — testing is done by invoking the skill and verifying the behaviour at each branch.

- [ ] **Step 1: Test happy path (Fireflies + HubSpot both found)**

Invoke the skill with a real company/contact name that has a recent Fireflies meeting and a HubSpot record.

Expected behaviour:
1. Skill fetches transcript without prompting for notes
2. Skill fetches HubSpot contact/deal without error
3. Draft is displayed with context summary showing both sources used
4. Subject line matches format `Follow-up: [Name] — [Date]`
5. Email has opening, summary bullets, next steps, CTA, sign-off
6. After "looks good", Gmail draft is created and confirmation shown

- [ ] **Step 2: Test Fireflies not found fallback**

Invoke the skill with a name that has no Fireflies transcript.

Expected behaviour:
1. Skill says "No Fireflies transcript found for '[name]'. Please paste your meeting notes..."
2. After pasting notes, draft is generated using only those notes + HubSpot data

- [ ] **Step 3: Test HubSpot not found fallback**

Invoke the skill with a name that exists in Fireflies but not in HubSpot.

Expected behaviour:
1. Draft is generated using transcript only
2. Context summary shows "HubSpot: Not found"
3. Gmail draft recipient field is blank

- [ ] **Step 4: Commit test results (note any bugs found)**

If the skill behaves correctly across all three tests:
```bash
git add .
git commit -m "test: manual smoke test pass for email-followup skill"
```

If bugs are found, fix `skills/email-followup/SKILL.md` and re-run the failing test before committing.

---

## Task 4: Push branch and open PR

- [ ] **Step 1: Push branch**

```bash
git push -u origin feat/email-followup-skill
```

- [ ] **Step 2: Open PR**

```bash
gh pr create \
  --title "feat: email-followup skill v0.3.0" \
  --body "$(cat <<'EOF'
## Summary
- Implements `email-followup` skill: fetches Fireflies transcript + HubSpot context, generates adaptive-tone follow-up email, shows draft for review, pushes to Gmail
- Bumps plugin version to 0.3.0

## Test plan
- [ ] Happy path: Fireflies + HubSpot both found → full draft → Gmail push
- [ ] Fireflies not found → prompts for notes → draft generated
- [ ] HubSpot not found → transcript-only draft → blank Gmail recipient

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

> Note: `gh` CLI may not be installed. If this command fails, open the PR manually on GitHub from the `feat/email-followup-skill` branch.
