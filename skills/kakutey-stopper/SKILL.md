---
name: kakutey-stopper
description: Stop the running kakutey application by terminating backend (port 8000) and frontend (port 4200) processes. Use when done with bookkeeping operations or before restarting the app.
---

# kakutey-stopper

起動中の kakutey アプリ（バックエンド + フロントエンド）を停止する。

## 使い方

```bash
python3 scripts/stop.py
```

port 8000 (バックエンド) と port 4200 (フロントエンド) をリッスンしているプロセスを検出し、停止する。

## 出力例

```
Backend  (port 8000): stopped (PID 12345)
Frontend (port 4200): stopped (PID 12346, 12347)
```

プロセスが見つからない場合:
```
Backend  (port 8000): not running
Frontend (port 4200): not running
```
