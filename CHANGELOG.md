# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [v0.2.0] - 2026-08-23

### Added
- Custom 404 error page (RU/EN autodetect, robot theme)
- Custom server error page for HTTP 500/502/503/504
- `/projects/` — full catalog of 26 repositories with category filters
- `/robotics/` — detailed robot specs, achievements and media slots
- `/now/` — what I'm building and running right now
- Social preview image (og.png), local favicon.svg
- sitemap.xml and robots.txt

### Changed
- deploy.sh copies all site assets and configures nginx `error_page`
- Homepage links to new sections

## [v0.1.0] - 2026-08-23

### Added
- Initial public release