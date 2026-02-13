"""仕訳を更新する。フル更新モードと証憑追加モードに対応。"""

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


def update_full(data):
    """フル更新: 全フィールドを指定して PUT する。"""
    eid = data["entity_id"]

    lines = data["lines"]
    if lines and "account" in lines[0]:
        account_names = [l["account"] for l in lines]
        acc_map = resolve_accounts(account_names)
        lines = [{"side": l["side"], "account_id": acc_map[l["account"]], "amount": l["amount"]} for l in lines]

    payload = {
        "date": data["date"],
        "description": data["description"],
        "lines": lines,
        "evidence_ids": data.get("evidence_ids", []),
        "expected_revision": data["expected_revision"],
    }
    return request("put", f"/journals/{eid}", payload)


def add_evidence(data):
    """証憑追加モード: 既存仕訳に証憑IDを追加する。"""
    eid = data["entity_id"]
    new_ids = data["add_evidence_ids"]

    # 現在の仕訳を取得
    journals = request("get", "/journals")
    journal = next((j for j in journals if j["entity_id"] == eid), None)
    if not journal:
        raise ValueError(f"仕訳が見つかりません: entity_id={eid}")

    existing_ids = journal.get("evidence_ids", [])
    merged_ids = list(set(existing_ids + new_ids))

    payload = {
        "date": journal["journal_date"],
        "description": journal["description"],
        "lines": [{"side": l["side"], "account_id": l["account_id"], "amount": l["amount"]} for l in journal["lines"]],
        "evidence_ids": merged_ids,
        "expected_revision": journal["revision"],
    }
    return request("put", f"/journals/{eid}", payload)


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_journal.py '<json>'", file=sys.stderr)
        print()
        print("フル更新:")
        print('  \'{"entity_id": 1, "date": "2025-01-15", "description": "...", "lines": [...], "evidence_ids": [...], "expected_revision": 1}\'')
        print()
        print("証憑追加:")
        print('  \'{"entity_id": 1, "add_evidence_ids": [10, 20]}\'')
        sys.exit(1)

    try:
        data = json.loads(sys.argv[1])

        if "add_evidence_ids" in data:
            result = add_evidence(data)
            print(f"証憑追加完了: entity_id={result['entity_id']}, revision={result['revision']}")
            print(f"  evidence_ids: {result.get('evidence_ids', [])}")
        else:
            result = update_full(data)
            print(f"更新完了: entity_id={result['entity_id']}, revision={result['revision']}")

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
