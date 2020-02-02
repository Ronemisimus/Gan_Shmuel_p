FROM python:3.5-alpine3.10
RUN mkdir app
COPY requirements.txt /app
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app

ENTRYPOINT flask run --host=0.0.0.0

