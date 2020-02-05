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
    "M-Wittner" : "",
    "RonBenMoshe" : "",
    "Neta182" : ""
}

providers_team_lead = "RonBenMoshe"

devops_team = {
    "IgorEnenberg" : "eigorek@gmail.com",
    "itzik-alayev" : "",
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

def gitOrGmail(team, name, email):
    if mail.find(gmail):
        return mail
    else:
        return team[name]

def emailRecipient(recipients, pusher, pushers_email, team):
    team_lead = "{}_lead".format(team)
    recipients.append(gitOrGmail(team, team_lead, team[team_lead]))

    if pusher != team_lead:
        recipients.append(gitOrGmail(team, pusher, pushers_email))


@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    commits_report(data)
    tests_report(data)   

    pushers_email = "{}".format(data['pusher']['email'])
    pusher = "{}".format(data['pusher']['name'])
    recipients = []

    if pusher in weight_team:
        recipients = emailRecipient(recipients, pusher, pushers_email, weight_team)
    elif pusher in providers_team:
        recipients = emailRecipient(recipients, pusher, pushers_email, providers_team)
    elif pusher in devops_team:
        recipients = emailRecipient(recipients, pusher, pushers_email, devops_team)

    entry = "Tests and Commits Reports for {}'s Latest Push".format(data['pusher']['name'])

    send_email(entry, ["test_log.txt", "committers_log.txt"], recipients)    
#
    return Response("200")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)