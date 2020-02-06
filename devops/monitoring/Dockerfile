#monitoring on port 8084
FROM python:3.6-alpine
WORKDIR /monitor-test
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY monitor.py .

ENTRYPOINT ["python3", "monitor.py"]
