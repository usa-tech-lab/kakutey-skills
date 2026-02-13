"""勘定科目一覧を取得する。"""

import argparse
import sys

from client import request


def get_accounts(category=None):
    accounts = request("get", "/accounts")
    if category:
        accounts = [a for a in accounts if a["category"] == category]
    accounts.sort(key=lambda a: (a.get("code") or "", a["name"]))
    return accounts


def main():
    parser = argparse.ArgumentParser(description="勘定科目一覧を取得")
    parser.add_argument("--category", choices=["asset", "liability", "equity", "revenue", "expense"],
                        help="カテゴリでフィルタ")
    args = parser.parse_args()

    try:
        accounts = get_accounts(args.category)
        print(f"{'entity_id':>10}  {'code':<6}  {'name':<20}  {'category':<10}")
        print("-" * 55)
        for a in accounts:
            if a.get("is_abstract"):
                continue
            print(f"{a['entity_id']:>10}  {a.get('code') or ''::<6}  {a['name']:<20}  {a['category']:<10}")
        print(f"\n合計: {len(accounts)} 件")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
