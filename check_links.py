import re
with open('index.html', encoding='utf-8') as f:
    html = f.read()
links = re.findall(r'href=["\']([^"\']+)["\']', html)
print('Found links:', len(links))
for l in links:
    if l.startswith('http'):
        print('External:', l)
    elif l.startswith('#'):
        pass
    else:
        print('Internal:', l)
