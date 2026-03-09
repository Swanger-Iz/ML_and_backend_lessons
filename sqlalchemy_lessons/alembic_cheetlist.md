# 📘 Alembic Cheat Sheet

Полное руководство по миграциям SQLAlchemy для повседневной работы. Закрывает ~90% типовых задач.

---

## 🚀 Быстрый старт

```bash
# 1. Инициализация (один раз)
alembic init src/migrations

# 2. Настройка alembic.ini
# script_location = src/migrations
# prepend_sys_path = src

# 3. Первая миграция
alembic revision --autogenerate -m "initial schema"

# 4. Применить миграцию
alembic upgrade head

# 5. Проверить статус
alembic current
```

---

## 📋 Основные команды

| Команда | Описание |
|---------|----------|
| `alembic init <path>` | Инициализировать новую папку миграций |
| `alembic revision --autogenerate -m "сообщение"` | Создать миграцию автоматически по изменениям в моделях |
| `alembic revision -m "сообщение"` | Создать пустую миграцию вручную |
| `alembic upgrade head` | Применить все неприменённые миграции |
| `alembic upgrade <revision_id>` | Применить миграции до конкретной версии |
| `alembic downgrade -1` | Откатить последнюю миграцию |
| `alembic downgrade <revision_id>` | Откатить до конкретной версии |
| `alembic current` | Показать текущую версию схемы в БД |
| `alembic history` | Показать историю всех миграций |
| `alembic heads` | Показать последние ревизии (head) |
| `alembic branches` | Показать ветви миграций |
| `alembic show <revision_id>` | Показать детали конкретной миграции |
| `alembic stamp <revision_id>` | Пометить БД как уже имеющую эту версию (без применения) |
| `alembic check` | Проверить, есть ли неприменённые изменения в моделях |

---

## 🔧 Настройка проекта

### ✅ alembic.ini

```ini
[alembic]
# Путь к папке миграций
script_location = src/migrations

# ⭐ Добавить src/ в sys.path (решает ModuleNotFoundError)
prepend_sys_path = src

# Шаблон имени файла миграции
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# Время в имени файла (UTC или local)
timezone = UTC

# URL БД (можно переопределить в env.py через settings)
# sqlalchemy.url = postgresql+psycopg://user:pass@localhost:5432/dbname

# Не забыть добавить Base и какой-нибудь созданный Orm для корректной настройки
```

### ✅ src/migrations/env.py

```python
from pathlib import Path
import sys

# 🔧 Добавляем src/ в путь
src_path = Path(__file__).resolve().parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config import settings
from models import Base  # Ваша декларативная база
from alembic import context

config = context.config
target_metadata = Base.metadata

def run_migrations_online():
    # Берём URL из настроек, а не из alembic.ini
    config.set_main_option("sqlalchemy.url", settings.DB_URL)
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,           # Сравнивать типы колонок
            compare_server_default=True, # Сравнивать дефолты
            include_schemas=True,        # Учитывать схемы (PostgreSQL)
        )
        with context.begin_transaction():
            context.run_migrations()
```

---

## 📝 Сценарии работы

### 🆕 Создание новой таблицы

```bash
# 1. Добавили класс в models.py
class NewTable(Base):
    __tablename__ = "new_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

# 2. Создали миграцию
alembic revision --autogenerate -m "add new_table"

# 3. Проверили файл в versions/ (важно!)

# 4. Применили
alembic upgrade head
```

### ✏️ Добавление колонки

```python
# models.py
class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    phone: Mapped[str | None]  # ← Новая колонка (nullable!)
```

```bash
alembic revision --autogenerate -m "add phone to users"
alembic upgrade head
```

> ⚠️ **Важно:** При добавлении колонки в существующую таблицу делайте её `nullable=True` или указывайте `server_default`, иначе миграция упадёт на заполненных таблицах!

### 🔄 Изменение типа колонки

```python
# models.py
class Users(Base):
    salary: Mapped[Decimal]  # Было: Mapped[int]
```

```bash
alembic revision --autogenerate -m "change salary type to decimal"
# ⚠️ Проверьте миграцию! Alembic может не заметить изменение типа
alembic upgrade head
```

### 🗑️ Удаление колонки

```python
# models.py
class Users(Base):
    # old_field: Mapped[str]  # ← Закомментировали или удалили
```

```bash
alembic revision --autogenerate -m "remove old_field from users"
# ⚠️ Проверьте, что в downgrade() есть восстановление колонки!
alembic upgrade head
```

### 🔗 Изменение отношений (ForeignKey, relationship)

```python
# models.py
class Resume(Base):
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    worker: Mapped["Worker"] = relationship(back_populates="resumes")
```

```bash
alembic revision --autogenerate -m "add cascade delete to resumes"
alembic upgrade head
```

---

## 🛠 Ручные миграции (когда autogenerate не справляется)

### Пустая миграция

```bash
alembic revision -m "manual data migration"
```

### Пример: заполнение данных

```python
# versions/xxxxx_manual_data_migration.py
def upgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text("UPDATE users SET role = 'admin' WHERE email LIKE '%@company.com'")
    )

def downgrade():
    conn = op.get_bind()
    conn.execute(
        sa.text("UPDATE users SET role = 'user' WHERE email LIKE '%@company.com'")
    )
```

