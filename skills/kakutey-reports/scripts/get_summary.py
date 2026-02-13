"""損益計算書（P/L）および貸借対照表（B/S）を取得・表示する。"""

import argparse
import sys

from client import request


def print_pl(year):
    pl = request("get", f"/financial-statements/pl/{year}")

    print(f"=== {year}年度 損益計算書 (P/L) ===\n")

    for item in pl.get("items", []):
        name = item["account_name"]
        amount = item["amount"]
        depth = item.get("relative_depth", 0)
        indent = "  " * depth

        if item.get("is_total"):
            print(f"  {'─' * 30}  {'─' * 12}")
            print(f"  {indent}{name:<{30 - depth * 2}}  {amount:>12,}")
        elif item.get("is_abstract"):
            print(f"\n  {indent}【{name}】")
        else:
            print(f"  {indent}{name:<{30 - depth * 2}}  {amount:>12,}")

    print(f"\n  {'━' * 30}  {'━' * 12}")
    print(f"  {'当期純利益':<30}  {pl.get('net_income', 0):>12,}")
    print()


def print_bs(year):
    bs = request("get", f"/financial-statements/bs/{year}")

    print(f"=== {year}年度 貸借対照表 (B/S) ===\n")

    category_labels = {
        "asset": "資産の部",
        "liability": "負債の部",
        "equity": "純資産の部",
    }

    for section in bs.get("sections", []):
        label = category_labels.get(section["category"], section["category"])
        print(f"  【{label}】")

        for item in section.get("items", []):
            name = item["account_name"]
            amount = item["amount"]
            depth = item.get("relative_depth", 0)
            indent = "  " * depth

            if item.get("is_total"):
                print(f"    {'─' * 28}  {'─' * 12}")
                print(f"    {indent}{name:<{28 - depth * 2}}  {amount:>12,}")
            elif item.get("is_abstract"):
                print(f"    {indent}〈{name}〉")
            else:
                print(f"    {indent}{name:<{28 - depth * 2}}  {amount:>12,}")

        print()

    balanced = "OK" if bs.get("is_balanced") else "NG"
    print(f"  当期純利益: {bs.get('net_income', 0):>12,}")
    print(f"  貸借一致: {balanced}")
    print()


def main():
    parser = argparse.ArgumentParser(description="財務諸表を取得")
    parser.add_argument("year", type=int, help="年度")
    parser.add_argument("--type", choices=["pl", "bs", "both"], default="both",
                        help="表示する帳票 (default: both)")
    args = parser.parse_args()

    try:
        if args.type in ("pl", "both"):
            print_pl(args.year)
        if args.type in ("bs", "both"):
            print_bs(args.year)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
