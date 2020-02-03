FROM python:3.6-alpine
WORKDIR /ci-test
RUN apk add docker && apk add docker-compose && apk add git
RUN pip install flask 
COPY app.py .

ENTRYPOINT ["python3", "app.py"]
