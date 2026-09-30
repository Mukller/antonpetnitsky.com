# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [v0.3.0] - 2026-09-30

22 commits since v0.2.0, mostly infrastructure. No change to the site's own
content beyond what is listed here.

### Added
- CI. The repository had none for its whole life, so a broken deploy could only
  be caught by a human noticing a page was missing.
  - `scripts/check-deploy-config.py` — the deploy guard. `deploy.sh` is the single
    source of truth for the nginx vhost, and that vhost had been silently
    truncated twice in this project's history: a parallel deploy wrote a stale
    copy over it and took `root`, gzip and the `/assets/` immutable caching with
    it. The guard extracts the heredoc and asserts every block that has ever
    been lost is still present, that braces balance, that there are no duplicate
    exact-match locations (nginx refuses to load the config when there are), and
    that every URL in `sitemap-pages.xml` maps to a real file.
  - `scripts/test-deploy-guard.py` — regression tests for the guard itself: it
    breaks the config in each of the eight ways it has been broken before and
    asserts the guard notices. A guard that cannot fail is worthless. Building
    it surfaced two real holes in the first draft: `location /kolonka/` was
    satisfied by `location /kolonka/sendRawTxt`, and a comment reading
    "compressed by gzip on" satisfied the gzip check.
  - `scripts/check_links.py` — internal link check over 12 pages.
    `check_links_full.py` never ran successfully: it reported 14 broken links
    that were all false positives (`mailto:`, `/#contact`, and the bare site
    root treated as a missing file). Rewritten to resolve paths the way nginx
    does; 104 local links currently pass.

### Fixed
- Restored the `/api/` proxy to the Research Catalog. Without it the catalog's
  tag autocomplete fetch (`/api/tags/suggest`) landed on the portfolio's 404.
- `/print/` (OmniPrint online slicer) 404'd through the portfolio root.
- `/privacy-policy.html` and `/terms.html` were missing from deploy.sh's copy
  list, so they 404'd in production.
- Deploy script no longer keeps its helper scripts in `/tmp`.

### Added (nginx routes for sibling apps)
- `/encyclyka/` — fashion media site, loopback upstream on `:8091`
- `/kolonka/` — smart speaker UI on `:5003`: player, TTS (with SSE streaming
  and raised read timeouts), STT, alarm and plugin routes
- `/botka/`, `/healthz`, `/og/`, `/fonts/`, `/sitemap-app.xml`

### Changed
- deploy.sh carries the complete nginx vhost, including the blocks for every
  sibling app, so a fresh deploy reproduces production exactly.

### Known gaps
- `robotics/media/` still holds only a README: the FIRA photos were never
  uploaded, and the media slots in `robotics/index.html` remain commented out.

## [v0.2.0] - 2026-08-23

### Added
- Custom 404 error page (RU/EN autodetect, robot theme)
- Custom server error page for HTTP 500/502/503/504
- `/projects/` — full catalog of 26 repositories with category filters
- `/robotics/` — detailed robot specs, achievements and media slots
- Social preview image (og.png), local favicon.svg
- sitemap.xml and robots.txt

### Changed
- deploy.sh copies all site assets and configures nginx `error_page`
- Homepage links to new sections

## [v0.1.0] - 2026-08-23

### Added
- Initial public release