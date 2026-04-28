#!/bin/bash
jq -n '{
  "continue": true,
  "suppressOutput": false,
  "systemMessage": "Guru — company knowledge source:\n\nWhenever the user asks about internal company knowledge — Pliant policies, processes, playbooks, product details, sales enablement, onboarding / compliance procedures, internal FAQs, or anything that would live in an internal wiki — you MUST use the Guru connector (MCP tools, typically prefixed with `guru`) to search Guru before answering. Do not answer from general knowledge or assumptions for these topics.\n\nIf no Guru tool is available in the current session, tell the user the Guru connector is not connected and ask them to enable it, rather than guessing.\n\nThis does NOT apply to HubSpot CRM data (deals, contacts, companies, pipeline) — that stays on the HubSpot connector."
}'
exit 0
