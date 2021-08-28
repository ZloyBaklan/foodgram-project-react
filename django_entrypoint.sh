#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Если используем POSGTRES, то дождемся пока он станет доступен
if [ "$POSTGRES_USER" = "postgres" ]; then
    echo "Waiting for PostgreSQL to become available..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL is available"
fi

# Запускаем миграции, загружаем фикстуры, собираем и сжимаем статику
echo "Making migrations."
python manage.py migrate --noinput

echo "Loading demo data from fixtures.json"
python manage.py loaddata -i fixtures.json

echo "Collecting static files."
python manage.py collectstatic --noinput

echo "Compressing static files."
python manage.py compress
