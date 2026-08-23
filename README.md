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

🌐 **[antonpetnitsky.com](https://antonpetnitsky.com)**

## Структура

```
index.html          главная страница-витрина
cv-ru.html          CV на русском
cv-en.html          CV на английском
404.html            кастомная страница 404
50x.html            страница ошибок сервера (500/502/503/504)
projects/           каталог всех проектов с фильтрами
robotics/           роботы: спеки, достижения, слоты под медиа
now/                чем занят прямо сейчас
ap-favicon.svg     фавикон (favicon.svg занят приложением-каталогом)
og.png              превью для соцсетей (Open Graph)
sitemap.xml         индекс карт сайта (портфолио + каталог)
sitemap-pages.xml   карта статических страниц портфолио
robots.txt          правила индексации
deploy.sh           деплой на сервер (nginx)
```

## Деплой

Статика раздаётся nginx'ом на домашнем сервере:

```bash
./deploy.sh
```

Скрипт клонирует репо, копирует файлы в `/var/www/antonpetnitsky.com`
и генерирует конфиг nginx с `error_page` для 404 и 5xx.

## Лицензия

Код сайта — MIT. Контент (тексты, фото) — © Anton Petnitsky.
