FROM python:3.8.5

WORKDIR /code

COPY backend/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./backend .

RUN chmod a+x django_entrypoint.sh
ENTRYPOINT django_entrypoint.sh

# RUN chmod +x django_entrypoint.sh
# CHECK
# RUN python manage.py collectstatic --noinput
# ENTRYPOINT django_entrypoint.sh

CMD gunicorn api.wsgi:application --bind 0.0.0.0:8000
