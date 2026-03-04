## 📋 Как создать файл:

1. **Скопируй** весь текст ниже (от `# PostgreSQL + SQLAlchemy Шпаргалка` до конца)
2. **Создай файл** в своём проекте:
   ```bash
   nano psql_sqlalchemy.md
   ```
3. **Вставь** содержимое (`Ctrl+Shift+V` в терминале или `Ctrl+V` в nano)
4. **Сохрани**: `Ctrl+O` → `Enter` → `Ctrl+X`

---

Вот полное содержимое для файла **psql_sqlalchemy.md**:

```markdown
# PostgreSQL + SQLAlchemy Шпаргалка

## 🔹 1. Управление сервисом PostgreSQL

### Через `service` (универсально)
| Команда | Описание |
|---------|----------|
| `sudo service postgresql start` | Запустить сервер |
| `sudo service postgresql stop` | Остановить сервер |
| `sudo service postgresql restart` | Перезапустить сервер |
| `sudo service postgresql status` | Проверить статус |
| `sudo service postgresql reload` | Перезагрузить конфиги без перезапуска |

### Через `pg_ctlcluster` (Debian/Ubuntu, надёжнее)
| Команда | Описание |
|---------|----------|
| `sudo pg_ctlcluster 17 main start` | Запустить кластер 17-main |
| `sudo pg_ctlcluster 17 main stop` | Остановить кластер |
| `sudo pg_ctlcluster 17 main restart` | Перезапустить кластер |
| `sudo pg_ctlcluster 17 main status` | Статус кластера |
| `sudo pg_ctlcluster 17 main reload` | Перезагрузить конфиги |

> 💡 **Проверь свою версию:** `ls /etc/postgresql/` (там будет номер версии, например `17`)

---

## 🔹 2. Подключение к базе данных

| Команда | Описание |
|---------|----------|
| `psql -U postgres` | Вход без пароля (через сокет) |
| `psql -h localhost -U postgres -d sa -W` | Вход по TCP с паролем |
| `psql -h localhost -U postgres -d sa` | Вход по TCP без пароля (если `trust`) |
| `sudo -u postgres psql` | Вход от имени пользователя postgres |

### Внутри `psql`:
| Команда | Описание |
|---------|----------|
| `\l` | Список всех баз данных |
| `\c sa` | Подключиться к базе `sa` |
| `\dt` | Список таблиц |
| `\d таблица` | Описание таблицы |
| `\du` | Список пользователей |
| `\q` | Выйти из psql |
| `\h` | Справка по SQL-командам |
| `\?` | Справка по командам psql |

---

## 🔹 3. Управление базами и пользователями

### Создание БД и пользователей
```sql
-- Создать базу данных
CREATE DATABASE sa;

-- Создать пользователя с паролем
CREATE USER myuser WITH PASSWORD 'mypassword';

-- Дать права на базу
GRANT ALL PRIVILEGES ON DATABASE sa TO myuser;

-- Удалить базу
DROP DATABASE sa;

-- Удалить пользователя
DROP USER myuser;
```

### Проверка прав
```sql
-- Показать права пользователя
\du

-- Показать права на таблицу
\dp таблица
```

---

## 🔹 4. Конфигурационные файлы (Debian 17)

| Файл | Путь | Назначение |
|------|------|------------|
| Основной конфиг | `/etc/postgresql/17/main/postgresql.conf` | Настройки сервера (порт, listen_addresses) |
| Аутентификация | `/etc/postgresql/17/main/pg_hba.conf` | Кто и как может подключаться |
| Данные | `/var/lib/postgresql/17/main/` | Файлы баз данных |
| Логи | `/var/log/postgresql/postgresql-17-main.log` | Лог сервера |

### Важные параметры в `postgresql.conf`:
```conf
listen_addresses = 'localhost'  # или '*' для всех интерфейсов
port = 5432
max_connections = 100
```

### Важные строки в `pg_hba.conf`:
```conf
# TYPE  DATABASE  USER  ADDRESS         METHOD
local   all       all                   trust      # Unix-сокет без пароля
host    all       all   127.0.0.1/32    trust      # TCP localhost без пароля
host    all       all   127.0.0.1/32    md5        # TCP localhost с паролем
```

> ⚠️ **Важно:** Строка `local ... 127.0.0.1/32` — **невалидна**! `local` не поддерживает IP-адреса.

---

## 🔹 5. Диагностика и логи

| Команда | Описание |
|---------|----------|
| `ss -tlnp | grep 5432` | Проверить, слушает ли порт 5432 |
| `sudo tail -n 50 /var/log/postgresql/postgresql-17-main.log` | Последние 50 строк лога |
| `sudo journalctl -xeu postgresql@17-main.service` | Логи systemd |
| `ps aux | grep postgres` | Показать процессы PostgreSQL |
| `sudo pg_ctlcluster 17 main status` | Детальный статус кластера |

---

## 🔹 6. SQLAlchemy: Подключение и сессии

### Синхронный движок
```python
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg://postgres@localhost:5432/sa"
# С паролем: postgresql+psycopg://postgres:1234@localhost:5432/sa

