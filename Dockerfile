FROM python:3.8.5

WORKDIR /code

COPY backend/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./backend .

RUN python manage.py collectstatic --noinput

CMD gunicorn api.wsgi:application --bind 0.0.0.0:8000
