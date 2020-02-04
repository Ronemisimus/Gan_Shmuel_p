FROM python:3.6-buster
WORKDIR /ci-test
RUN mkdir production
RUN apt-get install docker && apt-get install docker-compose && apt-get install git
RUN pip install flask && pip install python-dotenv
COPY app.py .

ENTRYPOINT ["python3", "app.py"]
