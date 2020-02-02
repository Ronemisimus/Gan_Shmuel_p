FROM python:3.6-alpine
WORKDIR /ci-test
RUN pip install flask
COPY app.py .

ENTRYPOINT ["python3", "app.py"]
