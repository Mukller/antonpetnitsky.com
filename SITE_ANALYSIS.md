# Анализ рекомендаций по сайту antonpetnitsky.com
Итоговый список из 3 источников (скриншоты): запуск, безопасность, предзапусковые задачи.

## Источник 1: «20 things to tell Claude to add before launching»
1. Custom 404 page — ЕСТЬ (404.html)
2. CTA above the fold — ЕСТЬ (hero с кнопками)
3. Internal links — ЕСТЬ (в проектных карточках, CV)
4. Thank you page — НЕТ
5. Breadcrumbs — НЕТ
6. Case studies — НЕТ (нужен раздел с кейсами проектов)
7. 5 FAQs — НЕТ (нужен FAQ блок)
8. Response time promise — НЕТ (нужна гарантия ответа для контактов)
9. Sticky mobile CTA — НЕТ (нет sticky кнопки на мобильном)
10. robots.txt — ЕСТЬ
11. Unique page titles — ЕСТЬ (title в index.html)
12. Meta descriptions — ЕСТЬ (meta description в head)
13. Social share img — ЕСТЬ (og.png, meta tags)
14. Maps + directions — НЕТ (нет карты/адреса в контактах)
15. Real reviews — НЕТ (нет блока отзывов)
16. Alt text on images — ЧАСТИЧНО (нужна проверка)
17. Local schema — НЕТ (нет structured data для локального бизнеса)
18. PP page (Privacy Policy) — НЕТ
19. Google analytics — НЕТ
20. Team photo — НЕТ

## Источник 2: «20 essential website security checks»
1. Hide API keys — ПРИМЕНИМО (проверить .env, deploy.sh, код)
2. Check env variables — ПРИМЕНИМО
3. Check keys in Git — ПРИМЕНИМО (проверить историю коммитов)
4. Protect admin routes — НЕ ПРИМЕНИМО (нет админ-панели на портфолио)
5. Add auth — НЕ ПРИМЕНИМО
6. Check user perms — НЕ ПРИМЕНИМО
7. Sanitize user inputs — НЕ ПРИМЕНИМО (нет форм ввода)
8. Protect against XSS — ПРИМЕНИМО (проверить вывод данных)
9. SQL injection protection — НЕ ПРИМЕНИМО (нет БД на фронте)
10. Check DB rules — НЕ ПРИМЕНИМО
11. Add rate limiting — НЕ ПРИМЕНИМО (nginx базовый)
12. Set spend cap — НЕ ПРИМЕНИМО
13. Secure file uploads — НЕ ПРИМЕНИМО
14. CSRF protection — НЕ ПРИМЕНИМО
15. Check CORS settings — ПРИМЕНИМО (проверить nginx CORS)
16. Enable HTTPS — ЕСТЬ (nginx перенаправляет на HTTPS)
17. Add security headers — НЕТ (нужны security headers в nginx)
18. Secure cookies — НЕ ПРИМЕНИМО (нет cookies)
19. Disable debug mode — ПРИМЕНИМО (проверить, что нет debug-режима)
20. Check prod settings — ПРИМЕНИМО

## Источник 3: «20 things to have Claude do before launching»
1. Privacy policy page — НЕТ (из Источника 1)
2. Terms & conditions page — НЕТ
3. Secrets off the frontend — ПРИМЕНИМО (проверить index.html на вшитые ключи)
4. Force HTTPS — ЕСТЬ (nginx redirect 301)
5. Cookie consent banner — НЕТ
6. Meta titles + descriptions — ЕСТЬ (частично)
7. Social preview image — ЕСТЬ (og.png)
8. Add a favicon — ЕСТЬ (ap-favicon.svg/png)
9. Sitemap + robots.txt — ЕСТЬ
10. Alt text on images — ЧАСТИЧНО (проверить картинки в робототехнике)
11. Compress your images — ПРИМЕНИМО (og.png 101KB — можно сжать)
12. Check page load speed — ПРИМЕНИМО
13. Fix color contrast — ПРИМЕНИМО (проверить CSS)
14. Make it mobile friendly — ПРИМЕНИМО (проверить responsive)
15. Custom 404 page — ЕСТЬ
16. Fix broken links — ПРИМЕНИМО (проверить check.js)
17. Form validation — НЕ ПРИМЕНИМО (нет форм)
18. Spam protection — НЕ ПРИМЕНИМО
19. Set up analytics — НЕТ (нет Google Analytics или альтернативы)
20. One clear call to action — ЕСТЬ (hero кнопки)

## Итоговая сводка

### Уже есть (не нужно делать):
- Custom 404, robots.txt, sitemap, favicon, HTTPS redirect, title/meta, social image, CTA
- Services section, project cards, CV pages

### Нужно сделать (по приоритету):
**Критично (безопасность и базовая готовность):**
- Проверить secrets в index/deploy
- Добавить security headers в nginx
- Проверить alt text на изображениях
- Сжать og.png
- Проверить broken links
- Добавить Privacy Policy + Terms
- Добавить Google Analytics или альтернативу
- Проверить mobile responsive и load speed

**Желательно (улучшение конверсии):**
- FAQ блок (5 пунктов)
- Breadcrumbs в навигации
- Case studies секция
- Real reviews / testimonials
- Maps + directions (если есть физический адрес)
- Team photo
- Local schema (structured data)
- Cookie consent banner
- Response time promise
- Sticky mobile CTA
