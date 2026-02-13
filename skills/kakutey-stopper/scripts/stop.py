#!/usr/bin/env python3
"""kakutey アプリ（バックエンド + フロントエンド）を停止する。"""

import subprocess
import sys


def find_pids_on_port(port):
    """指定ポートでリッスンしているプロセスの PID リストを返す。"""
    pids = set()
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["netstat", "-ano", "-p", "TCP"],
                capture_output=True, text=True, timeout=10,
            )
            for line in result.stdout.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    if parts:
                        pids.add(parts[-1])
        else:
            result = subprocess.run(
                ["lsof", "-iTCP:" + str(port), "-sTCP:LISTEN", "-t"],
                capture_output=True, text=True, timeout=10,
            )
            for line in result.stdout.strip().splitlines():
                if line.strip():
                    pids.add(line.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return list(pids)


def kill_pids(pids):
    """PID リストのプロセスを終了する。"""
    for pid in pids:
        try:
            if sys.platform == "win32":
                subprocess.run(
                    ["taskkill", "/PID", str(pid), "/F"],
                    capture_output=True, timeout=10,
                )
            else:
                subprocess.run(
                    ["kill", str(pid)],
                    capture_output=True, timeout=10,
                )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass


def stop_port(label, port):
    """指定ポートのプロセスを停止する。"""
    pids = find_pids_on_port(port)
    if not pids:
        print(f"{label} (port {port}): not running")
    else:
        kill_pids(pids)
        print(f"{label} (port {port}): stopped (PID {', '.join(pids)})")


def main():
    stop_port("Backend ", 8000)
    stop_port("Frontend", 4200)


if __name__ == "__main__":
    main()
