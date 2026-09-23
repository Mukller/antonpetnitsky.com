# Универсальный автодеплой для репо Антона

Создан в рамках сессии по улучшению сайта (анализ 3 скриншотов с рекомендациями).

## Как работает

`universal-deploy-template.sh` принимает 4 параметра:
1. `REPO_URL` — URL репозитория (по умолчанию: antonpetnitsky.com)
2. `DEPLOY_DIR` — директория для деплоя
3. `NGINX_CONF` — путь к nginx конфигу
4. `SERVER_IP_FILE` — куда записать текущий IP

## Применение ко всем репо

Для любого репо из воркспейса (`botka-platform`, `minecraft-survival-server`, `safalife-*`, `smart-speaker`, `voice-notes`, `tiktok-streak-bot` и др.):

```bash
bash /tmp/site-deploy/universal-deploy-template.sh \
  "https://github.com/Mukller/<repo>.git" \
  "/var/www/<repo>" \
  "/etc/nginx/sites-available/<repo>"
```

Если в репо есть `deploy.sh` — скрипт запустит его автоматически. Если нет — сообщит, что нужна ручная настройка.

## Интеграция с текущим репо (antonpetnitsky.com)

- `get-server-ip.sh` — получает IP и записывает в `current-server-ip.txt`
- `current-server-ip.txt` — текущий статус сервера в репо (коммит `e60cc41`)
- `SITE_ANALYSIS.md` — анализ 3 скриншотов (60 рекомендаций)
- `SITE_IMPROVEMENT_PLAN.md` — план в 6 этапов
- Коммиты: `8be90aa` (деплой + безопасность), `5873dee` (IP скрипт), `e60cc41` (IP файл), `90d5cc6` (финальный статус)
