#!/usr/bin/env python3
"""
Regression-test the deploy guard itself.

A guard that never fails is worthless, and this repo has already been bitten by
config damage that no check caught. So: break the config in every way it has
been broken before, and assert the guard notices.

Run: python3 scripts/test-deploy-guard.py
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPLOY = os.path.join(ROOT, "deploy.sh")
GUARD = os.path.join(ROOT, "scripts", "check-deploy-config.py")

if not os.path.isfile(DEPLOY):
    sys.exit("deploy.sh не найден")

src = open(DEPLOY, encoding="utf-8").read()


def heredoc(text: str) -> tuple[str, str]:
    m = re.search(
        r"""(?:\$SUDO|sudo)\s+tee\s+"?\$NGINX_CONF"?\s*>\s*/dev/null\s*<<'(\w+)'\n(.*?)\n\1""",
        text,
        re.S,
    )
    if not m:
        sys.exit("heredoc не найден")
    return m.group(1), m.group(2)


TAG, BODY = heredoc(src)


def make(broken_body: str) -> str:
    """Put a broken heredoc body back into a full deploy.sh."""
    return src[: src.index(BODY)] + broken_body + src[src.index(BODY) + len(BODY):]


# Each case: (name, transformation, must_be_reported_as_missing)
CASES = [
    (
        "потерян root (тот самый инцидент с Welcome to nginx)",
        lambda b: re.sub(r"^\s*root\s+/var/www[^;]*;\s*$", "", b, count=1, flags=re.M),
        "корень",
    ),
    (
        "потерян gzip",
        lambda b: re.sub(r"gzip\s+on\s*;", "", b),
        "gzip",
    ),
    (
        "потерян immutable-кеш /assets/",
        lambda b: b.replace("location ^~ /assets/ {", "location /assets-old/ {"),
        "/assets/",
    ),
    (
        "потерян JSON API каталога",
        lambda b: b.replace("location ^~ /api/ {", "location ^~ /api-old/ {"),
        "/api/",
    ),
    (
        "потерян Encyclyka",
        lambda b: b.replace("location ^~ /encyclyka/ {", "location ^~ /enc-old/ {"),
        "/encyclyka/",
    ),
    (
        "потерян OmniPrint",
        lambda b: b.replace("location /print/ {", "location /print-old/ {"),
        "/print/",
    ),
    (
        "потерян Kolonka",
        lambda b: b.replace("location /kolonka/ {", "location /kolonka-old/ {"),
        "/kolonka/",
    ),
    (
        "потерян RSS-лента каталога",
        lambda b: b.replace("location = /feed.xml {", "location = /feed-old.xml {"),
        "RSS-лента приложения",
    ),
    (
        "потерян sitemap приложения",
        lambda b: b.replace("location = /sitemap-app.xml {", "location = /sitemap-old.xml {"),
        "sitemap приложения",
    ),
    (
        "потерян локали каталога",
        lambda b: re.sub(r"location\s+~\s+\^/\(ru\|en\|uk[^)]*\)[^{]*\{", "", b, count=1),
        "локали каталога",
    ),
]


def run_guard(path: str) -> tuple[int, str]:
    # The encoding must be pinned. With text=True Python decodes the guard's
    # output using the locale code page, which is cp1251 on a Russian Windows box.
    # That does not raise -- the bytes decode into mojibake ('корень' arrives as
    # 'РєРѕСЂРµРЅСЊ') -- so every Cyrillic marker lookup below silently fails and
    # each broken config is reported as "not caught" even though the guard did its
    # job. UTF-8 is what the guard actually writes, on every platform.
    r = subprocess.run([sys.executable, GUARD, path], capture_output=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


print("=== 1. исправный конфиг должен проходить ===")
rc, out = run_guard(DEPLOY)
print("  код возврата: %d  %s" % (rc, "OK" if rc == 0 else "ПРОБЛЕМА — на нормальном конфиге падает"))
if rc != 0:
    print(out)
    sys.exit(1)

print("\n=== 2. каждая поломка должна ловиться ===")
missed = []
with tempfile.TemporaryDirectory() as td:
    for name, transform, marker in CASES:
        broken_body = transform(BODY)
        if broken_body == BODY:
            print("  %-58s ПРОПУЩЕНО (трансформация ничего не сделала)" % name)
            missed.append(name)
            continue
        path = os.path.join(td, "deploy-broken.sh")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(make(broken_body))
        rc, out = run_guard(path)
        caught = rc != 0 and marker in out
        print("  %-58s %s" % (name, "поймано" if caught else "НЕ ПОЙМАНО"))
        if not caught:
            missed.append(name)

print("\n=== 3. несбалансированные скобки ===")
with tempfile.TemporaryDirectory() as td:
    path = os.path.join(td, "deploy-brace.sh")
    # Drop one closing brace at the very end of the vhost.
    broken_body = BODY.replace("    location / {\n        try_files $uri $uri/ =404;\n    }\n}",
                              "    location / {\n        try_files $uri $uri/ =404;\n    }", 1)
    if broken_body == BODY:
        print("  %-58s ПРОПУЩЕНО (трансформация ничего не сделала)" % "удалена закрывающая скобка")
        missed.append("скобки")
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(make(broken_body))
        rc, out = run_guard(path)
        caught = rc != 0 and "скобк" in out
        print("  %-58s %s" % ("удалена закрывающая скобка", "поймано" if caught else "НЕ ПОЙМАНО"))
        if not caught:
            missed.append("скобки")

print()
print("=== 4. строка записи heredoc должна распознаваться, а её поломка — нет ===")
# deploy.sh writes the config through a `$SUDO` variable rather than a literal
# `sudo`. The guard has to understand that spelling (it used to look for
# `sudo tee` only, so the guard reported "no heredoc" and CI went red), but the
# relaxation must not turn the extraction into "match anything": break the
# write line and the guard has to fail again.
with tempfile.TemporaryDirectory() as td:
    path = os.path.join(td, "deploy-noheredoc.sh")
    broken = re.sub(
        r"^.*tee\s+\"?\$NGINX_CONF\"?\s*>\s*/dev/null\s*<<'\w+'\s*$",
        "cat > /tmp/nowhere <<'EOF'",
        src,
        count=1,
        flags=re.M,
    )
    if broken == src:
        print("  %-58s ПРОПУЩЕНО (трансформация ничего не сделала)" % "сломана строка записи heredoc")
        missed.append("heredoc")
    else:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(broken)
        rc, out = run_guard(path)
        caught = rc != 0 and "heredoc" in out
        print("  %-58s %s" % ("сломана строка записи heredoc", "поймано" if caught else "НЕ ПОЙМАНО"))
        if not caught:
            missed.append("heredoc")

print()
if missed:
    print("ПРОВАЛЕНО: %d кейсов не поймано" % len(missed))
    for m in missed:
        print("  -", m)
    sys.exit(1)

print("гард проверен: все %d поломок ловятся, исправный конфиг проходит" % len(CASES))
