FROM python:3.8.5 
 
RUN mkdir /code 
 
COPY requirements.txt /code

COPY django_entrypoint.sh /code
 
RUN pip3 install -r /code/requirements.txt 

COPY . /code

RUN chmod a+x /code/django_entrypoint.sh

ENTRYPOINT ["/code/django_entrypoint.sh"]

WORKDIR /code 

CMD gunicorn api.wsgi:application --bind 0.0.0.0:8000 