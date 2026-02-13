"""JSON ファイルから仕訳を一括登録する。"""

import json
import sys

from client import request


def build_account_map():
    """全勘定科目の {name: entity_id} マッピングを取得。"""
    accounts = request("get", "/accounts")
    return {a["name"]: a["entity_id"] for a in accounts}


def resolve_lines(lines, acc_map):
    """lines 内の account（科目名）を account_id に解決する。"""
    resolved = []
    for line in lines:
        if "account_id" in line:
            resolved.append(line)
        elif "account" in line:
            name = line["account"]
            if name not in acc_map:
                raise ValueError(f"勘定科目が見つかりません: {name}")
            resolved.append({"side": line["side"], "account_id": acc_map[name], "amount": line["amount"]})
        else:
            resolved.append(line)
    return resolved


def main():
    if len(sys.argv) < 2:
        print("Usage: python bulk_add_journals.py <json_file>", file=sys.stderr)
        print()
        print("JSON ファイルは仕訳オブジェクトの配列。各要素は以下のいずれかの形式:")
        print("  lines 形式: {date, description, lines: [{side, account|account_id, amount}]}")
        print("  簡易形式:   {date, description, debit_account, credit_account, amount}")
        sys.exit(1)

    json_path = sys.argv[1]
    with open(json_path) as f:
        entries = json.load(f)

    print(f"=== {len(entries)} 件の仕訳を登録 ===")
    acc_map = build_account_map()

    created = 0
    errors = []

    for i, entry in enumerate(entries, 1):
        try:
            if "lines" in entry:
                payload = {
                    "date": entry["date"],
                    "description": entry["description"],
                    "lines": resolve_lines(entry["lines"], acc_map),
                    "evidence_ids": entry.get("evidence_ids", []),
                }
            else:
                dr = entry["debit_account"]
                cr = entry["credit_account"]
                if dr not in acc_map:
                    raise ValueError(f"勘定科目が見つかりません: {dr}")
                if cr not in acc_map:
                    raise ValueError(f"勘定科目が見つかりません: {cr}")
                payload = {
                    "date": entry["date"],
                    "description": entry["description"],
                    "lines": [
                        {"side": "debit", "account_id": acc_map[dr], "amount": entry["amount"]},
                        {"side": "credit", "account_id": acc_map[cr], "amount": entry["amount"]},
                    ],
                    "evidence_ids": entry.get("evidence_ids", []),
                }

            request("post", "/journals", payload)
            created += 1
        except Exception as e:
            errors.append((i, entry.get("description", "?"), str(e)))

        if i % 20 == 0 or i == len(entries):
            print(f"  [{i}/{len(entries)}] 登録: {created}, エラー: {len(errors)}")

    print(f"\n完了: 登録={created}, エラー={len(errors)}")
    if errors:
        print("\nエラー一覧:")
        for idx, desc, msg in errors:
            print(f"  #{idx} ({desc}): {msg}")


if __name__ == "__main__":
    main()