engine = create_engine(DATABASE_URL, echo=True, pool_size=5, max_overflow=10)

with engine.connect() as conn:
    result = conn.execute(text("SELECT VERSION()"))
    print(result.scalar())
```

### Асинхронный движок
```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres@localhost:5432/sa"

engine = create_async_engine(DATABASE_URL, echo=True)
session_maker = async_sessionmaker(engine, expire_on_commit=False)

async with session_maker() as session:
    result = await session.execute(text("SELECT VERSION()"))
    print(result.scalar())
```

### URL форматы
| Формат | Описание |
|--------|----------|
| `postgresql+psycopg://user@host/db` | Без пароля (trust) |
| `postgresql+psycopg://user:pass@host/db` | С паролем |
| `postgresql+asyncpg://user@host/db` | Асинхронный драйвер asyncpg |
| `postgresql+psycopg2://user@host/db` | Старый драйвер psycopg2 |

---

## 🔹 7. Частые проблемы и решения

| Проблема | Решение |
|----------|---------|
| `Connection refused` | Сервер не запущен: `sudo service postgresql start` |
| `Authentication failed` | Проверь `pg_hba.conf` и пароль |
| `Database does not exist` | Создай базу: `CREATE DATABASE sa;` |
| `Port 5432 already in use` | Найди процесс: `ss -tlnp | grep 5432`, убей или смени порт |
| `Permission denied` | Исправь права: `sudo chown -R postgres:postgres /var/lib/postgresql/17/main` |
| `Invalid authentication method` | Замени `scram-sha-256` на `trust` или `md5` в `pg_hba.conf` |
| `local ... 127.0.0.1/32` ошибка | Удали эту строку — `local` не поддерживает IP |

---

## 🔹 8. Полезные SQL-запросы

```sql
-- Версия PostgreSQL
SELECT VERSION();

-- Список всех баз
SELECT datname FROM pg_database;

-- Список всех таблиц в текущей БД
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Размер базы данных
SELECT pg_size_pretty(pg_database_size('sa'));

-- Количество подключений
SELECT count(*) FROM pg_stat_activity;

-- Убить все подключения к базе (для DROP DATABASE)
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'sa';
```

---

## 🔹 9. Алиасы для терминала (~/.bashrc)

Добавь в конец `~/.bashrc` для удобства:

```bash
# PostgreSQL алиасы
alias pgstart='sudo pg_ctlcluster 17 main start'
alias pgstop='sudo pg_ctlcluster 17 main stop'
alias pgrestart='sudo pg_ctlcluster 17 main restart'
alias pgstatus='sudo pg_ctlcluster 17 main status'
alias pglog='sudo tail -n 50 /var/log/postgresql/postgresql-17-main.log'
alias pgconf='sudo nano /etc/postgresql/17/main/postgresql.conf'
alias pghba='sudo nano /etc/postgresql/17/main/pg_hba.conf'
```

Примени изменения:
```bash
source ~/.bashrc
```

Теперь можно писать `pgstart` вместо полной команды! 🚀

---

## 🔹 10. Безопасность (для продакшена)

```conf
# pg_hba.conf - безопасные настройки
local   all   postgres   peer
local   all   all        scram-sha-256
host    all   all        127.0.0.1/32   scram-sha-256
host    all   all        ::1/128        scram-sha-256
```

```python
# Никогда не храни пароли в коде!
# Используй переменные окружения:
import os
from sqlalchemy import create_engine

DATABASE_URL = f"postgresql+psycopg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost/{os.getenv('DB_NAME')}"
engine = create_engine(DATABASE_URL)
```

---

## 📌 Быстрый чек-лист при старте работы

```bash
# 1. Запустить PostgreSQL
pgstart

# 2. Проверить, что порт слушается
ss -tlnp | grep 5432

# 3. Подключиться и проверить
psql -h localhost -U postgres -d sa

# 4. Запустить Python-скрипт
python src/database.py
```

---