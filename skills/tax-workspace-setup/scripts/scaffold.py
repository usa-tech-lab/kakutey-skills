#!/usr/bin/env python3
"""年度別の確定申告作業用フォルダ構造を生成する。"""

import re
import sys
from pathlib import Path

SUBDIRS = [
    "証憑/01_弊社から顧客への請求書",
    "証憑/02_業者から弊社への請求書・領収書",
    "証憑/03_銀行口座",
    "証憑/04_クレジットカード/csv",
    "証憑/05_paypay",
    "処理",
    "確定申告",
]


def main():
    if len(sys.argv) < 2 or not re.match(r"^\d{4}$", sys.argv[1]):
        print("Usage: python scaffold.py <year> [base_dir]")
        print("  year: 4-digit fiscal year (e.g. 2025)")
        print("  base_dir: directory to create the folder in (default: current directory)")
        sys.exit(1)

    year = sys.argv[1]
    base_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    root = base_dir / year

    created = 0
    for subdir in SUBDIRS:
        d = root / subdir
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created += 1

    if created > 0:
        print(f"Created {year} workspace at: {root.resolve()}")
    else:
        print(f"{year} workspace already exists at: {root.resolve()}")

    print(f"""
Structure:
  {year}/
  ├── 証憑/
  │   ├── 01_弊社から顧客への請求書/
  │   ├── 02_業者から弊社への請求書・領収書/
  │   ├── 03_銀行口座/
  │   ├── 04_クレジットカード/
  │   │   └── csv/
  │   └── 05_paypay/
  ├── 処理/
  └── 確定申告/

Next: place evidence files in 証憑/ subdirectories.""")


if __name__ == "__main__":
    main()
