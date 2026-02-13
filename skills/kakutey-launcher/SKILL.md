---
name: kakutey-launcher
description: Start the kakutey bookkeeping application (Electron + FastAPI backend). Use before any kakutey operation when the app is not yet running.
---

# kakutey-launcher

kakutey アプリ（Electron フロントエンド + FastAPI バックエンド）を起動する。

## 起動方法

kakutey リポジトリの `frontend/` ディレクトリで `npm start` を実行する。

```bash
cd /path/to/kakutey/frontend && npm start
```

スクリプトでも起動可能（カレントディレクトリ不問）:

```bash
bash scripts/launch.sh
```

`launch.sh` は環境変数 `KAKUTEY_FRONTEND_DIR`、または `scripts/` からの相対パスで `frontend/` を探す。見つからない場合は `KAKUTEY_FRONTEND_DIR` を設定すること。

## 起動の仕組み

1. `npm start` → `npm-run-all -p electron:serve ng:serve`
2. Angular dev server が port **4200** で起動
3. Electron が port 4200 を待ってから起動し、バックエンド (FastAPI/uvicorn) を port **8000** で自動起動

起動完了まで約10秒。kakutey-healthcheck で確認可能。

## 注意

- 既にアプリが起動している場合、ポート競合でエラーになる
- バックエンドのみ起動したい場合は `kakutey/backend/` で `uv run uvicorn main:app --host 127.0.0.1 --port 8000` を直接実行
