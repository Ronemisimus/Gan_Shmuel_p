#monitoring on port 8084
FROM python:3.6-alpine
WORKDIR /monitor-test
RUN pip install flask && pip install requests
COPY monitor.py .

ENTRYPOINT ["python3", "monitor.py"]
