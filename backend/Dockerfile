FROM python:3.8.5 
 
WORKDIR /code 

COPY . .

RUN pip install --upgrade pip && pip install -r /code/requirements.txt

ADD django_entrypoint.sh /django_entrypoint.sh

RUN chmod a+x /django_entrypoint.sh

ENTRYPOINT ["/django_entrypoint.sh"] 

CMD gunicorn api.wsgi:application --bind 0.0.0.0:8000 