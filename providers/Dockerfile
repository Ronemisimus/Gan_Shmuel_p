FROM python:3.5-alpine3.10
RUN apk update 
RUN apk add bash
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add --no-cache mariadb-dev
RUN pip3 install --upgrade pip setuptools && python3 -m pip install flask
RUN python3 -m pip install flask-sqlalchemy flask-migrate mysqlclient
RUN apk del build-deps