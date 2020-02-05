FROM python:3.6-alpine
WORKDIR /monitoring/logs
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "logs.py"]
