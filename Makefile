run_app:
    docker compose up --build

migration_and_static:
    docker compose exec backend python manage.py migrate
    docker compose exec backend python manage.py collectstatic
    docker compose exec backend cp -r /app/collected_static/. /static/static/.
