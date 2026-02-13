#!/bin/bash
# 年度別の確定申告作業用フォルダ構造を生成する

set -euo pipefail

YEAR="${1:-}"
BASE_DIR="${2:-.}"

if [ -z "$YEAR" ] || ! [[ "$YEAR" =~ ^[0-9]{4}$ ]]; then
  echo "Usage: bash scaffold.sh <year> [base_dir]"
  echo "  year: 4-digit fiscal year (e.g. 2025)"
  echo "  base_dir: directory to create the folder in (default: current directory)"
  exit 1
fi

ROOT="$BASE_DIR/$YEAR"

dirs=(
  "$ROOT/証憑/01_弊社から顧客への請求書"
  "$ROOT/証憑/02_業者から弊社への請求書・領収書"
  "$ROOT/証憑/03_銀行口座"
  "$ROOT/証憑/04_クレジットカード/csv"
  "$ROOT/証憑/05_paypay"
  "$ROOT/処理"
  "$ROOT/確定申告"
)

created=0
for d in "${dirs[@]}"; do
  if [ ! -d "$d" ]; then
    mkdir -p "$d"
    created=$((created + 1))
  fi
done

if [ "$created" -gt 0 ]; then
  echo "Created $YEAR workspace at: $(cd "$ROOT" && pwd)"
else
  echo "$YEAR workspace already exists at: $(cd "$ROOT" && pwd)"
fi

echo ""
echo "Structure:"
echo "  $YEAR/"
echo "  ├── 証憑/"
echo "  │   ├── 01_弊社から顧客への請求書/"
echo "  │   ├── 02_業者から弊社への請求書・領収書/"
echo "  │   ├── 03_銀行口座/"
echo "  │   ├── 04_クレジットカード/"
echo "  │   │   └── csv/"
echo "  │   └── 05_paypay/"
echo "  ├── 処理/"
echo "  └── 確定申告/"
echo ""
echo "Next: place evidence files in 証憑/ subdirectories."
