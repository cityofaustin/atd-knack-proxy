server {
    listen 80;
    listen 443 ssl;

    location / {
        proxy_pass http://172.18.0.22:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias  /app/static/;
    }

    error_page 502 /502_custom.html;
        location = /custom_502.html {
                root /usr/share/nginx/html;
                internal;
        }

    ssl_certificate /app/cert.pem;
    ssl_certificate_key /app/key.pem;
}
