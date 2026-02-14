#!/usr/bin/env python3
"""kakutey CLI (npm パッケージ) をインストールする。"""

import shutil
import subprocess
import sys
import re


def get_version(cmd, flag="--version"):
    """コマンドのバージョン文字列を取得する。"""
    try:
        result = subprocess.run(
            [cmd, flag], capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip() or result.stderr.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def parse_version(version_str):
    """バージョン文字列から (major, minor, patch) タプルを抽出する。"""
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version_str or "")
    if match:
        return tuple(int(x) for x in match.groups())
    return None


def check_prerequisites():
    """前提条件をチェックし、問題があれば一覧表示して終了する。"""
    errors = []

    # Node.js
    if not shutil.which("node"):
        errors.append(
            "  node が見つかりません\n"
            "  https://nodejs.org/"
        )
    else:
        ver = parse_version(get_version("node"))
        if ver and ver < (18, 0, 0):
            errors.append(
                f"  Node.js v18.0.0 以上が必要です（現在: {'.'.join(map(str, ver))}）\n"
                f"  https://nodejs.org/"
            )

    # npm
    if not shutil.which("npm"):
        errors.append(
            "  npm が見つかりません（Node.js と一緒にインストールされます）\n"
            "  https://nodejs.org/"
        )

    if errors:
        print("前提条件を満たしていません:\n")
        print("\n".join(errors))
        sys.exit(1)

    print("前提条件チェック OK")


def install_kakutey_cli():
    """kakutey CLI をグローバルインストールする。"""
    print("kakutey CLI をインストール中...")
    result = subprocess.run(
        ["npm", "install", "-g", "kakutey"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"インストールに失敗しました:\n{result.stderr}")
        print("\n権限エラーの場合は sudo を使用してください:")
        print("  sudo npm install -g kakutey")
        sys.exit(1)
    print("インストール完了")


def verify_installation():
    """インストールされた kakutey CLI のバージョンを確認する。"""
    version = get_version("kakutey")
    if version:
        print(f"kakutey {version}")
    else:
        print("警告: kakutey コマンドが見つかりません")
        print("npm のグローバルインストール先が PATH に含まれているか確認してください")
        sys.exit(1)


def main():
    print("=== kakutey CLI installer ===\n")

    check_prerequisites()
    print()
    install_kakutey_cli()
    print()
    verify_installation()

    print("\n=== インストール完了 ===")
    print("kakutey health でアプリの稼働状態を確認できます")


if __name__ == "__main__":
    main()
