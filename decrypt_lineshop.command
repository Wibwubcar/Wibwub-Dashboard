#!/bin/bash
# decrypt_lineshop.command — ถอดรหัส Line My Shop files แล้วสร้าง CSV

set -e
BASE="$HOME/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"
LINE_DIR="$BASE/data ยอดขาย plaform/Line My Shop"
OUT_DIR="$BASE/data ยอดขาย plaform/Line My Shop/decrypted"

mkdir -p "$OUT_DIR"

# Install msoffcrypto if needed
pip3 install msoffcrypto-tool --quiet 2>/dev/null || true

python3 << 'PYEOF'
import msoffcrypto, io, csv, os, glob
from pathlib import Path
import openpyxl

BASE = Path(os.path.expanduser("~/Library/CloudStorage/GoogleDrive-thanasab.li@gmail.com/.shortcut-targets-by-id/1-TeohYqk3oWyyTHTbnLIjXW8mAqYowRe/Digital Marketing/claude/All"))
LINE_DIR = BASE / "data ยอดขาย plaform" / "Line My Shop"
OUT_DIR = LINE_DIR / "decrypted"
DL_DIR = Path(os.path.expanduser("~/Downloads"))
PASSWORD = "5000113570"

# Find all Order Report files
files = list(LINE_DIR.glob("*.xlsx")) + list(DL_DIR.glob("Order Report*.xlsx"))
print(f"Found {len(files)} files")

all_data = {}  # order_id → (date, amount, month)

for fp in files:
    print(f"\nProcessing: {fp.name}")
    try:
        with open(str(fp), 'rb') as f:
            of = msoffcrypto.OfficeFile(f)
            of.load_key(password=PASSWORD)
            dec = io.BytesIO()
            of.decrypt(dec)
        dec.seek(0)
        wb = openpyxl.load_workbook(dec, read_only=True, data_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        print(f"  Headers: {rows[0][:8]}")
        
        # Aggregate by month
        from collections import defaultdict
        monthly = defaultdict(lambda: {'rev':0,'ord':0})
        
        for row in rows[1:]:
            if not row or not row[0]: continue
            # Find order ID and amount columns
            # Typical structure varies - find date and amount
            for i, v in enumerate(row):
                if isinstance(v, str) and v.startswith('20') and len(v) >= 8:
                    date_str = v[:10]
                    month = int(date_str[5:7]) if '-' in date_str else None
                    break
            else:
                month = None
            # Try to find amount
            # Print first row to understand structure
            if rows.index(row) == 1:
                print(f"  Row1: {row[:10]}")
            break
        
        wb.close()
        print(f"  ✅ Decrypted successfully")
        
        # Save decrypted
        dec.seek(0)
        out_path = OUT_DIR / f"decrypted_{fp.stem}.xlsx"
        with open(str(out_path), 'wb') as f:
            f.write(dec.read())
        print(f"  Saved: {out_path.name}")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n✅ Done. Decrypted files saved to:", OUT_DIR)
PYEOF
