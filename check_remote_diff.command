#!/bin/bash
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
echo "=== Fetching from GitHub ==="
git fetch origin main
echo ""
echo "=== Commits on GitHub that this Mac does NOT have ==="
git log HEAD..origin/main --oneline
echo ""
echo "=== Files that differ between this Mac and GitHub ==="
git diff HEAD origin/main --stat
echo ""
echo "(This script only LOOKS — it does not change or push anything.)"
