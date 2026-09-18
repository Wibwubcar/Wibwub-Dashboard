#!/bin/bash
# Refreshed 2026-09-18 (Monday weekly update run) — pushes all pending local commits to origin/main
cd "/Users/thanasablilutanon/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
rm -f .git/index.lock .git/HEAD.lock
git push origin main && echo "✅ Push สำเร็จ" || echo "❌ Push ล้มเหลว"
