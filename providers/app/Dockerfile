FROM python:3.6-alpine3.10
RUN apk update 
RUN apk add bash
RUN apk add --virtual build-deps gcc python3-dev musl-dev
RUN apk add --no-cache mariadb-dev
RUN pip3 install --upgrade pip setuptools && python3 -m pip install flask
RUN python3 -m pip install flask-sqlalchemy flask-migrate mysqlclient requests
RUN apk del build-deps
WORKDIR /flask-app
COPY  ./flask-app /flask-app
ENV FLASK_APP=/flask-app/app.py
RUN chmod +x startup.sh
EXPOSE "${APP_EXPOSE}"
ENTRYPOINT [ "/bin/bash", "startup.sh" ]

# add ENV for port and stuff