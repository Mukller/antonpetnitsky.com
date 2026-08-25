<div align="center">

**English** • [Русский](README.md)

</div>

# antonpetnitsky.com

<p align="center">
  <a href="https://github.com/Mukller">
    <img src="https://img.shields.io/badge/Anton%20Petnitsky-Developer-0d1117?style=for-the-badge&logo=github&logoColor=white&labelColor=0d1117&color=58a6ff" alt="Anton Petnitsky" />
  </a>
</p>

Personal portfolio website of Anton Petnitsky: projects, skills, CV (RU/EN).

**[antonpetnitsky.com](https://antonpetnitsky.com)**

## Structure

```
index.html          main portfolio page
cv-ru.html          CV in Russian
cv-en.html          CV in English
404.html            custom 404 page
50x.html            server error page (500/502/503/504)
projects/           full projects catalog with filters
robotics/           robots: specs, achievements, media slots
now/                what I'm doing right now
ap-favicon.svg     favicon (favicon.svg is taken by the catalog app)
assets/fonts/      self-hosted Inter Variable (latin + cyrillic), no Google Fonts
og.png              social preview image (Open Graph)
sitemap.xml         sitemap index (portfolio + catalog app)
sitemap-pages.xml   static portfolio pages sitemap
robots.txt          crawling rules
deploy.sh           deploy to server (nginx)
```

## Deploy

Static files are served by nginx on the home server:

```bash
./deploy.sh
```

The script clones the repo, copies files to `/var/www/antonpetnitsky.com`
and generates an nginx config with `error_page` for 404 and 5xx.

## License

Website code — MIT. Content (texts, photos) — © Anton Petnitsky.
