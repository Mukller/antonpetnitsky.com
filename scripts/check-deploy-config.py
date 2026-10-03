#!/usr/bin/env python3
"""
Pre-deploy guard for antonpetnitsky.com.

The worst incident in this repository's history was silent damage to the nginx
vhost: a parallel deploy wrote a stale copy of the config back to disk and the
`root` directive, gzip block and /assets/ immutable caching all disappeared,
which served "Welcome to nginx" to the world or broke font loading. Nothing
caught it until a human looked.

`deploy.sh` is the single source of truth for that config, and it embeds it as a
heredoc. This script extracts the heredoc and asserts the required blocks are
still present, before anyone deploys it.

Run:  python3 scripts/check-deploy-config.py
Exit: 0 = safe to deploy, 1 = something was lost.
"""
from __future__ import annotations

import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# An explicit path can be passed so the guard itself can be regression-tested
# against a deliberately broken config.
DEPLOY = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "deploy.sh")

failures: list[str] = []
warnings: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def extract_nginx_conf(path: str) -> str | None:
    """Pull the heredoc body out of deploy.sh.

    The write line goes through a `$SUDO` variable (it expands to `sudo -n`
    when the caller is not root and to `sudo` otherwise), so the literal
    `sudo tee` spelling is not the only one that has to be recognised.
    """
    src = open(path, encoding="utf-8").read()
    m = re.search(
        r"""(?:\$SUDO|sudo)\s+tee\s+"?\$NGINX_CONF"?\s*>\s*/dev/null\s*<<'(\w+)'\n(.*?)\n\1""",
        src,
        re.S,
    )
    return m.group(2) if m else None


# --- 1. the heredoc must exist --------------------------------------------
conf = extract_nginx_conf(DEPLOY)
if conf is None:
    print("FAIL: не найден heredoc с nginx-конфигом в deploy.sh")
    sys.exit(1)

print("nginx-конфиг извлечён: %d строк" % len(conf.splitlines()))

# Match against the config with comments stripped. A comment must never satisfy
# a requirement: deploy.sh carries the line "# compression for text assets (html
# is compressed by gzip on)", and a naive search for "gzip on" would happily
# pass on a config where the directive itself is gone.
conf_nc = "\n".join(re.sub(r"#.*$", "", line) for line in conf.splitlines())

# --- 2. required blocks ----------------------------------------------------
# Each entry: (human description, pattern). These are the pieces whose loss has
# actually happened before.
def loc(path_fragment: str) -> re.Pattern:
    """Match `location [modifier] <exact path> {`.

    The path must be followed by `{`. Without that anchor, a check for
    `location /kolonka/` is satisfied by `location /kolonka/sendRawTxt {` too,
    and the loss of the real block would go unnoticed.
    """
    return re.compile(
        r"location\s+(?:\^~|~)?\s*=?\s*" + re.escape(path_fragment) + r"\s*\{"
    )


REQUIRED = [
    ("корень (статика портфолио)", re.compile(r"root\s+/var/www")),
    ("try_files для статики", re.compile(r"try_files\s+\$uri")),
    ("gzip", re.compile(r"gzip\s+on")),
    ("immutable-кеш /assets/", loc("/assets/")),
    ("кеш /fonts/", loc("/fonts/")),
    ("локали каталога (regex)", re.compile(r"location\s+~\s+\^/\(ru\|en\|uk")),
    ("JSON API каталога", loc("/api/")),
    ("OG-картинки каталога", loc("/og/")),
    ("healthcheck каталога", loc("/healthz")),
    ("auth-роуты каталога", re.compile(r"location\s+~\s+\^/\(login\|register")),
    ("sitemap приложения", loc("/sitemap-app.xml")),
    ("RSS-лента приложения", loc("/feed.xml")),
    ("Botka Mini App", loc("/botka/")),
    ("Kolonka (TTS)", loc("/kolonka/")),
    ("OmniPrint", loc("/print/")),
    ("Encyclyka", loc("/encyclyka/")),
    ("редирект 80 -> 443", re.compile(r"return\s+301\s+https")),
    ("ssl-сертификат", re.compile(r"ssl_certificate")),
    ("HSTS", re.compile(r"Strict-Transport-Security")),
    ("X-Frame-Options", re.compile(r"X-Frame-Options")),
    ("error_page на кастомные 404/50x", re.compile(r"error_page\s+404")),
]

