#!/bin/bash
# kakutey アプリ（バックエンド + フロントエンド）を停止する

stop_port() {
  local label="$1"
  local port="$2"

  pids=$(lsof -iTCP:"$port" -sTCP:LISTEN -t 2>/dev/null)

  if [ -z "$pids" ]; then
    echo "$label (port $port): not running"
  else
    kill $pids 2>/dev/null
    echo "$label (port $port): stopped (PID $pids)"
  fi
}

stop_port "Backend " 8000
stop_port "Frontend" 4200
