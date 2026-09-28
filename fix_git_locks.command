#!/bin/bash
# Removes stale git lock files left behind when Claude's sandbox commits into this
# Google Drive folder (the sandbox can unlink() nothing under .git/, so locks stay).
# Double-click this file, then double-click push_now.command.
cd "$(dirname "$0")" || exit 1
echo "Repo: $(pwd)"
for f in .git/index.lock .git/HEAD.lock .git/objects/maintenance.lock .git/refs/heads/main.lock; do
  if [ -e "$f" ]; then rm -f "$f" && echo "removed $f"; fi
done
find .git/objects -name 'tmp_obj_*' -delete 2>/dev/null
echo "--- git status ---"
git status --short | head -20
echo
echo "Done. Now double-click push_now.command to push."
read -n 1 -s -r -p "Press any key to close..."
