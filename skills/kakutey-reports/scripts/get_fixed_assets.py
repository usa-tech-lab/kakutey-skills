"""固定資産一覧と減価償却計算を取得する。"""

import argparse
import sys

from client import request


def main():
    parser = argparse.ArgumentParser(description="固定資産一覧を取得")
    parser.add_argument("--depreciation", type=int, metavar="YEAR",
                        help="指定年度の減価償却を計算")
    args = parser.parse_args()

    try:
        assets = request("get", "/fixed-assets")

        if not assets:
            print("固定資産の登録はありません。")
            return

        print(f"\n=== 固定資産一覧 ({len(assets)} 件) ===\n")

        total_depreciation = 0

        for asset in assets:
            print(f"  資産名称:   {asset['name']}")
            print(f"  entity_id:  {asset['entity_id']}")
            print(f"  取得日:     {asset['acquisition_date']}")
            print(f"  取得価額:   {asset['acquisition_cost']:>12,}")
            print(f"  耐用年数:   {asset['useful_life']} 年")
            method = "定額法" if asset["depreciation_method"] == "straight_line" else "定率法"
            print(f"  償却方法:   {method}")

            if args.depreciation:
                dep = request("get", f"/fixed-assets/{asset['entity_id']}/depreciation",
                              params={"target_year": args.depreciation})
                print(f"  --- {args.depreciation}年度 減価償却 ---")
                print(f"  本年分償却費:     {dep['depreciation_expense']:>12,}")
                print(f"  累計償却額:       {dep['accumulated_depreciation']:>12,}")
                print(f"  期末帳簿価額:     {dep['book_value']:>12,}")
                total_depreciation += dep["depreciation_expense"]

            dep_journals = asset.get("depreciation_journals", [])
            if dep_journals:
                print(f"  償却仕訳: {len(dep_journals)} 件")

            print()

        if args.depreciation:
            print(f"  {'━' * 40}")
            print(f"  本年分減価償却費 合計: {total_depreciation:>12,}")
            print()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
