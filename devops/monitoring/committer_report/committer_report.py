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

   commits = data['commits']

   messages = ""
   
	for commit in commits:
      messages.append("Commit Message: {}\n".format(commit["message"]))

   email_subject = "New Push By: {}".format(data['pusher']['name'])

   email = Message(email_subject, sender="gan.shmuel.ashdod@gmail.com", recipients=["eigorek@gmail.com"])

   email.body = message)

   mail.send(email)
   
   return Response("200")

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)
