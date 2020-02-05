from flask import Flask, request, Response
from flask_mail import Mail, Message
import json
import os
from datetime import datetime, timezone
import pytz

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "gan.shmuel.ashdod@gmail.com"
app.config['MAIL_PASSWORD'] = "nA@UemKJPlo0GjperLN4"

weight_group = [
    "nati-elmaliach",
    "Aransh",
    "ozshm",
    "KateDvo" 
]

providers_group = {
    "M-Wittner",
    "RonBenMoshe",
    "Neta182" 
}

devops_group = {
    "IgorEnenberg",
    "itzik-alayev",
    "ChrisPushkin" 
}

mail = Mail(app)

def log_entry(entry, log_name):
    with open(os.getcwd() + "/" + log_name, "w+") as log:
        tz = pytz.timezone('Asia/Jerusalem')
        isr_now = datetime.now(tz)
        log.write("{}".format(isr_now))
        log.write(entry)
        log.write("\n********************************************************\n")

def send_email(subject, logs, recipients_list):
    email = Message(subject, sender="gan.shmuel.ashdod@gmail.com", recipients=recipients_list)

    for log in logs:
        with app.open_resource(os.getcwd() + "/" + log) as fp:
            email.attach(log, "text/plain", fp.read())

    mail.send(email)

def commits_report(data):   
    messages = ""
    for commit in data['commits']:
        messages += "Commit ID: {}\nCommit Timestamp: {}\nMessage: {}\n\n".format(commit['id'], commit['timestamp'], commit["message"])

    entry = "{}'s Latest Commits".format(data['pusher']['name'])

    log_entry("\n" + entry + "\n\n" + messages, "committers_log.txt")

    return Response("200")

def tests_report(data):
    messages = ""

    data["tests"] = { 
        "test1" : "success",
   	    "test2" : "failure",
   	    "test3" : "success",
        "test4" : "success",
        "test5" : "success"
    }
    
    for k, v in data["tests"].items(): 
        messages += "{} {}\n".format(k, "was successful." if v == "success" else "has failed.")

    entry = "Dummy Test Report for {}'s Latest Push".format(data['pusher']['name'])

    log_entry("\n" + entry + "\n\n" + messages, "test_log.txt")

@app.route('/log', methods=['POST'])
def test():
    data = request.get_json()
    commits_report(data)
    tests_report(data)   

    pushers_email = "{}".format(data['pusher']['email'])
    pusher = "{}".format(data['pusher']['name'])
    recipients = []
    if pusher in weight_group:
        recipients = ["natielmaliach3197@gmail.com", pushers_email]
        # recipients = ["eigorek@gmail.com"]
    elif pusher in providers_group:
        recipients = ["ronmoshe333@gmail.com", pushers_email]
        # recipients = ["eigorek@gmail.com"]
    elif pusher in devops_group:
        recipients = ["chrispushkin@gmail.com", pushers_email]

    entry = "Tests and Commits Reports for {}'s Latest Push".format(data['pusher']['name'])

    send_email(entry, ["test_log.txt", "committers_log.txt"], recipients)    

    return Response("200")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)