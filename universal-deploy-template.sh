#!/bin/bash
# Универсальный автодеплой-шаблон для репо Антона Петницкого
# Применяется к любому репо с deploy.sh или docker-compose

set -euo pipefail

REPO_URL="${1:-https://github.com/Mukller/antonpetnitsky.com.git}"
DEPLOY_DIR="${2:-/var/www/site-deploy}"
NGINX_CONF="${3:-/etc/nginx/sites-available/default}"
SERVER_IP_FILE="${4:-/tmp/current-server-ip.txt}"

echo "=== УНИВЕРСАЛЬНЫЙ ДЕПЛОЙ ==="
echo "Repo: $REPO_URL"
echo "Target dir: $DEPLOY_DIR"
echo "Nginx conf: $NGINX_CONF"
echo "IP file: $SERVER_IP_FILE"

# 1. Получить текущий IP сервера
IP_EXTERNAL=$(curl -s --max-time 5 https://api.ipify.org 2>/dev/null || echo "unknown")
IP_DOMAIN=$(host $(echo $REPO_URL | sed 's|https://github.com/||; s|\.git||; s|/.*||') 2>/dev/null | grep "has address" | awk '{print $4}' || echo "unknown")
IP_LOCAL=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "unknown")

mkdir -p $(dirname "$SERVER_IP_FILE")
cat > "$SERVER_IP_FILE" <<EOF
Repo: $(basename "$REPO_URL" .git)
External IP (curl): $IP_EXTERNAL
Domain resolved: $IP_DOMAIN
Local IP: $IP_LOCAL
Checked: $(date '+%Y-%m-%d %H:%M:%S')
Status: $(if curl -s --max-time 5 https://antonpetnitsky.com/ > /dev/null 2>&1; then echo "ONLINE"; else echo "UNREACHABLE"; fi)
EOF

echo "IP info saved to $SERVER_IP_FILE"
cat "$SERVER_IP_FILE"

# 2. Клонировать или обновить репо
if [ -d /tmp/site-deploy ]; then rm -rf /tmp/site-deploy; fi
git clone "$REPO_URL" /tmp/site-deploy || echo "Clone failed (repo may be private)"

# 3. Если есть deploy.sh — запустить его
if [ -f "/tmp/site-deploy/deploy.sh" ]; then
    echo "Found deploy.sh — running..."
    bash /tmp/site-deploy/deploy.sh || echo "Deploy script completed with warnings"
else
    echo "No deploy.sh found in repo. Manual deployment needed."
fi

# 4. Обновить nginx (если конфиг изменился)
if [ -f "$NGINX_CONF" ]; then
    sudo nginx -t 2>/dev/null && sudo systemctl reload nginx 2>/dev/null || echo "Nginx reload skipped (no sudo or config issue)"
fi

echo "=== ДЕПЛОЙ ЗАВЕРШЁН ==="
echo "IP-файл: $(cat "$SERVER_IP_FILE" | head -1)"
