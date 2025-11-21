# Справочник организаций - REST API

REST API приложение для управления справочником организаций, зданий и видов деятельности.

## Технологический стек

- **FastAPI** - современный, быстрый веб-фреймворк для построения API
- **Pydantic** - валидация данных и сериализация
- **SQLAlchemy** - ORM для работы с базой данных
- **Alembic** - система миграций базы данных
- **PostgreSQL** - база данных (можно заменить на другую через настройки)
- **Docker** - контейнеризация приложения

## Функциональность

### Организации

- Поиск организаций по названию
- Фильтрация организаций по зданию
- Фильтрация организаций по виду деятельности `рекурсивно`
- Поиск организаций в географической области

### Здания

- Географический поиск организаций (в радиусе)
- Координаты в формате широты/долготы

### Деятельности

- Древовидная структура видов деятельности
- Ограничение вложенности до 3 уровней
- Поиск организаций по дереву деятельностей

## Диограма БД
![alt text](DB_diogram.png)

## Установка и запуск

### Предварительные требования

- Docker
- docker compose

### Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone git@github.com:Sovraska/Tesovoe_dictionary_for_organistaions.git
cd Tesovoe_dictionary_for_organistaions
```


2. Создайте файл .env:

```dotenv
DB_USERNAME=test_username
DB_NAME=test_db_name
DB_PASSWORD=test_password
DB_HOST=test_app_postgres
DB_PORT=5432
API_KEY=test
```
3. Собирите образ:

```bash
docker compose build .
```

4 Запустите его:
```bash
docker compsoe up -d
```

# Локальная разработка без Docker
Убедитесь, что PostgreSQL запущен и доступен

1. Создайте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```
2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения в .env файле

4. Выполните миграции:

```bash
alembic upgrade head
```
5. Запустите сервер разработки:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
1. Приложение будет доступно по адресу: http://localhost:8000

2. Документация API:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    - Offline: `openapi.yaml`
