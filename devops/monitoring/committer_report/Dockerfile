FROM python:3.6-alpine
WORKDIR /monitoring/committer_report
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "committer_report.py"]
