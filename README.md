````markdown
# 🚀 Деплой FastAPI-проекта на WPS хостинг

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)](https://fastapi.tiangolo.com/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-blue)](https://www.postgresql.org/)  
[![Redis](https://img.shields.io/badge/Redis-7%2B-red)](https://redis.io/)  

---

## 📑 Оглавление

1. [Подготовка сервера](#1-подготовка-сервера)  
2. [Настройка PostgreSQL](#2-настройка-postgresql)  
3. [Настройка Redis](#3-настройка-redis)  
4. [Клонирование и установка проекта](#4-клонирование-и-установка-проекта)  
5. [Конфигурация окружения](#5-конфигурация-окружения)  
6. [Миграции базы данных](#6-миграции-базы-данных)  
7. [Создание суперпользователя](#7-создание-суперпользователя)  
8. [Запуск приложения](#8-запуск-приложения)  
9. [Настройка Nginx (опционально)](#9-настройка-nginx-опционально)  
10. [Настройка Supervisor](#10-настройка-supervisor)  
11. [Полезные команды](#11-полезные-команды)  
12. [Важные замечания](#12-важные-замечания)  

---

## 1. Подготовка сервера

### 1.1 Обновление и установка зависимостей

```bash
sudo apt update
sudo apt install -y \
    python3.11 python3.11-venv python3.11-dev \
    postgresql postgresql-contrib \
    redis \
    nginx
````

> **Примечание:** версии Python до 3.13 включительно.

---

## 2. Настройка PostgreSQL

```bash
sudo -u postgres psql -c "CREATE DATABASE yourdb;"
sudo -u postgres psql -c "CREATE USER youruser WITH PASSWORD 'yourpassword';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE yourdb TO youruser;"
```

---

## 3. Настройка Redis

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

---

## 4. Клонирование и установка проекта

```bash
git clone https://github.com/DaniilMurai/CleaningCompanyBackend.git
cd CleaningCompanyBackend

python3.11 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. Конфигурация окружения

Создайте файл `.env` в корне проекта:

```dotenv
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
```

---

## 6. Миграции базы данных

1. Создать ревизию:

   ```bash
   alembic revision --autogenerate -m "initial"
   ```
2. Применить миграции:

   ```bash
   alembic upgrade head
   ```

---

## 7. Создание суперпользователя

```bash
python -m manage createsuperadmin
```

> Следуйте инструкциям в терминале.

---

## 8. Запуск приложения

* Основное API:

  ```bash
  python run.py
  ```
* Фоновый воркер:

  ```bash
  python run_worker.py
  ```

---

## 9. Настройка Nginx (опционально)

Создайте конфиг `/etc/nginx/sites-available/yourdomain.com`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Активируйте и перезапустите:

```bash
sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 10. Настройка Supervisor

```bash
sudo apt install -y supervisor
```

Создайте `/etc/supervisor/conf.d/your_app.conf`:

```ini
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
```

Примените:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

---

## 11. Полезные команды

* Проверить статус Redis:

  ```bash
  redis-cli ping
  ```
* Протестировать подключение к PostgreSQL:

  ```bash
  psql -h localhost -U youruser -d yourdb
  ```
* Просмотр логов:

  ```bash
  journalctl -u supervisor -f      # Supervisor
  tail -f /var/log/api.out.log     # Логи приложения
  ```

---

## 12. Важные замечания

* Для HTTPS используйте сертификаты Let’s Encrypt.
* В продакшене устанавливайте `RELOAD=False`.
* Настройте брандмауэр:

  ```bash
  sudo ufw allow 80
  sudo ufw allow 443
  sudo ufw enable
  ```

---

> **Этот гайд включает:**
>
> * Установку Python ≤ 3.13
> * Использование `pip` (вместо `poetry`)
> * Настройку `.env`
> * Скрипты миграций
> * Запуск через `run.py` и `run_worker.py`
> * Опциональный Nginx и Supervisor
> * Команду для создания суперпользователя

```
```
