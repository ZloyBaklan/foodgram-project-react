FROM python:3.8.5 
 
RUN mkdir /code 
 
COPY requirements.txt /code

COPY django_entrypoint.sh /code
 
RUN pip3 install -r /code/requirements.txt 
  
WORKDIR /code 

COPY . .

ENTRYPOINT django_entrypoint.sh

CMD gunicorn api.wsgi:application --bind 0.0.0.0:8000 