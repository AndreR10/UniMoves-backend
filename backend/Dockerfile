FROM python:3.8-slim-buster

ENV PYTHONBUFFERED=1
RUN mkdir /django
WORKDIR /django
ADD . /django
COPY ./requirements.txt /django/requirements.txt
RUN pip3 install -r requirements.txt

# COPY . .
# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]   ESTES HAO DE IR PARA O Docker Compose
