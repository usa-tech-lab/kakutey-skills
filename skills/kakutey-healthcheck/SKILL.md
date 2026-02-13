---
name: kakutey-healthcheck
description: Check if the kakutey backend API (localhost:8000) and frontend (localhost:4200) are running. Use to verify the app is ready before performing bookkeeping operations.
---

# kakutey-healthcheck

kakutey のバックエンド API (port 8000) とフロントエンド (port 4200) の状態を確認する。

## 使い方

```bash
python3 scripts/healthcheck.py
```

## 出力例

全て正常:
```
Backend  (port 8000): OK - API responding
Frontend (port 4200): OK - listening
```

バックエンドが未起動（ポートも空き）:
```
Backend  (port 8000): NG - nothing listening
Frontend (port 4200): OK - listening
```

ポートは使用中だが API が応答しない:
```
Backend  (port 8000): NG - port in use but API not responding (HTTP 000)
Frontend (port 4200): OK - listening
```
