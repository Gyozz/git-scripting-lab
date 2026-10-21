#!/usr/bin/env python3

import json
import shutil
import socket
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "python_health.jsonl"

SERVICES = ["bind9", "nginx"]


def check_service(service):
    result = subprocess.run(
        ["systemctl", "is-active", service],
        capture_output=True,
        text=True,
        check=False,
    )

    status = result.stdout.strip() or "unknown"

    return {
        "service": service,
        "status": status,
        "active": result.returncode == 0,
    }


def get_disk_usage():
    usage = shutil.disk_usage("/")
    return {
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
        "used_percent": round(
            usage.used / usage.total * 100, 2
        ),
    }


def collect_data():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hostname": socket.gethostname(),
        "disk": get_disk_usage(),
        "services": [
            check_service(service) for service in SERVICES
        ],
    }


def main():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    data = collect_data()

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(data) + "\n")

    print(json.dumps(data, indent=2))
    print(f"\nLog tersimpan di: {LOG_FILE}")


if __name__ == "__main__":
    main()
