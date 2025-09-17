# E-commerce Backend (Django + DRF + PostgreSQL)

Production-ready API with JWT auth, filtering/sorting/search, pagination, OpenAPI docs, CI, and Docker.

## Features
- **Auth**: JWT (access/refresh)
- **Products & Categories**: CRUD, filtering, ordering, search, pagination
- **Docs**: OpenAPI/Swagger at `/api/docs/`
- **Performance**: `select_related`/`prefetch_related`, DB indexes
- **Security**: CORS, HTTPS settings, throttling
- **CI**: GitHub Actions runs tests on push/PR

## Run locally
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit as needed
python backend/manage.py migrate
python backend/manage.py runserver 0.0.0.0:8000
```

## Run with Docker
```bash
cp .env.example .env
docker compose up --build
```
Services:
- App: http://localhost:8000
- Docs: http://localhost:8000/api/docs/

## Tests
```bash
source .venv/bin/activate
pytest -q
```

## API examples
JWT obtain/refresh:
```bash
curl -X POST http://localhost:8000/api/auth/jwt/create/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"demo","password":"pass12345"}'

curl -X POST http://localhost:8000/api/auth/jwt/refresh/ \
  -H 'Content-Type: application/json' \
  -d '{"refresh":"<refresh_token>"}'
```

Products:
```bash
# list
curl http://localhost:8000/api/products/?ordering=-created_at&page=1
# create (requires auth)
curl -X POST http://localhost:8000/api/products/ \
  -H 'Authorization: Bearer <access_token>' -H 'Content-Type: application/json' \
  -d '{"category_id":1,"name":"Phone","slug":"phone","price_cents":9999,"currency":"USD","is_active":true,"stock":10}'
```

## Deployment
### Heroku
1. Set env vars: `SECRET_KEY`, `DEBUG=False`, `DATABASE_URL`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`
2. Procfile is provided:
```procfile
release: python backend/manage.py migrate --noinput
web: gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-3}
```
3. Push to Heroku; migrations run on release phase.

### Render/Railway
- Use Docker deploy or native Python environment. Set env vars as above.
- Health check: `/api/docs/` or `/admin/login/`

## Production settings
- Set:
  - `DJANGO_DEBUG=False`
  - `DJANGO_ALLOWED_HOSTS=yourdomain.com`
  - `DJANGO_SECURE_SSL_REDIRECT=True`
  - `DJANGO_SESSION_COOKIE_SECURE=True`, `DJANGO_CSRF_COOKIE_SECURE=True`
  - `DJANGO_SECURE_HSTS_SECONDS=31536000`, `DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=True`, `DJANGO_SECURE_HSTS_PRELOAD=True`
  - `CSRF_TRUSTED_ORIGINS=https://yourdomain.com`
  - `CORS_ALLOWED_ORIGINS=https://yourfrontend.com`
- DRF throttling via env: `DRF_THROTTLE_USER`, `DRF_THROTTLE_ANON`

## Performance
- Query optimization: viewsets use `select_related`/`prefetch_related`
- DB indexes on `Category.slug`, `Category.name`, `Product.name`, `Product.slug`, `Product.is_active`+`category`, `Product.price_cents`
- For deeper analysis, enable `pg_stat_statements` in Postgres:
  - Add to `postgresql.conf`: `shared_preload_libraries = 'pg_stat_statements'`
  - Restart DB, then `CREATE EXTENSION pg_stat_statements;`
  - Query with: `SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 20;`

