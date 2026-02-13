"""登録済み証憑を検索する。"""

import argparse
import sys

from client import request


def main():
    parser = argparse.ArgumentParser(description="証憑を検索")
    parser.add_argument("--name", help="表示名で部分一致検索")
    parser.add_argument("--tag", help="タグ名で検索")
    args = parser.parse_args()

    if not args.name and not args.tag:
        print("--name または --tag のいずれかを指定してください。", file=sys.stderr)
        sys.exit(1)

    try:
        params = {}
        if args.name:
            params["display_name"] = args.name
        if args.tag:
            params["tag"] = args.tag

        results = request("get", "/evidence/search", params=params)

        print(f"\n検索結果: {len(results)} 件")
        print("-" * 80)
        print(f"{'EID':>6}  {'display_name':<40}  {'file_type':<20}  {'tags'}")
        print("-" * 80)

        for ev in results:
            tags = ", ".join(t["name"] for t in ev.get("tags", []))
            print(f"{ev['entity_id']:>6}  {ev.get('display_name', '?'):<40}  {ev.get('file_type', '?'):<20}  {tags}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
