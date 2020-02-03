from flask import Flask, request, Response
import json
import os
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

   msg = Message("New Commit By: {}".format(data['committer', 'name']), sender="gan.shmuel.ashdod@gmail.com",  recipients=["eigorek@gmail.com"])
   msg.body("Commit Message: {}".format(data['head_commit', 'message']))
   mail.send(msg)
   return Response("200")

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)
