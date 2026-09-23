#!/usr/bin/env python3
# Улучшенный проверщик ссылок — проверяет index.html и все подстраницы
# Используется для аудита перед запуском

import os
import re
import sys

pages = [
    'index.html',
    'about/index.html',
    'projects/index.html',
    'robotics/index.html',
    'homelab/index.html',
    'print3d/index.html',
    'privacy-policy.html',
    'terms.html',
]

failed = 0
for p in pages:
    path = p
    if not os.path.exists(path):
        print('FAIL missing page:', p)
        failed += 1
        continue
    with open(path, encoding='utf-8') as f:
        html = f.read()
    links = re.findall(r'href=["\']([^"\']+)["\']', html)
    for l in links:
        if l.startswith('#'):
            pass  # anchor links — skip
        elif l.startswith('http'):
            pass  # external links — we don't verify them live
        else:
            # Internal link
            target = l
            # Remove leading /
            if target.startswith('/'):
                target_path = target[1:]  # relative to root
            else:
                target_path = os.path.join(os.path.dirname(p) if '/' in p else '.', target)
            # Check if file exists
            if target_path.endswith('/'):
                target_path += 'index.html'
            if not os.path.exists(target_path):
                print('FAIL broken link in', p, ':', l, '-> file not found:', target_path)
                failed += 1
    print('OK page:', p, '| links checked:', len(links))

if failed:
    print(failed, 'failures')
    sys.exit(1)
else:
    print('All pages checked — 0 broken internal links.')
