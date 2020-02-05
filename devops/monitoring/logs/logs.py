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

weight_team = {
    "nati-elmaliach" : "natielmaliach3197@gmail.com",
    "Aransh" : "aranshavit@gmail.com",
    "ozshm" : "ozshmuel@gmail.com",
    "KateDvo" : "kate.dvoretsky@gmail.com"
}

weight_team_lead = "nati-elmaliach"

providers_team = {
    "M-Wittner" : "Matan.wittner@gmail.com",
    "RonBenMoshe" : "RonBenMoshe@gmail.com",
    "Neta182" : "Netaba@mta.ac.il"
}

providers_team_lead = "RonBenMoshe"

devops_team = {
    "IgorEnenberg" : "eigorek@gmail.com",
    "itzik-alayev" : "startukk@gmail.com",
    "ChrisPushkin" : "chrispushkin@gmail.com"
}

devops_team_lead = "ChrisPushkin"

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

    # data["tests"] = { 
    #     "app_name" : "weight",
    #     "test_result" : "failure"
    # }

    messages += "Tests for {}: {}".format(data["tests"]["app_name"], data["tests"]["test_result"])

    entry = "Dummy Test Report for {}'s Latest Push".format(data['pusher']['name'])

    log_entry("\n" + entry + "\n\n" + messages, "test_log.txt")

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    commits_report(data)
    tests_report(data)   

    pushers_email = "{}".format(data['pusher']['email'])
    pusher = "{}".format(data['pusher']['name'])
    recipients = []

    if pusher in weight_team:
        recipients.append(weight_team[weight_team_lead])
        if pusher != weight_team_lead:
            recipients.append(weight_team[pusher] if weight_team[pusher] else pushers_email)
    elif pusher in providers_team:
        recipients.append(providers_team[providers_team_lead])
        if pusher != providers_team_lead:
            recipients.append(providers_team[pusher] if providers_team[pusher] else pushers_email)
    elif pusher in devops_team:
        recipients.append(devops_team[devops_team_lead])  
        if pusher != devops_team_lead:
            recipients.append(devops_team[pusher] if devops_team[pusher] else pushers_email)      

    entry = "Tests and Commits Reports for {}'s Latest Push".format(data['pusher']['name'])

    send_email(entry, ["test_log.txt", "committers_log.txt"], recipients)    
#
    return Response("200")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)