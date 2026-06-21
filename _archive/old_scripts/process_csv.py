#!/usr/bin/env python3
import json, base64, io, csv, sys
from collections import defaultdict

# Read the saved download file
saved_file = "/var/folders/rp/gcgj8vnn68n9v7flmfth963c0000gn/T/claude-hostloop-plugins/a8d001833b717686/projects/-Users-thanasablilutanon-Library-Application-Support-Claude-local-agent-mode-sessions-63474075-287d-46b7-bbd8-5f5bc16621e4-b7d79abc-f657-493b-8a54-c51cdb92110f-local-2777b6f1-4477-4091-8dc7-b92b1ddc2a-h44hdp/8fb8b59a-ee7c-4d57-8a3f-532c7d59b8b9/tool-results/mcp-631cf5b2-d348-4eff-a244-06b07fea56f7-download_file_content-1779931045020.txt"

with open(saved_file) as f:
    data = json.load(f)

csv_b64 = data['content']
csv_bytes = base64.b64decode(csv_b64)
csv_text = csv_bytes.decode('utf-8')

reader = csv.reader(io.StringIO(csv_text))
rows = list(reader)

print(f"Total rows: {len(rows)}")
print("\nFirst 40 rows (structure):")
for i, row in enumerate(rows[:40]):
    print(f"{i}: {row}")
