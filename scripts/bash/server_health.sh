#!/bin/bash

set -u

echo "================================"
echo "       SERVER HEALTH CHECK"
echo "================================"

echo ""
echo "Tanggal: $(date)"
echo "Hostname: $(hostname)"

echo ""
echo "=== Uptime ==="
uptime

echo ""
echo "=== Memory ==="
free -h

echo ""
echo "=== Disk Usage ==="
df -h /

echo ""
echo "=== Service Status ==="

for service in bind9 nginx; do
    if systemctl is-active --quiet "$service"; then
        echo "[OK] $service is running"
    else
        echo "[ERROR] $service is not running"
    fi
done

echo ""
echo "=== Check Complete ==="
