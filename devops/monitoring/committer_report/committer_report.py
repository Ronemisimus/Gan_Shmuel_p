from flask import Flask, request, Response
import json
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "gan.shmuel.ashdod@gmail.com"
app.config['MAIL_PASSWORD'] = "nA@UemKJPlo0GjperLN4"

mail = Mail(app)

@app.route('/health', methods=['GET'])
def heath_test():
    return Response(status=200)

@app.route('/committer_report', methods=['POST'])
def log():

    data = request.get_json()


    pusher_email = data['pusher']['email']

    


    commits = data['commits']

    messages = ""
    for commit in commits:
        messages += ("Commit id:{}\nMessage: {}\n\n".format(commit['id'], commit["message"]))
    email_subject = "New Push By: {}".format(data['pusher']['name'])

    email = Message(email_subject, sender="gan.shmuel.ashdod@gmail.com", recipients=["eigorek@gmail.com", "chrispushkin@gmail.com"])

    email.body = (messages)

    os.system('docker ps -q | xargs -L 1 docker logs > log.txt')  
    with current_app.open_resource("log.txt") as fp:
        msg.attach("log.txt", "text/plain", fp.read())

    mail.send(email)

    return Response("200")

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)