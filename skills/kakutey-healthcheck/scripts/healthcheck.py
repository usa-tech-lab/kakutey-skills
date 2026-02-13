#!/usr/bin/env python3
"""kakutey バックエンド API + フロントエンドのヘルスチェック。"""

import socket
import sys
from urllib.request import urlopen


def check_port(host, port, timeout=2):
    """ポートがリッスン中かどうかを返す。"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        return sock.connect_ex((host, port)) == 0
    finally:
        sock.close()


def check_http(url, timeout=5):
    """URL に GET リクエストを送り HTTP ステータスコードを返す。"""
    try:
        resp = urlopen(url, timeout=timeout)
        return resp.status
    except Exception:
        return None


def main():
    exit_code = 0

    # --- Backend (port 8000) ---
    if not check_port("localhost", 8000):
        print("Backend  (port 8000): NG - nothing listening")
        exit_code = 1
    else:
        status = check_http("http://localhost:8000/api/fiscal-year")
        if status == 200:
            print("Backend  (port 8000): OK - API responding")
        else:
            print(f"Backend  (port 8000): NG - port in use but API not responding (HTTP {status})")
            exit_code = 1

    # --- Frontend (port 4200) ---
    if not check_port("localhost", 4200):
        print("Frontend (port 4200): NG - nothing listening")
        exit_code = 1
    else:
        print("Frontend (port 4200): OK - listening")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