### Пример: сложное изменение схемы

```python
def upgrade():
    # 1. Добавляем новую колонку
    op.add_column('users', sa.Column('phone_new', sa.String(), nullable=True))
    
    # 2. Копируем данные
    op.execute("UPDATE users SET phone_new = phone")
    
    # 3. Удаляем старую колонку
    op.drop_column('users', 'phone')
    
    # 4. Переименовываем новую
    op.alter_column('users', 'phone_new', new_column_name='phone')

def downgrade():
    # Обратный порядок
    op.alter_column('users', 'phone', new_column_name='phone_old')
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    op.execute("UPDATE users SET phone = phone_old")
    op.drop_column('users', 'phone_old')
```

---

## 🐛 Troubleshooting

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: No module named 'config'` | Добавить `prepend_sys_path = src` в `alembic.ini` или `sys.path.insert()` в `env.py` |
| `Target metadata is empty` | Импортировать все модели в `env.py` до `target_metadata = Base.metadata` |
| Alembic не видит изменения в моделях | Убедиться, что модели импортированы в `env.py` (иногда нужен явный `import models`) |
| Миграция падает на продакшене | Проверить `downgrade()`, протестировать на staging, делать бэкап БД |
| Конфликт миграций (multiple heads) | `alembic merge heads -m "merge conflict"` |
| `Column type mismatch` | Включить `compare_type=True` в `context.configure()` |
| Миграция создалась, но пустая | Проверить, что `Base.metadata` подключена к тем же моделям, которые изменили |

---

## ✅ Best Practices

### 📌 Перед созданием миграции

- [ ] Все модели импортированы в `env.py`
- [ ] `.env` с настройками БД доступен
- [ ] Виртуальное окружение активировано
- [ ] Изменения в `models.py` сохранены

### 📌 После генерации миграции

- [ ] **Проверить сгенерированный файл** (Alembic может ошибаться!)
- [ ] Проверить `upgrade()` и `downgrade()`
- [ ] Протестировать на локальной БД
- [ ] Убедиться, что `downgrade()` работает (откат возможен)

### 📌 Для продакшена

- [ ] Сделать бэкап БД перед `upgrade`
- [ ] Применять миграции в maintenance window
- [ ] Иметь план отката на случай ошибок
- [ ] Не удалять колонки с данными без миграции данных
- [ ] Новые колонки — только `nullable=True` или с `server_default`

### 📌 Именование миграций

```bash
# ✅ Хорошо
alembic revision -m "add_email_index_to_users"
alembic revision -m "create_orders_table"
alembic revision -m "make_phone_nullable_in_users"

# ❌ Плохо
alembic revision -m "fix"
alembic revision -m "update"
alembic revision -m "migration_1"
```

---

## 🔍 Полезные сниппеты для env.py

### Импорт всех моделей

```python
# Чтобы Alembic видел все модели, импортируйте их явно
from models import User, Resume, Worker  # или
import models  # если в __init__.py есть экспорты
```

### Фильтрация таблиц

```python
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    include_object=lambda object, name, type_, reflected, compare_to: (
        name not in ['alembic_version', 'temp_table']  # Игнорировать таблицы
    ),
)
```

### Несколько схем (PostgreSQL)

```python
context.configure(
    connection=connection,
    target_metadata=target_metadata,
    include_schemas=True,
)
```

---

## 📊 Рабочий процесс команды

```bash
# 1. Получили изменения из репозитория
git pull

# 2. Проверили, есть ли новые миграции
alembic current          # Ваша версия
alembic heads            # Последняя версия в репо

# 3. Если версии не совпадают — применили
alembic upgrade head

# 4. Создали свои изменения
# ... редактируем models.py ...
alembic revision --autogenerate -m "my feature"

# 5. Перед коммитом проверили
alembic check            # Есть ли неприменённые изменения
alembic upgrade head     # Применяем локально
alembic downgrade -1     # Проверяем откат
alembic upgrade head     # Снова применяем

# 6. Коммитим миграцию вместе с кодом
git add src/migrations/versions/xxxx_my_feature.py
git commit -m "feat: add my feature + migration"
```

---

## 🎯 Шпаргалка по операциям

| Задача | Команда |
|--------|---------|
| Создать миграцию | `alembic revision --autogenerate -m "msg"` |
| Применить все | `alembic upgrade head` |
| Откатить одну | `alembic downgrade -1` |
| Текущая версия | `alembic current` |
| История | `alembic history --verbose` |
| Проверить изменения | `alembic check` |
| Слить ветви | `alembic merge heads -m "merge"` |
| Пометить версию | `alembic stamp <revision_id>` |

---

## 📚 Дополнительные ресурсы

- [Официальная документация Alembic](https://alembic.sqlalchemy.org/)
- [Batch Operations для SQLite](https://alembic.sqlalchemy.org/en/latest/batch.html)
- [Ops Reference](https://alembic.sqlalchemy.org/en/latest/ops.html)

---

> 💡 **Золотое правило:** Всегда проверяйте сгенерированные миграции перед применением! Alembic — инструмент мощный, но не всемогущий.

**Версия:** 1.0 | **Обновлено:** 2024