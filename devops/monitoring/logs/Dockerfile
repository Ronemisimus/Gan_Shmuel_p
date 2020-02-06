FROM python:3.6-alpine
WORKDIR /monitoring/logs
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY logs.py .
ENTRYPOINT ["python3", "logs.py"]
