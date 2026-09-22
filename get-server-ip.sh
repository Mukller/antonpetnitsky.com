#!/bin/bash
# Получить текущий внешний IP сервера и записать в файл

# Внешний IP через curl (если доступен) или через hostname
IP_EXTERNAL=$(curl -s --max-time 5 https://api.ipify.org 2>/dev/null || curl -s --max-time 5 https://ifconfig.me 2>/dev/null || echo "unknown")
IP_DOMAIN=$(host antonpetnitsky.com 2>/dev/null | grep "has address" | awk '{print $4}' || echo "unknown")
IP_LOCAL=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "unknown")

cat > /tmp/current-server-ip.txt <<EOF
External IP (curl): $IP_EXTERNAL
Domain resolved: $IP_DOMAIN
Local IP: $IP_LOCAL
Checked: $(date '+%Y-%m-%d %H:%M:%S')
EOF

echo "Server IP info written to /tmp/current-server-ip.txt"
cat /tmp/current-server-ip.txt
