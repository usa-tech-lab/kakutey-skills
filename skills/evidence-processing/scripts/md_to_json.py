"""仕訳一覧 MD → 仕訳データ JSON 変換スクリプト

07_仕訳一覧.md を読み取り、同ディレクトリに 07_仕訳データ.json を出力する。

Usage:
    python md_to_json.py <path/to/07_仕訳一覧.md>
"""

import json
import os
import re
import sys


def parse_accounts_table(lines, start_idx):
    """勘定科目一覧テーブルをパースし、科目名 → entity_id のマッピングを返す。"""
    accounts = {}
    i = start_idx
    # ヘッダー行とセパレータ行をスキップ
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "---" in line:
            i += 1
            break
        i += 1

    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            break
        cols = [c.strip() for c in line.split("|")]
        # cols[0] は空文字（先頭の | の前）
        if len(cols) >= 4:
            name = cols[1].strip()
            try:
                entity_id = int(cols[2].strip().replace(",", ""))
                accounts[name] = entity_id
            except ValueError:
                pass
        i += 1
    return accounts


def parse_amount(text):
    """金額文字列をパースして整数を返す。"""
    text = text.strip().replace(",", "").replace("**", "")
    if not text:
        return 0
    return int(text)


def parse_journals_table(lines, start_idx, accounts):
    """仕訳一覧テーブルをパースし、仕訳リストを返す。"""
    journals = []
    i = start_idx
    # ヘッダー行とセパレータ行をスキップ
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "---" in line:
            i += 1
            break
        i += 1

    current_journal = None
    errors = []

    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith("|"):
            break

        cols = [c.strip() for c in line.split("|")]
        if len(cols) < 7:
            i += 1
            continue

        no_str = cols[1].strip()
        date_str = cols[2].strip()
        desc = cols[3].strip()
        debit_acct = cols[4].strip()
        credit_acct = cols[5].strip()
        amount_str = cols[6].strip()

        if no_str:
            # 新しい仕訳の開始
            if current_journal:
                journals.append(current_journal)
            current_journal = {
                "date": date_str,
                "description": desc,
                "lines": [],
            }

        if current_journal is None:
            i += 1
            continue

        amount = parse_amount(amount_str)

        if debit_acct:
            if debit_acct not in accounts:
                errors.append(f"Line {i + 1}: unknown debit account '{debit_acct}'")
            else:
                current_journal["lines"].append(
                    {"side": "debit", "account_id": accounts[debit_acct], "amount": amount}
                )
        if credit_acct:
            if credit_acct not in accounts:
                errors.append(f"Line {i + 1}: unknown credit account '{credit_acct}'")
            else:
                current_journal["lines"].append(
                    {"side": "credit", "account_id": accounts[credit_acct], "amount": amount}
                )

        i += 1

    if current_journal:
        journals.append(current_journal)

    return journals, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python md_to_json.py <path/to/07_仕訳一覧.md>")
        sys.exit(1)

    md_path = sys.argv[1]
    if not os.path.isfile(md_path):
        print(f"Error: file not found: {md_path}")
        sys.exit(1)

    with open(md_path, encoding="utf-8") as f:
        lines = f.readlines()

    lines = [l.rstrip("\n") for l in lines]

    # 勘定科目一覧テーブルを探す
    accounts = {}
    accounts_start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s*勘定科目一覧", line):
            accounts_start = i + 1
            break

    if accounts_start is None:
        print("Error: '## 勘定科目一覧' section not found")
        sys.exit(1)

    accounts = parse_accounts_table(lines, accounts_start)
    if not accounts:
        print("Error: no accounts found in 勘定科目一覧 table")
        sys.exit(1)

    print(f"Accounts loaded: {len(accounts)}")

    # 仕訳一覧テーブルを探す
    journals_start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s*仕訳一覧", line):
            journals_start = i + 1
            break

    if journals_start is None:
        print("Error: '## 仕訳一覧' section not found")
        sys.exit(1)

    journals, errors = parse_journals_table(lines, journals_start, accounts)

    if errors:
        print(f"\nWarnings ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

    # 検証: 各仕訳の貸借一致チェック
    balance_errors = 0
    for j_idx, j in enumerate(journals):
        debit_total = sum(l["amount"] for l in j["lines"] if l["side"] == "debit")
        credit_total = sum(l["amount"] for l in j["lines"] if l["side"] == "credit")
        if debit_total != credit_total:
            print(f"  Balance error in journal #{j_idx + 1} ({j['date']} {j['description']}): "
                  f"debit={debit_total}, credit={credit_total}")
            balance_errors += 1

    # 出力
    out_dir = os.path.dirname(md_path)
    json_path = os.path.join(out_dir, "07_仕訳データ.json")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(journals, f, ensure_ascii=False, indent=2)

    print(f"\nJournals: {len(journals)}")
    if balance_errors:
        print(f"Balance errors: {balance_errors}")
    print(f"Output: {json_path}")


if __name__ == "__main__":
    main()
