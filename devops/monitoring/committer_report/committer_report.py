from flask import Flask, request
import json
import os
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com' 
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = "gan.shmuel.ashdod@gmail.com"
app.config['MAIL_PASSWORD'] = "nA@UemKJPlo0GjperLN4"
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Gan Shmuel]' 
app.config['FLASKY_MAIL_SENDER'] = 'Gan Shmuel Admin <gan.shmuel.ashdod@gmail.com>'

mail = Mail(app)

# def send_email(to, subject, template, **kwargs): 
#    # msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,  sender=app.config'FLASKY_MAIL_SENDER'], recipients=[to]) 
#    # msg.body = render_template(template + '.txt', **kwargs) 
#    # msg.html = render_template(template + '.html', **kwargs) 
#    # mail.send(msg)
    

@app.route('/committer_report', methods=['POST'])
def log():
   data = request.get_json()
   user_name =  data['repository']['name']

   # data = json.loads(request.data)
   msg_to_send = "New commit by: {}".format(user_name)
   msg = Message(msg_to_send, sender="gan.shmuel.ashdod@gmail.com",  recipients=["eigorek@gmail.com"])
   mail.send(msg)
   return "ok"
   # return "New commit by: {}".format(data['commits'][0]['author']['name'])

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8084, threaded=True, debug=True)