#!/usr/bin/env python3
"""
Render the sales dashboard HTML by substituting {{TOKEN}} placeholders.

Usage:
    echo '{"REP_NAME":"Jane Doe","CALLS_WEEK":"12",...}' | python3 render_dashboard.py <template_path> <output_path>

- Reads a JSON object from stdin where keys are token names (without braces)
- Reads the HTML template from <template_path>
- Replaces every {{KEY}} with the corresponding value
- Writes the result to <output_path>
- Prints a confirmation line to stdout

Any {{TOKEN}} not present in the JSON input is left as-is (so you'll see
the raw placeholder in the output — useful for spotting missing metrics).
"""

import json
import sys
import os


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 render_dashboard.py <template_path> <output_path>", file=sys.stderr)
        sys.exit(1)

    template_path = sys.argv[1]
    output_path = sys.argv[2]

    # Read token values from stdin
    tokens = json.load(sys.stdin)

    # Read template
    with open(template_path, "r") as f:
        html = f.read()

    # Substitute every {{KEY}} with its value
    for key, value in tokens.items():
        html = html.replace("{{" + key + "}}", str(value))

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Write output
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Dashboard written to {output_path}")


if __name__ == "__main__":
    main()