print("\n=== обязательные блоки ===")
for desc, pattern in REQUIRED:
    ok = pattern.search(conf_nc) is not None
    print("  %-42s %s" % (desc, "OK" if ok else "ОТСУТСТВУЕТ"))
    if not ok:
        fail("в nginx-конфиге потерян блок: %s (паттерн %s)" % (desc, pattern.pattern))

# --- 3. structural sanity --------------------------------------------------
print("\n=== структурная проверка ===")
opens = conf.count("{")
closes = conf.count("}")
print("  скобки: { = %d, } = %d" % (opens, closes))
if opens != closes:
    fail("несбалансированные скобки в nginx-конфиге: %d против %d" % (opens, closes))

if conf.count("server {") < 1:
    fail("в конфиге нет ни одного server-блока")
if conf.count("server_name antonpetnitsky.com") < 1:
    fail("потерян server_name antonpetnitsky.com")

for line in conf.splitlines():
    s = line.strip()
    if not s or s.startswith("#"):
        continue
    # A bare "location /" with no upstream/try_files means the portfolio root
    # stopped being served; this is the exact failure from the old incident.
    if re.fullmatch(r"location\s+/\s*\{\s*\}", s):
        fail("location / пустой — статика портфолио не отдаётся")

# Duplicate exact-match locations are silently rejected by nginx at runtime.
exact = re.findall(r"location\s+=\s+(/\S+)", conf)
dupes = {x for x in exact if exact.count(x) > 1}
if dupes:
    fail("дублирующиеся location = %s — nginx откажется грузить конфиг" % sorted(dupes))

# --- 4. sitemap must point at files that exist -----------------------------
print("\n=== sitemap ===")
sitemap = os.path.join(ROOT, "sitemap-pages.xml")
if not os.path.isfile(sitemap):
    fail("нет sitemap-pages.xml")
else:
    tree = ET.parse(sitemap)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = [e.text for e in tree.iterfind(".//s:loc", ns) if e.text]
    print("  URL в индексе: %d" % len(locs))
    for loc in locs:
        path = loc.split("antonpetnitsky.com", 1)[-1] or "/"
        rel = path.strip("/")
        if not rel:
            target = os.path.join(ROOT, "index.html")
        elif "." in rel.split("/")[-1]:
            target = os.path.join(ROOT, rel)
        else:
            target = os.path.join(ROOT, rel, "index.html")
        exists = os.path.isfile(target)
        print("   %-34s %s" % (path, "OK" if exists else "ФАЙЛА НЕТ -> " + os.path.relpath(target, ROOT)))
        if not exists:
            fail("URL из sitemap не соответствует файлу: %s -> %s" % (path, os.path.relpath(target, ROOT)))

# --- 5. index must reference the app's assets -----------------------------
print("\n=== ссылки на ассеты приложения ===")
idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
for asset in ("styles.css", "app.js", "favicon.svg"):
    pass  # the portfolio pages must NOT reference the catalog's assets
for bad in ("/styles.css", "/app.js"):
    if bad in idx:
        warn("index.html ссылается на %s — этот путь перехватывает каталог-приложение (:8200)" % bad)

# --- verdict ---------------------------------------------------------------
print()
if warnings:
    print("предупреждения:")
    for w in warnings:
        print("  ! %s" % w)

if failures:
    print("\nПРОВАЛЕНО %d проверок — деплой небезопасен:" % len(failures))
    for f in failures:
        print("  x %s" % f)
    sys.exit(1)

print("\nвсе проверки пройдены — деплой безопасен")
sys.exit(0)