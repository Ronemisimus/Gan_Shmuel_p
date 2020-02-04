from flask import Flask, request, Response
import json
from flask_mail import Mail, Message
import os
from time import gmtime, strftime
import sched, time

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "gan.shmuel.ashdod@gmail.com"
app.config['MAIL_PASSWORD'] = "nA@UemKJPlo0GjperLN4"

email_recipients = ["eigorek@gmail.com"]

mail = Mail(app)

def log_entry(entry, log_name):
    with open(os.getcwd() + "/" + log_name, "a+") as log:
        log.write(strftime("%B %d, %Y %H:%M:%S (UTC)\n", gmtime()))
        log.write(entry)
        log.write("\n********************************************************")

def send_email(subject, messages, log_name):
    email = Message(subject, sender="gan.shmuel.ashdod@gmail.com", recipients=email_recipients)
    email.body = messages

    with app.open_resource(os.getcwd() + "/" + log_name) as fp:
        email.attach("log.txt", "text/plain", fp.read())

    mail.send(email)

@app.route('/committer_report', methods=['POST'])
def log():   
    data = request.get_json()

    messages = ""
    for commit in data['commits']:
        messages += ("Commit id:{}\nMessage: {}\n\n".format(commit['id'], commit["message"]))

    entry = "New Push From {}".format(data['pusher']['name'])

    log_entry("\n" + entry + "\n\n" + messages, "log.txt")
    send_email(entry, messages, "log.txt")    

    return Response("200")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)