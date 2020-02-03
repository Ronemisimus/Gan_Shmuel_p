FROM python:3.6-alpine
WORKDIR /ci-test
RUN mkdir production
RUN apk add docker && apk add docker-compose && apk add git
RUN pip install flask && pip install dotenv
COPY app.py .

ENTRYPOINT ["python3", "app.py"]
