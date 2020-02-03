FROM python:3.6-alpine
WORKDIR .
RUN pip install flask
RUN pip install flask-mail

COPY committer_report.py .

ENTRYPOINT ["python3", "committer_report.py"]
