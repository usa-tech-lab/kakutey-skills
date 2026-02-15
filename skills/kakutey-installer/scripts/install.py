#!/usr/bin/env python3
"""kakutey アプリを GitHub からダウンロードしセットアップする。"""

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

REPO_ZIP_URL = "https://github.com/usa-tech-lab/kakutey/archive/refs/heads/main.zip"
ARCHIVE_PREFIX = "kakutey-main"
KAKUTEY_MARKERS = {"backend", "frontend", "package.json"}


def check_command(name):
    """コマンドの存在を確認し、パスを返す。見つからなければ None。"""
    return shutil.which(name)


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
    import re

    match = re.search(r"(\d+)\.(\d+)\.(\d+)", version_str or "")
    if match:
        return tuple(int(x) for x in match.groups())
    return None


def check_prerequisites():
    """前提条件をチェックし、問題があれば一覧表示して終了する。"""
    errors = []

    # Python バージョン（自分自身を確認）
    if sys.version_info < (3, 12):
        errors.append(
            f"  Python 3.12 以上が必要です（現在: {sys.version.split()[0]}）\n"
            f"  https://www.python.org/"
        )

    # Node.js
    node_cmd = check_command("node")
    if not node_cmd:
        errors.append(
            "  node が見つかりません\n"
            "  https://nodejs.org/"
        )
    else:
        ver = parse_version(get_version("node"))
        if ver and ver < (22, 12, 0):
            errors.append(
                f"  Node.js v22.12.0 以上が必要です（現在: {'.'.join(map(str, ver))}）\n"
                f"  https://nodejs.org/"
            )

    # uv
    if not check_command("uv"):
        errors.append(
            "  uv が見つかりません\n"
            "  https://docs.astral.sh/uv/getting-started/installation/"
        )

    # npm（Node.js に付属だが念のため確認）
    if not check_command("npm"):
        errors.append(
            "  npm が見つかりません（Node.js と一緒にインストールされます）\n"
            "  https://nodejs.org/"
        )

    if errors:
        print("前提条件を満たしていません:\n")
        print("\n".join(errors))
        sys.exit(1)

    print("前提条件チェック OK")


def validate_existing_dir(dest):
    """既存ディレクトリが kakutey のインストール先として安全か確認する。"""
    if not dest.exists():
        return
    contents = {item.name for item in dest.iterdir()}
    if not contents:
        return  # 空ディレクトリは OK
    if not contents & KAKUTEY_MARKERS:
        print(f"エラー: {dest} に kakutey 以外のファイルが存在します。")
        print(f"既存ファイル: {', '.join(sorted(contents))}")
        print("別のインストール先を指定するか、ディレクトリを整理してください。")
        sys.exit(1)


def download_and_extract(dest):
    """GitHub から zip をダウンロードし展開する。"""
    dest = Path(dest)
    validate_existing_dir(dest)
    print(f"ダウンロード中: {REPO_ZIP_URL}")

    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "kakutey.zip"
        urlretrieve(REPO_ZIP_URL, zip_path)
        print("展開中...")

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp)

        extracted = Path(tmp) / ARCHIVE_PREFIX

        if dest.exists():
            print(f"既存ディレクトリを更新: {dest}")
            # node_modules や .venv は保持しつつソースを上書き
            for item in extracted.iterdir():
                target = dest / item.name
                if item.is_dir():
                    if target.exists() and item.name in ("node_modules", ".venv"):
                        continue
                    if target.exists():
                        shutil.rmtree(target)
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(extracted, dest)

    print(f"ソースコード取得完了: {dest}")


def install_backend(dest):
    """バックエンド依存関係をインストールする。"""
    backend_dir = Path(dest) / "backend"
    print(f"バックエンドセットアップ中: {backend_dir}")
    subprocess.run(["uv", "sync"], cwd=backend_dir, check=True)
    print("バックエンドセットアップ完了")


def install_frontend(dest):
    """フロントエンド依存関係をインストールする。"""
    frontend_dir = Path(dest) / "frontend"
    print(f"フロントエンドセットアップ中: {frontend_dir}")
    subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
    print("フロントエンドセットアップ完了")


def main():
    if len(sys.argv) > 1:
        dest = Path(sys.argv[1]).resolve()
    else:
        dest = Path.cwd() / "kakutey"

    # インストール先は必ず kakutey/ フォルダにまとめる
    if dest.name != "kakutey":
        dest = dest / "kakutey"

    print(f"=== kakutey installer ===\n")

    check_prerequisites()
    print()
    download_and_extract(dest)
    print()
    install_backend(dest)
    print()
    install_frontend(dest)

    frontend_dir = dest / "frontend"
    print(f"\n=== インストール完了 ===")
    print(f"インストール先: {dest}")
    print(f"\nkakutey-launcher で起動するには:")
    print(f"  export KAKUTEY_FRONTEND_DIR={frontend_dir}")


if __name__ == "__main__":
    main()
