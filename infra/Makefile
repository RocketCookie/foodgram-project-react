run_app:
    docker compose up -d --build

migration_and_static:
    docker compose exec backend python manage.py migrate
    docker compose exec backend python manage.py collectstatic
    docker compose exec backend python manage.py import_json
