#!/bin/bash
DISK_THRESHOLD=10
LOG_DIR="$HOME/Scripts-collection/logs"
LOG_FILE="$LOG_DIR/health_check.log"

mkdir -p "$LOG_DIR"

RED='\e[0;31m'
GREEN='\e[0;32m'
YELLOW='\e[0;33m'
NC='\e[0m'

echo "=================================="
echo "      SERVER HEALTH GUARDIAN"
echo "      Date: $(date)"
echo "=================================="

CURRENT_DISK_USAGE=$(df -h / | tail -n 1 | awk '{print $5}' | tr -d '%')

echo "Current disk usage: ${CURRENT_DISK_USAGE}%"

if [[ "$CURRENT_DISK_USAGE" -ge "$DISK_THRESHOLD" ]]; then
    echo -e "${RED} EXCEEDED DISK USAGE THRESHOLD: ${CURRENT_DISK_USAGE}%${NC}"
    echo " Please take action to free up space."
else
    echo -e "${GREEN} Disk usage is within safe limits.${NC}"
fi

echo "----------------------------------"

USED_RAM=$(free -m | awk '/^Mem:/ {print $3}')
TOTAL_RAM=$(free -m | awk '/^Mem:/ {print $2}')

RAM_PERCENT=$(( USED_RAM * 100 / TOTAL_RAM ))

echo "RAM: ${USED_RAM}MB / ${TOTAL_RAM}MB (Usage: ${RAM_PERCENT}%)"

if [[ "$RAM_PERCENT" -ge 80 ]]; then
    echo -e "${RED} EXCEEDED RAM USAGE THRESHOLD: ${RAM_PERCENT}%${NC}"
    echo " Please take action to free up memory."
else
    echo -e "${GREEN} RAM usage is within safe limits.${NC}"
fi  

echo "----------------------------------"

echo "2024-02-10 12:00:01 INFO Application started" > "$LOG_FILE"
echo "2024-02-10 12:05:22 ERROR Database connection failed" >> "$LOG_FILE"
echo "2024-02-10 12:06:00 INFO Retrying..." >> "$LOG_FILE"
echo "2024-02-10 12:06:10 ERROR Timeout waiting for service" >> "$LOG_FILE"

ERROR_COUNT=$(grep -c "ERROR" "$LOG_FILE")

echo "[LOGS] Analiza pliku $LOG_FILE"
echo "       Znaleziono błędów: $ERROR_COUNT"

if [[ $ERROR_COUNT -gt 0 ]]; then
    echo -e "${YELLOW} WARNING:${NC} Found ${RED}$ERROR_COUNT${NC} errors in logs. Please investigate."
else
    echo -e "${GREEN} LOGS CLEAN${NC}"
fi

echo "=========================================="
rm "$LOG_FILE"