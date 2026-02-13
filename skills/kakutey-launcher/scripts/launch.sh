#!/bin/bash
# kakutey アプリを起動する

FRONTEND_DIR="${KAKUTEY_FRONTEND_DIR:-}"

if [ -z "$FRONTEND_DIR" ] || [ ! -d "$FRONTEND_DIR" ]; then
  echo "Error: kakutey frontend directory not found."
  echo "Set KAKUTEY_FRONTEND_DIR or check the path."
  exit 1
fi

cd "$FRONTEND_DIR"
echo "Starting kakutey from: $FRONTEND_DIR"
npm start &
echo "kakutey started (PID: $!)"
echo "Backend will be available at http://localhost:8000 in ~10 seconds."
