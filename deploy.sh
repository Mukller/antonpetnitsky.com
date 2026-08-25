#!/bin/bash
# Deploy antonpetnitsky.com to local server
# Run from: ssh anton@192.168.0.36

set -e

SITE_DIR="/var/www/antonpetnitsky.com"
NGINX_CONF="/etc/nginx/sites-available/antonpetnitsky.com"

# Create web root
sudo mkdir -p "$SITE_DIR"

# Clone or pull latest
if [ -d /tmp/site-deploy ]; then rm -rf /tmp/site-deploy; fi
git clone https://github.com/Mukller/antonpetnitsky.com.git /tmp/site-deploy

# Copy files
for f in index.html cv-ru.html cv-en.html 404.html 50x.html sitemap.xml sitemap-pages.xml robots.txt ap-favicon.svg ap-favicon.png og.png; do
    if [ -f "/tmp/site-deploy/$f" ]; then
        sudo cp "/tmp/site-deploy/$f" "$SITE_DIR/"
    fi
done

# Copy page directories
for d in projects robotics now homelab minecraft uses assets; do
    if [ -d "/tmp/site-deploy/$d" ]; then
        sudo cp -r "/tmp/site-deploy/$d" "$SITE_DIR/"
    fi
done
sudo chown -R www-data:www-data "$SITE_DIR"
sudo chmod -R 755 "$SITE_DIR"

# Write nginx config
sudo tee "$NGINX_CONF" > /dev/null <<'EOF'
# CANONICAL nginx config for antonpetnitsky.com
# Source of truth: deploy.sh in Mukller/antonpetnitsky.com repo.
# Do NOT hand-edit or redeploy stale copies — portfolio (root!), gzip,
# /assets/ cache, sitemap-index and catalog proxy all live here.
server {
    listen 80;
    server_name antonpetnitsky.com www.antonpetnitsky.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name antonpetnitsky.com www.antonpetnitsky.com;

    ssl_certificate /etc/letsencrypt/live/antonpetnitsky.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/antonpetnitsky.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    root /var/www/antonpetnitsky.com;
    index index.html;

    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;

    # compression for text assets (html is compressed by gzip on)
    gzip on;
    gzip_comp_level 5;
    gzip_min_length 256;
    gzip_vary on;
    gzip_types text/css application/javascript application/json image/svg+xml application/xml text/plain;

    # long cache for self-hosted assets (content-addressed)
    location ^~ /assets/ {
        add_header Cache-Control "public, max-age=2592000, immutable";
        try_files $uri =404;
    }

    # ── Research Catalog app (:8200) — do not remove ──
    location ~ ^/(ru|en|uk|be|pl|cs|sk|bg)(/|$) {
        proxy_pass http://127.0.0.1:8200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~ ^/(styles\.css|app\.js|favicon\.svg)$ {
        proxy_pass http://127.0.0.1:8200;
        proxy_set_header Host $host;
        proxy_hide_header cache-control;
        add_header cache-control "public, max-age=3600" always;
    }

    location /og/ { proxy_pass http://127.0.0.1:8200; proxy_set_header Host $host; }
    location /fonts/ {
        proxy_pass http://127.0.0.1:8200;
        proxy_set_header Host $host;
        proxy_hide_header cache-control;
        add_header cache-control "public, max-age=604800" always;
    }

    location = /healthz { proxy_pass http://127.0.0.1:8200; }
    location = /robots.txt { proxy_pass http://127.0.0.1:8200; }
    # app's dynamic sitemap under a new name — /sitemap.xml is our static index
    location = /sitemap-app.xml { proxy_pass http://127.0.0.1:8200/sitemap.xml; }

    location ~ ^/(login|register|logout|dashboard|settings|admin|forgot-password|reset-password|verify-email|favorites)(/|$) {
        proxy_pass http://127.0.0.1:8200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Botka - Telegram Mini App (:8310)
    location /botka/ {
        proxy_pass http://127.0.0.1:8310;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 25m;
    }

    # everything else → portfolio static files
    location / {
        try_files $uri $uri/ =404;
    }
}
EOF

# Enable site
sudo ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/antonpetnitsky.com

# Test and reload
sudo nginx -t && sudo systemctl reload nginx

echo "Deployed successfully!"
