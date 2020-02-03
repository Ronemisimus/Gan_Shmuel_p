from flask import Flask, Response, request
import requests
import os
import sys

app = Flask(__name__)

REPOSITORY_URL = 'https://github.com/ChrisPushkin/Gan_Shmuel_p.git'
TESTING_DIR = 'test/'
PRODUCTION_DIR = 'production/'
BRANCHES = {
#	BRANCH		DOCKER-COMPOSE PATH
	'weight': 	'../weight/docker-compose.yml',
	'provider': '../provider/providers/docker-compose.yml'
}

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

@app.route('/payload', methods=['POST'])
def gitWebHook():
	data = request.get_json()
	branch = data['ref'].split('/')[-1]
	user_name =  data['pusher']['name']
	email = data['pusher']['email']

	os.system('rm -rf {}*'.format(TESTING_DIR))
	print('{}{}'.format(TESTING_DIR, branch), file=sys.stderr)
	os.system('git clone {} --single-branch -b {} {}{}'.format(REPOSITORY_URL, branch, TESTING_DIR, branch))
	compose_file = find('docker-compose.yml', '{}{}'.format(TESTING_DIR, branch))
	print('compose_file: {}'.format(compose_file), file=sys.stderr)
	os.system('docker-compose -f {} up -d'.format(compose_file))

	'''
		TODO: end to end testing goes here
	'''

	os.system('docker-compose -f {} rm -f'.format(compose_file))
	os.system('rm -rf {}/{}'.format(PRODUCTION_DIR, branch))
	os.system('mv {}{} {}{}'.format(TESTING_DIR, branch, PRODUCTION_DIR, branch))
	os.system('rm -rf test')
	compose_file = find('docker-compose.yml', '{}{}'.format(PRODUCTION_DIR, branch))
	os.system('docker-compose -f {} rm -f'.format(compose_file))
	os.system('docker-compose -f {} up -d'.format(compose_file))
	return Response(status=200)



	'''for branch in BRANCHES:
		os.system('rm -rf ../{}'.format(branch))
		os.system('git clone {} --single-branch -b {} ../{}'.format(REPOSITORY_URL, branch, branch))
		os.system('docker-compose -f {} up --build -d'.format(BRANCHES[branch]))
	'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, threaded=True, debug=True)
