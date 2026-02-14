---
name: kakutey-cli-installer
description: Install the kakutey CLI tool (npm package) for operating the kakutey bookkeeping app from the command line. Run once before using other kakutey-* skills.
---

# kakutey-cli-installer

kakutey CLI（npm パッケージ `kakutey`）をインストールする。

## 前提条件

| ツール | バージョン | インストール |
|--------|-----------|-------------|
| Node.js | v18.0.0 以上 | https://nodejs.org/ |

## 使い方

```bash
python3 scripts/install.py
```

## 処理の流れ

1. 前提条件（node, npm）のバージョンチェック
2. `npm install -g kakutey` でグローバルインストール
3. `kakutey --version` でインストール確認

## インストール後

`kakutey health` でアプリの稼働状態を確認できる。

## 注意

- インターネット接続が必要
- npm のグローバルインストール権限が必要（権限エラーの場合は `sudo` を使用）
- macOS / Linux / Windows 対応
