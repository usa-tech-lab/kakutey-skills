---
name: kakutey-installer
description: Download and set up the kakutey bookkeeping application from GitHub. Run once before first use or after major updates to reinstall dependencies.
---

# kakutey-installer

kakutey アプリを GitHub からダウンロードし、依存関係をセットアップする。

## 前提条件

| ツール | バージョン | インストール |
|--------|-----------|-------------|
| Node.js | v22.12.0 以上 | https://nodejs.org/ |
| Python | 3.12 以上 | https://www.python.org/ |
| uv | 最新 | https://docs.astral.sh/uv/getting-started/installation/ |

## 使い方

```bash
# カレントディレクトリに kakutey/ を作成
python3 scripts/install.py

# インストール先を指定
python3 scripts/install.py /path/to/install/dir
```

## 処理の流れ

1. 前提条件（node, python, uv）のバージョンチェック
2. GitHub から kakutey ソースコードの zip をダウンロード・展開
3. バックエンド依存関係のインストール（`uv sync`）
4. フロントエンド依存関係のインストール（`npm install`）

## インストール後

完了メッセージに表示される `KAKUTEY_FRONTEND_DIR` を環境変数に設定すれば、kakutey-launcher でアプリを起動できる。

## 注意

- インターネット接続が必要
- すでにインストール先が存在する場合はソースコードを上書き更新する（`node_modules/` や `.venv/` は保持）
- macOS / Linux / Windows 対応
