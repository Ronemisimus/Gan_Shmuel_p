from flask import Flask

app = Flask(__name__)

@app.route('/payload', methods=['POST'])
def gitWebHook():
        return 'a push has been made.'


if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8085, threaded=True, debug=True)
