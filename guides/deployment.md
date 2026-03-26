# Deployment

## Render

Render'da `static` fayllar `WhiteNoise` orqali servis qilinadi. `media` fayllar esa persistent disk bo'lmasa saqlanib qolmaydi. Shu sabab `render.yaml` ichida disk mount qilingan va `MEDIA_ROOT=/var/data/media` ishlatiladi.

Minimal env:

- `DEBUG=False`
- `SECRET_KEY=<secret>`
- `ALLOWED_HOSTS=.onrender.com,<your-domain>`
- `CORS_ALLOWED_ORIGINS=https://your-frontend-domain`
- `CSRF_TRUSTED_ORIGINS=https://your-frontend-domain`
- `MEDIA_ROOT=/var/data/media`

Build command:

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Start command:

```bash
gunicorn config.wsgi:application
```

## Nginx

Agar VPS ishlatsangiz, `gunicorn` oldiga `nginx` qo'yiladi. Misol konfiguratsiya:

```nginx
server {
    listen 80;
    server_name api.example.com;

    client_max_body_size 50M;

    location /static/ {
        alias /srv/visit-backend/staticfiles/;
    }

    location /media/ {
        alias /srv/visit-backend/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Muhim

Render'da user yuklagan rasmni doimiy saqlash uchun persistent disk yoki S3 kabi object storage kerak. Faqat `MEDIA_ROOT=media/` qilib qo'yish yetmaydi.
