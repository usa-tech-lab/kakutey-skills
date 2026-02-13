#!/bin/bash
# kakutey バックエンド API + フロントエンドのヘルスチェック

exit_code=0

# --- Backend (port 8000) ---
if ! lsof -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Backend  (port 8000): NG - port is open (nothing listening)"
  exit_code=1
else
  response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/fiscal-year 2>/dev/null)
  if [ "$response" = "200" ]; then
    echo "Backend  (port 8000): OK - API responding"
  else
    echo "Backend  (port 8000): NG - port in use but API not responding (HTTP $response)"
    exit_code=1
  fi
fi

# --- Frontend (port 4200) ---
if ! lsof -iTCP:4200 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "Frontend (port 4200): NG - port is open (nothing listening)"
  exit_code=1
else
  echo "Frontend (port 4200): OK - listening"
fi

exit $exit_code
