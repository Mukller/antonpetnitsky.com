# Подробный аудит сайта antonpetnitsky.com
Создан: 20.09.2026 · Версия сайта: v3 · Коммит: af3b06f / 2e7038f / 5873dee / 8be90aa

---

## 1. ТЕХНИЧЕСКОЕ СОСТОЯНИЕ

### Структура репо
- `index.html` — главная страница (1991 строка, ~60 КБ без CSS)
- `cv-en.html`, `cv-ru.html` — CV на двух языках
- `404.html`, `50x.html` — кастомные ошибки
- `projects/`, `robotics/`, `homelab/`, `print3d/`, `about/` — подстраницы
- `assets/` — шрифты (self-hosted Inter), CSS (`style.css`, `theme.css`, `common.css`), `site.js`
- `deploy.sh` — деплой-скрипт с nginx конфигом
- `get-server-ip.sh` — скрипт получения текущего IP сервера (добавлен)
- `universal-deploy-template.sh` — универсальный шаблон для всех репо
- `SITE_ANALYSIS.md`, `SITE_IMPROVEMENT_PLAN.md` — анализ и план
- `current-server-ip.txt` — текущий IP сервера в репо
- `privacy-policy.html`, `terms.html` — юридические страницы

### Nginx конфигурация (deploy.sh)
- Слушает 80 (redirect 301 на https)
- 443 ssl с сертификатами Let's Encrypt
- Компрессия gzip включена (level 5)
- Кэш `/assets/` (immutable, 30 дней)
- Прокси для Research Catalog (`:8200`), Botka (`:8310`), Smart Speaker (`:5003` — Kolonka)
- Security headers добавлены (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `HSTS`)
- `map` для sitemap-app.xml, `/fonts/`, `/og/`

### CSS состояние
- Темная тема по умолчанию (`#0C0C0D`), светлая через `[data-theme="light"]`
- Шрифт: `Inter Tight` (self-hosted, latin + cyrillic woff2)
- CSS-переменные для цветов, отступов, радиуса, анимаций
- Utility-классы для отступов (`.mt-sm`, `.mb-xl`, `.gap-md` и т.д.)
- Responsive: `@media (max-width: 720px)` и `@media (max-width: 480px)`
- Mobile sticky CTA (.sticky-mobile-cta) добавлен с `z-index: 150`, `fixed`, `bottom: 16px`
- Touch targets улучшены для мобильного (`min-height: 44px` для `.contact-card`, `.nav a`)

---

## 2. ЧТО БЫЛО СДЕЛАНО В ЭТОЙ СЕССИИ

### Безопасность (Этап 1)
- [x] Security headers в nginx (X-Content-Type-Options, X-Frame-Options, CSP, HSTS, Referrer-Policy)
- [x] HTTPS принудителен (301 redirect в nginx)
- [x] robots.txt актуален
- [x] sitemap.xml актуален
- [x] Проверка secrets в deploy.sh (нет вшитых ключей)
- [x] Проверка .env / переменных окружения (нет в репо)

### Юридические страницы (Этап 2)
- [x] `privacy-policy.html` (noindex, nofollow — базовый текст без сбора данных)
- [x] `terms.html` (noindex, nofollow — базовые условия)
- [x] Ссылки в footer `index.html` (Privacy Policy · Terms of Use)
- [x] Sitemap не обновлён для этих страниц (они noindex — это правильно)
- [x] Meta robots (`noindex, follow`) добавлены

### SEO / Мета-теги (Этап 3)
- [x] Уникальные title на подстраницах (`About`, `Projects`, `Robotics`, `Homelab`, `Print3d`)
- [x] Meta descriptions присутствуют
- [x] Alt text на изображении (`hero-avatar img` — `alt="Anton Petnitsky"`)
- [x] Structured data (JSON-LD Person schema) добавлен в head `index.html`
- [ ] `og.png` — 101 КБ, не сжат (осталось из опциональных)
- [x] Sitemap актуален

### Пользовательский опыт / Контент (Этап 4)
- [x] FAQ (5 вопросов) добавлен в `index.html`
- [x] Breadcrumbs присутствуют в подстраницах (`Index / About` и т.д.)
- [x] Case study (`Safalife`) присутствует в секции `Explore`
- [ ] Team photo — нет фото автора в высоком разрешении (оставлено как опциональное)
- [x] Response time promise добавлен (`Within 24 hours`)
- [x] Cookie consent banner добавлен (сохранение в localStorage)
- [ ] Real reviews / testimonials — нет отзывов (оставлено как опциональное)
- [ ] Maps + directions — нет физического адреса (оставлено)
- [x] Sticky mobile CTA добавлен

### Аналитика / Производительность (Этап 5)
- [x] Analytics (Plausible script добавлен в head)
- [ ] Скрипт проверки скорости загрузки — не добавлен (опционально)
- [x] Mobile responsive — viewport meta + responsive CSS присутствуют
- [ ] Цветовой контраст — не проверен инструментально (CSS использует хорошую контрастность: `#ECE6DA` на `#0C0C0D`, `#B8924A` на `#0C0C0D`)
- [x] CTA присутствует (hero ссылки, sticky mobile CTA)
- [x] Broken links проверены через `check_links.py` — 0 broken

### Финальная проверка (Этап 6)
- [x] Все ссылки проверены (внутренние + внешние)
- [ ] Формы — нет форм на сайте (N/A)
- [ ] Spam protection — нет форм (N/A)
- [x] Meta-теги актуальны
- [x] Sitemap + robots.txt актуальны
- [x] Финальный коммит (`3c151f8` → `af3b06f` → `2e7038f` → `5873dee` → `e60cc41` → `90d5cc6` → `2e7038f` ... финальный `3c151f8` для улучшений + `af3b06f` для мобильной оптимизации)
- [x] Сайт на живом сервере отвечает 200 OK
- [x] Nginx config валиден и содержит Kolonka proxy + security headers

---

## 3. ОСТАВШИЕСЯ ОПЦИОНАЛЬНЫЕ ЗАДАЧИ (из плана, не критично)

1. **Сжатие `og.png`** (101 КБ → можно сжать до ~30-50 КБ через `pngquant` или `oxipng`)
2. **Проверка цветового контраста** инструментально (`axe-core`, `lighthouse` accessibility audit)
3. **Добавление фото автора** (если появится фото в хорошем разрешении)
4. **Отзывы / testimonials** (если появятся реальные отзывы клиентов)
5. **Maps + directions** (если нужен физический адрес или карта Минска)
6. **Скрипт проверки скорости загрузки** (`lighthouse-cli` или базовая метрика в `check.js`)

---

## 4. ЧТО ЕЩЁ МОЖНО СДЕЛАТЬ (предложено пользователем)

- **Автодеплой для всех репо**: `universal-deploy-template.sh` + `universal-deploy-template.md` созданы. Работает для любого репо с `deploy.sh` или без (ручная настройка).
- **IP-трекинг**: `get-server-ip.sh` интегрирован в `deploy.sh`. При каждом деплое IP обновляется в `current-server-ip.txt` и в репо.
- **Текущий статус сервера**: сервер временно был недоступен (timeout), сейчас восстановлен (`46.216.19.51`, `200 OK`, SSH работает).
