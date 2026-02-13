"""仕訳を1件登録する。簡易形式と複合仕訳（lines）形式の両方に対応。"""

import json
import sys

from client import request


def resolve_accounts(names):
    """科目名のリストを受け取り {name: entity_id} マッピングを返す。"""
    accounts = request("get", "/accounts")
    acc_map = {a["name"]: a["entity_id"] for a in accounts}
    result = {}
    for name in names:
        if name not in acc_map:
            raise ValueError(f"勘定科目が見つかりません: {name}")
        result[name] = acc_map[name]
    return result


def add_journal(data):
    if "lines" in data:
        # 複合仕訳形式
        account_names = [line["account"] for line in data["lines"]]
        acc_map = resolve_accounts(account_names)
        payload = {
            "date": data["date"],
            "description": data["description"],
            "lines": [
                {"side": l["side"], "account_id": acc_map[l["account"]], "amount": l["amount"]}
                for l in data["lines"]
            ],
            "evidence_ids": data.get("evidence_ids", []),
        }
    else:
        # 簡易形式（debit_account / credit_account / amount）
        acc_map = resolve_accounts([data["debit_account"], data["credit_account"]])
        payload = {
            "date": data["date"],
            "description": data["description"],
            "lines": [
                {"side": "debit", "account_id": acc_map[data["debit_account"]], "amount": data["amount"]},
                {"side": "credit", "account_id": acc_map[data["credit_account"]], "amount": data["amount"]},
            ],
            "evidence_ids": data.get("evidence_ids", []),
        }

    result = request("post", "/journals", payload)
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python add_journal.py '<json>'", file=sys.stderr)
        print()
        print("簡易形式:")
        print('  \'{"date":"2025-01-15","description":"文房具購入","debit_account":"消耗品費","credit_account":"現金","amount":1000}\'')
        print()
        print("複合仕訳形式:")
        print('  \'{"date":"2025-01-01","description":"開始仕訳","lines":[{"side":"debit","account":"現金","amount":50000},{"side":"credit","account":"元入金","amount":50000}]}\'')
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])
        result = add_journal(data)
        print(f"登録完了: entity_id={result['entity_id']}, revision={result['revision']}")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
