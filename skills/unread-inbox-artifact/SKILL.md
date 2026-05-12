---
name: unread-inbox-artifact
description: Create or refresh the rep's "Unread Inbox" live artifact — a persistent Cowork view of unread Gmail threads with one-click AI-drafted replies that get created as Gmail drafts. Use when the user asks for an unread inbox view, a live inbox, an email triage page, an inbox artifact, or wants to set up the inbox drafting tool. The artifact, once created, persists across sessions and reloads its own data from Gmail; this skill only builds or updates it.
---

The user wants the **Unread Inbox** live artifact installed (or refreshed) in their Cowork. The argument (if provided) is: $ARGUMENTS

## What this skill does

It creates a single persisted artifact (id: `unread-inbox`) that:
- Loads the user's unread Gmail threads on open.
- Renders each as a card with sender, subject, snippet, and a row of buttons.
- "AI draft reply" reads the full thread via Gmail's get-thread MCP, sends it to `window.cowork.askClaude()` with a fixed prompt, and fills a textarea with the result.
- "Manual draft" opens an empty textarea.
- "Apply adjustment" revises the current draft according to a free-text instruction.
- "Create draft in Gmail" calls Gmail's create-draft MCP with the textarea contents, addressed to the original sender, threaded as a reply.

The artifact is **self-refreshing** — once installed, the rep clicks Reload in the artifact header to pull fresh unread threads. This skill should only run when the artifact doesn't exist yet, or the user explicitly asks to reinstall/refresh the template.

## Output rules — READ THIS FIRST

- The HTML structure is **fixed**. Use `${CLAUDE_PLUGIN_ROOT}/skills/unread-inbox-artifact/references/artifact-template.html` verbatim and only substitute the `{{TOKEN}}` placeholders defined below. Do not edit the styles, layout, button labels, or the AI prompts inside the template — those have been tuned and should remain consistent across the team.
- The artifact ID is **always** `unread-inbox`. Never invent a different ID — the same ID across reps means each rep has exactly one inbox artifact and re-running this skill updates it in place instead of creating duplicates.
- All Gmail MCP tool IDs and the rep's email address must be resolved at runtime — they vary per user. Do not hardcode any values you happen to see in this prompt or in another rep's installed artifact.

---

## Step 1 — Resolve the rep's Gmail identity

Resolve the invoker's email. Store as `REP_EMAIL`:

Priority (stop at first that succeeds):
1. The Cowork `userEmail` context injected at the top of the conversation (look for a `# userEmail` block).
2. Gmail MCP `get_me` / profile call.
3. `From` header on the 3 most recent sent messages.
4. If none work, stop and ask: *"What email address should the inbox artifact be wired to?"*

Do **not** fall back to any email you've seen in another session, in a sample, or in this prompt. `REP_EMAIL` is the email used for "is this message from me?" comparisons inside the artifact — wrong value silently breaks the AI tone-matching.

---

## Step 2 — Resolve the Gmail MCP tool names

The Gmail MCP server prefix is a per-installation UUID (e.g. `mcp__c129f9cd-30bc-4722-a3b5-8e4d5d16a35c__...`). It differs across reps. Resolve the three tool names this artifact needs:

| Purpose | Tool suffix | Token |
| --- | --- | --- |
| Search threads by query | `search_threads` | `SEARCH_TOOL` |
| Get full thread by id | `get_thread` | `GET_THREAD_TOOL` |
| Create a draft reply | `create_draft` | `DRAFT_TOOL` |

Use `ToolSearch` with the keyword query `gmail` (or `+gmail search_threads`, etc.) to find the current fully-qualified names. Verify each starts with `mcp__` and ends with the expected suffix. If any of the three tools cannot be found, stop and tell the rep: *"Gmail connector isn't installed — connect Gmail in Cowork settings and re-run."* Do not substitute a different mail provider.

---

## Step 3 — Render the template

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/unread-inbox-artifact/references/artifact-template.html`.
2. Substitute every `{{TOKEN}}` exactly once:
   - `{{SEARCH_TOOL}}` — full Gmail search-threads tool name from Step 2.
   - `{{GET_THREAD_TOOL}}` — full Gmail get-thread tool name from Step 2.
   - `{{DRAFT_TOOL}}` — full Gmail create-draft tool name from Step 2.
   - `{{REP_EMAIL}}` — value resolved in Step 1, lowercased.
3. Write the rendered HTML to a workspace file (e.g. `/sessions/<session>/unread-inbox.html`). Do **not** write it to the artifacts directory directly — `create_artifact` / `update_artifact` reads from the path you pass and persists it itself.

---

## Step 4 — Install (or update) the artifact

Check whether the artifact already exists:

1. Call `list_artifacts`.
2. If an entry with `id: "unread-inbox"` exists → call `update_artifact` with that id, the rendered file path, and `update_summary: "Refresh unread-inbox template"`.
3. Otherwise → call `create_artifact` with:
   - `id: "unread-inbox"`
   - `html_path`: the rendered file path
   - `description: "Live view of unread Gmail inbox threads. Each card has AI-draft and manual-draft reply buttons; sending creates a draft in Gmail."`
   - `mcp_tools`: the three fully-qualified names from Step 2, in the order `[SEARCH_TOOL, GET_THREAD_TOOL, DRAFT_TOOL]`.

Pass the three tools to `mcp_tools` even on update — Cowork uses this list to gate `window.cowork.callMcpTool` calls from inside the artifact. Omitting one will make that button fail at runtime with a permissions error.

---

## Step 5 — Confirm in chat

Print exactly this block (substituting values):

```
Unread Inbox artifact installed.
  Wired to: <REP_EMAIL>
  Gmail tools: search_threads, get_thread, create_draft
  Open it from the Cowork sidebar — click Reload to refresh unread threads.
```

If you updated rather than created, replace the first line with `Unread Inbox artifact refreshed.`

Do not paste the rendered HTML into chat. Do not explain the buttons — the artifact is self-explanatory.
