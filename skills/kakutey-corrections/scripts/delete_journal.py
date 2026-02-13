"""仕訳を削除する。"""

import sys

from client import request


def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_journal.py <entity_id>", file=sys.stderr)
        sys.exit(1)

    eid = int(sys.argv[1])

    try:
        result = request("delete", f"/journals/{eid}")
        print(f"削除完了: entity_id={eid}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
