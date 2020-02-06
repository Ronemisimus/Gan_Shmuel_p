FROM python:3.6-alpine
WORKDIR /ci-server
RUN apk add docker && apk add docker-compose && apk add git && apk add bash
RUN pip install flask
RUN pip install python-dotenv
RUN pip install requests
RUN mkdir test && mkdir stage && mkdir production
COPY app.py .
COPY index.html .

ENTRYPOINT ["python3", "app.py"]
