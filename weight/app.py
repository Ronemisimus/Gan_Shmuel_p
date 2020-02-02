from flask import Flask
from db import db_api
app = Flask(__name__)

app.register_blueprint(db_api)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000 , debug=True)