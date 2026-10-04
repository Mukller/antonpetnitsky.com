<div align="center">

[English](README_EN.md) • **Русский**

</div>

# antonpetnitsky.com

<p align="center">
  <a href="https://github.com/Mukller">
    <img src="https://img.shields.io/badge/Anton%20Petnitsky-Developer-0d1117?style=for-the-badge&logo=github&logoColor=white&labelColor=0d1117&color=58a6ff" alt="Anton Petnitsky" />
  </a>
</p>

Персональный сайт-портфолио Антона Петницкого: проекты, навыки, CV (RU/EN).

**[antonpetnitsky.com](https://antonpetnitsky.com)**

## Структура

Все пути ниже проверены и существуют в репозитории.

```
# --- страницы ---
index.html                --> главная страница-витрина
about/index.html          --> обо мне: таймлайн, образование, как работаю
projects/index.html       --> каталог всех проектов с фильтрами
robotics/index.html       --> роботы: спеки, достижения, слоты под медиа
homelab/index.html        --> домашняя инфраструктура: железо, watchdog
print3d/index.html        --> 3D-печать: Klipper, Ender 5 S1
privacy-policy.html       --> политика конфиденциальности
terms.html                --> условия использования
404.html                  --> кастомная страница 404
50x.html                  --> страница ошибок сервера (500/502/503/504)
cv-ru.html                --> CV на русском
cv-en.html                --> CV на английском
cv-ru.pdf                 --> CV на русском, PDF
cv-en.pdf                 --> CV на английском, PDF

# --- медиа и фавиконки ---
og.png                    --> превью для соцсетей (Open Graph)
ap-favicon.svg            --> фавикон (favicon.svg занят приложением-каталогом)
ap-favicon.png            --> то же в PNG
assets/fonts/             --> self-hosted Inter Variable (latin + cyrillic),
                             без Google Fonts; fonts.css + два woff2
googleb85d258bd2c492dc.html --> файл подтверждения прав в Google Search Console

# --- стили и скрипты ---
assets/css/style.css      --> стили страниц портфолио
assets/common.css         --> общие стили
assets/theme.css          --> светлая/тёмная тема
assets/site.js            --> переключатель темы, навигация, aria-current

# --- карта сайта и индексация ---
sitemap.xml               --> индекс карт сайта (портфолио + каталог)
sitemap-pages.xml         --> карта статических страниц портфолио
robots.txt                --> правила индексации

# --- деплой и сервер ---
deploy.sh                 --> деплой на сервер (nginx), единый источник
                             правды по vhost'у (лежит внутри как heredoc)
get-server-ip.sh          --> узнать текущий внешний IP сервера
current-server-ip.txt     --> снимок IP и состояния сервера с историей WAN
universal-deploy-template.sh --> автодеплой-шаблон для других репо
universal-deploy-template.md  --> описание того же шаблона

# --- проверки, которые крутит CI ---
scripts/check-deploy-config.py --> гард nginx-конфига и sitemap
scripts/test-deploy-guard.py   --> самотест гарда (доказывает, что он умеет падать)
scripts/check_links.py         --> проверка внутренних ссылок
check.js                   --> быстрая проверка наличия ключевых блоков в разметке
check_links.py             --> простой линтер ссылок главной (не в CI)
check_links_full.py        --> старая версия проверки ссылок, не используется
load-check.py              --> замер TTFB и размеров ассетов (локально)

# --- CI ---
.github/workflows/ci.yml  --> три шага: гард, его самотест, внутренние ссылки

# --- документация ---
README.md                  --> этот файл (RU)
README_EN.md               --> английская версия
CHANGELOG.md               --> история изменений по версиям
RELEASE_INFO.md            --> текущая версия и дата релиза
CONTRIBUTING.md            --> как Contributing Guide
CODE_OF_CONDUCT.md         -> кодекс поведения
LICENSE.md                 -> лицензия (MIT)
DETAILED_SITE_AUDIT.md     -> разбор сайта
SITE_ANALYSIS.md           -> анализ сайта
SITE_IMPROVEMENT_PLAN.md   -> план улучшений

# --- служебное ---
.gitignore                 -> .DS_Store и *.swp
robotics/media/README.txt  -> naming для фото/видео роботов (самих файлов нет)
```

## Деплой

Статика раздаётся nginx'ом на домашнем сервере:

```bash
./deploy.sh
```

Скрипт клонирует репо, копирует файлы в `/var/www/antonpetnitsky.com`
и генерирует конфиг nginx с `error_page` для 404 и 5xx.

## CI

`.github/workflows/ci.yml` гоняет три проверки на каждом пуше в `main`/`master`
и на каждом pull request:

1. `scripts/check-deploy-config.py` — достаёт vhost nginx'а из heredoc'а внутри
   `deploy.sh` и проверяет, что на месте каждый блок, который хоть раз терялся,
   что скобки сбалансированы, что нет дублирующихся `location =` (nginx откажется
   грузить такой конфиг) и что каждый URL из `sitemap-pages.xml` соответствует
   реальному файлу.
2. `scripts/test-deploy-guard.py` — самотест самого гарда: ломает конфиг всеми
   способами, которыми он ломался раньше, и требует, чтобы гард это заметил.
   Гард, который не может упасть, бесполезен.
3. `scripts/check_links.py` — внутренние ссылки. Внешние намеренно не
   запрашиваются, чтобы CI не краснел из-за чужого сайта.

Зачем это нужно: vhost nginx'а в этом репозитории дважды молча терял целые
блоки — параллельный деплой записывал поверх устаревшую копию и уносил с собой
`root`, gzip и immutable-кеш `/assets/`, — и ни одна проверка этого не ловила.
CI существует прежде всего затем, чтобы такой деплой больше не мог пройти молча.

## Лицензия

Код сайта — MIT. Контент (тексты, фото) — © Anton Petnitsky.
