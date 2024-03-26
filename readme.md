
## Booking hotels
***
> Booking Hotels - это API, разработанное на базе FastAPI, предназначенное для бронирования номеров в отелях на выбранный срок.

#### Установка / Начало работы

1. Склонируйте репозиторий с проектом "Booking Hotels".

2. Перейдите в каталог проекта.

3. Создайте файл `.env-non-dev` с необходимыми переменными окружения, используя образец `.env.example`.

#### Запуск приложения
Для запуска FastAPI используется веб-сервер uvicorn.

```bash
uvicorn app.main:app --reload
```
#### Celery & Flower

##### Для запуска Celery используется команда:
```bash
celery --app=app.tasks.celery_conf:celery_app worker -l INFO
```

##### Для запуска Flower используется команда:
```bash
celery --app=app.tasks.celery_conf:celery_app flower
```
##### Для запуска Celery-beat используется команда:
```bash
celery --app=app.tasks.celery_conf:celery_app worker -l INFO -B
```

#### Docker compose

Перед запуском проекта "Booking Hotels" с помощью Docker Compose, вам возможно потребуется внести изменения в файлах (`docker-compose.yml`, `nginx.conf`).

Для запуска проекта "Booking Hotels" с использованием Docker Compose выполните следующие шаги:

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Склонируйте репозиторий с проектом "Booking Hotels".

3. Перейдите в каталог проекта.

4. Создайте файл `.env-non-dev` с необходимыми переменными окружения, используя образец `.env.example`.

5. Запустите контейнеры с помощью команд:

```bash
docker compose build
docker compose up
```
#### Функциональные возможности

Проект "Booking Hotels" предоставляет следующие ключевые функции:

- Поиск доступных номеров в отелях на выбранный срок.
- Бронирование выбранного номера в отеле.
- Напоминание о дате заезда в номер, за 3 дня до заезда и за 1 день до заезда 
- Управление бронированиями, включая просмотр, изменение и отмену бронирований.
