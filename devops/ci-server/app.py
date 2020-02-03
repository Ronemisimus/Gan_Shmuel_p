from flask import Flask, Response
import os

app = Flask(__name__)

REPOSITORY_URL = 'https://github.com/ChrisPushkin/Gan_Shmuel_p.git'
CLONE_DIR = '../production'
BRANCHES = {
#	BRANCH		DOCKER-COMPOSE PATH
	'weight': 	'../weight/docker-compose.yml',
	'provider': '../provider/providers/docker-compose.yml'
}

@app.route('/payload', methods=['POST'])
def gitWebHook():
	for branch in BRANCHES:
		os.system('rm -rf ../{}'.format(branch))
		os.system('git clone {} --single-branch -b {} ../{}'.format(REPOSITORY_URL, branch, branch))
		os.system('docker-compose -f {} up --build -d'.format(BRANCHES[branch]))
	return Response(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, threaded=True, debug=True)
