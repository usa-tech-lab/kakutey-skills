#!/usr/bin/env python3
"""kakutey アプリを起動する。"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    frontend_dir = os.environ.get("KAKUTEY_FRONTEND_DIR", "")

    if not frontend_dir or not Path(frontend_dir).is_dir():
        print("Error: kakutey frontend directory not found.")
        print("Set KAKUTEY_FRONTEND_DIR or check the path.")
        sys.exit(1)

    frontend_dir = Path(frontend_dir).resolve()
    print(f"Starting kakutey from: {frontend_dir}")

    proc = subprocess.Popen(
        ["npm", "start"],
        cwd=frontend_dir,
        # Windows では shell=True が必要（npm は npm.cmd）
        shell=(sys.platform == "win32"),
    )

    print(f"kakutey started (PID: {proc.pid})")
    print("Backend will be available at http://localhost:8000 in ~10 seconds.")


if __name__ == "__main__":
    main()
