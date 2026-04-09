#!/bin/bash
GLOSSARY_FILE="${CLAUDE_PLUGIN_ROOT}/references/hubspot-glossary.md"

if [ -f "$GLOSSARY_FILE" ]; then
  GLOSSARY=$(cat "$GLOSSARY_FILE")
  jq -n --arg glossary "$GLOSSARY" '{
    "continue": true,
    "suppressOutput": false,
    "systemMessage": "HubSpot Reference Guide:\n\n" + $glossary
  }'
  exit 0
else
  echo "Error: Glossary file not found" >&2
  exit 2
fi
