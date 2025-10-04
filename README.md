cp template.env .env


docker compose up -d --build

# Скопируйте шаблон и создайте `.env` файл:

```bash
cp template.env .env
```

# В файле .env укажите переменные окружения по примеру:

```env
DEBUG=true
DATABASE_NAME=secretmanager
DATABASE_USER=demo
DATABASE_PASSWORD=demo
DATABASE_HOST=postgres
DATABASE_PORT=5432
OPENBAO_URL=http://openbao:8200
BAO_TOKEN_FILE=/path/to/token/file
EMAIL_SENDER=example@example.com
EMAIL_PASSWORD=secret
```

# почту и пароль узнать у нас

## Запуск проекта

```bash
docker compose up -d --build
```
