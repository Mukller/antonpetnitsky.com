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
for f in index.html cv-ru.html cv-en.html 404.html 50x.html sitemap.xml robots.txt favicon.svg og.png; do
    if [ -f "/tmp/site-deploy/$f" ]; then
        sudo cp "/tmp/site-deploy/$f" "$SITE_DIR/"
    fi
done

# Copy page directories
for d in projects robotics now; do
    if [ -d "/tmp/site-deploy/$d" ]; then
        sudo cp -r "/tmp/site-deploy/$d" "$SITE_DIR/"
    fi
done
sudo chown -R www-data:www-data "$SITE_DIR"
sudo chmod -R 755 "$SITE_DIR"

# Write nginx config
sudo tee "$NGINX_CONF" > /dev/null <<'EOF'
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
