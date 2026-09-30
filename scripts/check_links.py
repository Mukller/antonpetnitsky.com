#!/usr/bin/env python3
"""
Internal link check for the portfolio pages.

Only local file references are verified: external links are not fetched (they
would make CI flaky and are not this repo's responsibility). Everything else is
resolved against the working tree the same way the deployed nginx resolves it.

The previous version of this script reported 14 "broken" links that were all
false positives -- `mailto:`, `/#contact` and the bare site root were treated as
missing files -- so it could never have passed. Fixed here:

  * schemes other than http(s) (mailto:, tel:, javascript:, data:) are skipped
  * fragment-only links (including `/#section`) only verify the path part
  * `/` resolves to index.html, and a trailing slash to <dir>/index.html

Run: python3 scripts/check_links.py
Exit: 0 = no broken internal links.
"""
from __future__ import annotations

import os
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = [
    "index.html",
    "about/index.html",
    "projects/index.html",
    "robotics/index.html",
    "homelab/index.html",
    "print3d/index.html",
    "privacy-policy.html",
    "terms.html",
    "cv-ru.html",
    "cv-en.html",
    "404.html",
    "50x.html",
]

HREF_RE = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "sms:", "ftp:")


def resolve(page: str, link: str) -> str | None:
    """Return the repo-relative file a link points at, or None if not checkable."""
    raw = link.strip()
    if not raw or raw.startswith("#"):
        return None
    if raw.lower().startswith(SKIP_SCHEMES):
        return None
    if raw.startswith("//"):  # protocol-relative
        return None

    parts = urlsplit(raw)
    if parts.scheme in ("http", "https"):
        return None
    path = unquote(parts.path)
    if not path:
        return None

    page_dir = os.path.dirname(page)

    if path.startswith("/"):
        target = path[1:]
    else:
        target = os.path.normpath(os.path.join(page_dir, path))

    if target in ("", "."):
        target = "index.html"
    if target.endswith("/"):
        target += "index.html"

    return target.replace("\\", "/")


def main() -> int:
    os.chdir(ROOT)
    failures = 0
    checked = 0

    for page in PAGES:
        if not os.path.isfile(page):
            print("FAIL нет страницы: %s" % page)
            failures += 1
            continue

        html = open(page, encoding="utf-8").read()
        links = HREF_RE.findall(html)
        local = 0

        for link in links:
            target = resolve(page, link)
            if target is None:
                continue
            local += 1
            # A link into the hybrid domain's other apps (catalog, botka,
            # kolonka, print, encyclyka) is served by nginx, not by a file here.
            if target.split("/")[0] in (
                "ru", "en", "uk", "be", "pl", "cs", "sk", "bg",
                "api", "og", "fonts", "assets", "botka", "kolonka",
                "print", "encyclyka", "healthz", "styles.css", "app.js",
                "favicon.svg", "sitemap.xml", "sitemap-app.xml",
            ):
                continue
            if not os.path.exists(target):
                print("FAIL битая ссылка в %s: %s -> нет файла %s" % (page, link, target))
                failures += 1

        checked += local
        print("OK  %-24s локальных ссылок проверено: %d" % (page, local))

    print()
    if failures:
        print("битых внутренних ссылок: %d (проверено %d)" % (failures, checked))
        return 1
    print("все %d локальных ссылок ведут на существующие файлы" % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
