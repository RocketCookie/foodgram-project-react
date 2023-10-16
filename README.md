# Foodgram

**Foodgram** - это приложение для обмена рецептами. Пользователи могут загружать свои рецепты, просматривать рецепты других пользователей.

## Технологический стек

* Python 3.11.6
* Django 4.2.6
* Django REST Framework 3.14.0
* PostgreSQL 15.4
* Docker 24.0.6

## Установка и запуск проекта локально

Чтобы развернуть проект локально необходимо выполнить следующие шаги:

Установить [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

Склонировать репозиторий:

```
git clone git@github.com:RocketCookie/foodgram-project-react.git
```

Создать, в папке infra, файл '.env' на основе '.env.example' и заполнить его валидными данными.

Запустить приложение с помощью команды:

```
make run_app
```

## Миграция и статика

Выполните миграции и сбор статических файлов:

```
make migration_and_static
```

### Автор

Олег Гуров
