# Foodgram

**Foodgram** - это приложение для обмена рецептами. Пользователи могут загружать свои рецепты, просматривать рецепты других пользователей.

## Технологический стек

* Python 3.11.4
* Django 4.2.3
* Django REST Framework 3.14.0
* PostgreSQL 13.1
* Docker 24.0.2

## Установка и запуск проекта локально

Чтобы развернуть проект локально необходимо выполнить следующие шаги:

Установить [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/).

Склонировать репозиторий:

```
git clone git@github.com:RocketCookie/foodgram-project-react.git
```

Создать файл '.env' на основе '.env.example' и заполнить его валидными данными.

Запустить приложение с помощью команды: `make run_app`.

## Миграция и статика

Выполните миграции и сбор статических файлов

`make migration_and_static`

### Автор

Олег Гуров
