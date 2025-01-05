# "Mini shop" tg web app fastapi backend

This backend for "Mini shop" tg web app

*Pay methods*:

* [Yookassa](https://yookassa.ru/)
* [CryptoBot](https://t.me/send) 

### Techonoligies

* [FastAPI](https://fastapi.tiangolo.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [Aiogram](https://aiogram.dev/)
* [Telegram Web App](https://core.telegram.org/bots/api)
* [Postgres](https://www.postgresql.org/)
* [Redis](https://redis.io/)
* [OAuth](https://en.wikipedia.org/wiki/OAuth)

### Settings

* `.env` - environment variables

Example:
```env
# TG
TG_BOT_TOKEN=123:ABCDEFGHIJKLMNOPQRSTUVWXYZ  # Get from https://t.me/BotFather
TG_BOT_USERNAME=test_bot  # Optional (autosetting)

# General
SECRET_KEY=12345678qwerty
DEBUG=False  # Optional

# Yokassa pay (optional)
YOOKASSA_SHOP_ID=123456
YOOKASSA_SECRET_KEY=abc_defghijklmnopqrstuvwxyz
# or
YOOKASSA_OAUTH_TOKEN=123_ABCDEFGHIJKLMNOPQRSTUVWXYZ

# CryptoBot pay (optional)
CRYPTO_BOT_TOKEN=123:ABCDEFGHIJKLMNOPQRSTUVWXYZ

# Database
DB_NAME=postgres
DB_PORT=5432
DB_HOST=localhost
DB_PASSWORD=qwerty
DB_USER=postgres
# or
DB_URL=postgres+asyncpg://postgres:qwerty@localhost:5432/postgres
```

* `config.toml` - configuration file

All variables from this file is optional

Example:
```.toml
[dir]
base='./'
uploads='./uploads'

[redis]
host='localhost'
port=6379
db=0

[fastapi]
host='0.0.0.0'
port=8000
reload=false
origins=["*"]

[project]
backend_url='http://localhost:8000'
frontend_url='http://localhost:3000'
payment_time_life=60

[file]
max_size=16777216  # 16MB
allowed_extensions=["jpg", "jpeg", "png", "mp4"]

[auth]
algorithm='HS256'
access_token_expire_minutes=1440
max_token_size=8192

[logging]
level='WARNING'
format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s'
datefmt='%m.%d.%Y %H:%M:%S'
```

### Run project

* Using docker: 
```bash
docker-compose up -d --build
```

### TODO

- [ ] Create docker files
- [ ] Create order routes
- [ ] Create tests
- [ ] Create bot routes and handlers 
- [ ] Add notifications

### Project hierarchy

```txt
mini_shop_web_app_backend/src
├─ __init__.py
├─ api
│  ├─ __init__.py
│  └─ v1
│     ├─ __init__.py
│     ├─ admin.py
│     ├─ category.py
│     ├─ dependencies.py
│     ├─ media.py
│     ├─ order.py
│     ├─ payment.py
│     ├─ product.py
│     └─ user.py
├─ common
│  ├─ __init__.py
│  └─ scheduler.py
├─ core
│  ├─ __init__.py
│  └─ config
│     ├─ __init__.py
│     ├─ base.py
│     ├─ common_config.py
│     ├─ payment_config.py
│     └─ settings.py
├─ db
│  ├─ __init__.py
│  ├─ base.py
│  ├─ migrations
│  │  ├─ README
│  │  ├─ env.py
│  │  ├─ script.py.mako
│  │  └─ versions
│  │     └─ ...
│  ├─ models
│  │  ├─ __init__.py
│  │  ├─ admin.py
│  │  ├─ media.py
│  │  ├─ order.py
│  │  ├─ product.py
│  │  └─ user.py
│  ├─ repositories
│  │  ├─ __init__.py
│  │  ├─ admin.py
│  │  ├─ base
│  │  │  ├─ __init__.py
│  │  │  ├─ abstract.py
│  │  │  └─ sqlalchemy.py
│  │  ├─ media.py
│  │  ├─ order.py
│  │  ├─ product.py
│  │  └─ user.py
│  └─ unitofwork.py
├─ enums
│  ├─ __init__.py
│  ├─ media.py
│  └─ order.py
├─ exceptions
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ base.py
│  ├─ category.py
│  ├─ common.py
│  ├─ media.py
│  ├─ payment.py
│  └─ product.py
├─ main.py
├─ modules
│  ├─ __init__.py
│  └─ payment
│     ├─ __init__.py
│     ├─ base.py
│     ├─ crypto_bot.py
│     └─ yookassa.py
├─ schemas
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ category.py
│  ├─ common.py
│  ├─ media.py
│  ├─ order.py
│  ├─ payment.py
│  ├─ product.py
│  └─ user.py
├─ services
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ base.py
│  ├─ category.py
│  ├─ media.py
│  ├─ payment.py
│  ├─ product.py
│  └─ user.py
└─ utils
   ├─ __init__.py
   ├─ other.py
   └─ validate.py

```
