"""証憑ファイルをアップロードする。"""

import os
import sys

from client import upload


def main():
    if len(sys.argv) < 2:
        print("Usage: python upload_evidence.py <file_path> [display_name]", file=sys.stderr)
        print()
        print("例: python upload_evidence.py /path/to/receipt.pdf \"領収書 サンプル商事 2025-01\"")
        sys.exit(1)

    file_path = sys.argv[1]
    display_name = sys.argv[2] if len(sys.argv) >= 3 else os.path.basename(file_path)

    if not os.path.isfile(file_path):
        print(f"Error: ファイルが見つかりません: {file_path}", file=sys.stderr)
        sys.exit(1)

    try:
        result = upload("/evidence", file_path, display_name)
        print(f"アップロード完了:")
        print(f"  entity_id:    {result['entity_id']}")
        print(f"  display_name: {result.get('display_name', display_name)}")
        print(f"  file_type:    {result.get('file_type', '?')}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
