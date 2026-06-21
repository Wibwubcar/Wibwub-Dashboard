#!/bin/bash
SRC="$HOME/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All/SKILL_update-wibwub_v2.md"
DST="/var/folders/rp/gcgj8vnn68n9v7flmfth963c0000gn/T/claude-hostloop-plugins/967f28441b6e2074/skills/update-wibwub/SKILL.md"

if [ ! -f "$SRC" ]; then
  echo "❌ ไม่พบไฟล์ต้นทาง: $SRC"
  exit 1
fi

cp "$SRC" "$DST" && echo "✅ Skill อัปเดตแล้ว — Step 8B (subfolder path) + Step 8B-2 (ใช้ไฟล์ export แทน Chrome scraping)" || echo "❌ Copy ล้มเหลว — ลอง restart Cowork แล้วรัน apply_skill_update อีกครั้ง"
