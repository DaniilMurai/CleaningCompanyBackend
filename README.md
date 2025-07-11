# 🚀 Деплой FastAPI проекта на WPS хостинг

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue)
![Redis](https://img.shields.io/badge/Redis-7%2B-red)

## 1. Подготовка сервера

### Установка Python и зависимостей
```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev  # До 3.13 включительно
sudo apt install -y postgresql postgresql-contrib redis
sudo apt install -y nginx  # Если нужно проксировать запросы


2. Настройка базы данных PostgreSQL

sudo -u postgres psql -c "CREATE DATABASE yourdb;"
sudo -u postgres psql -c "CREATE USER youruser WITH PASSWORD 'yourpassword';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE yourdb TO youruser;"


3. Настройка Redis

sudo systemctl enable redis-server
sudo systemctl start redis-server


4. Клонирование и настройка проекта


git clone https://github.com/DaniilMurai/CleaningCompanyBackend
cd <папка-проекта>
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

5. Создание файла .env
Создайте .env файл в корне проекта:

DATABASE_URL=postgresql+asyncpg://youruser:yourpassword@localhost:5432/yourdb
SECRET_KEY=your-secret-key-here
FRONTEND_URL=https://your-frontend.com
HOST=0.0.0.0
RELOAD=False
REDIS_HOST=localhost
REDIS_PORT=6379
DEFAULT_LANG=en
LOGS_DIR=logs
LOCALES_PATH=locales

6. Миграции базы данных
Создание миграций:

alembic revision --autogenerate -m "initial"

Применение миграций:

alembic upgrade head


7. Создание суперпользователя

python -m manage createsuperadmin
(следуйте инструкциям в терминале)

8. Запуск приложения
Основное приложение (FastAPI):

python run.py

Worker:

python run_worker.py


9. Настройка Nginx (опционально)
Создайте файл /etc/nginx/sites-available/yourdomain.com:

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

Активируйте конфиг:

sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

10. Настройка Supervisor (для управления процессами)
Установите Supervisor:

sudo apt install -y supervisor

Создайте конфиг /etc/supervisor/conf.d/your_app.conf:


[program:api]
command=/path/to/venv/bin/python run.py
directory=/path/to/your/project
autostart=true
autorestart=true
stderr_logfile=/var/log/api.err.log
stdout_logfile=/var/log/api.out.log

[program:worker]
command=/path/to/venv/bin/python run_worker.py
directory=/path/to/your/project
autostart=true
autorestart=true
stderr_logfile=/var/log/worker.err.log
stdout_logfile=/var/log/worker.out.log

Примените настройки:

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all


Полезные команды
Проверить статус Redis: redis-cli ping

Проверить подключение к PostgreSQL: psql -h localhost -U youruser -d yourdb

Просмотр логов:

journalctl -u supervisor -f  # Для supervisor
tail -f /var/log/api.out.log  # Для логов приложения


Важные замечания

Для HTTPS добавьте сертификат Let's Encrypt
Для продакшена установите RELOAD=False

Настройте брандмауэр (если нужно):

sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable


Этот гайд включает:
- Установку Python до 3.13
- Использование pip вместо poetry
- Создание .env с вашими настройками
- Скрипты для миграций
- Запуск через run.py и run_worker.py
- Опциональные настройки Nginx и Supervisor
- Команду для создания суперпользователя

