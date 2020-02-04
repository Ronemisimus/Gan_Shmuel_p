from flask import Flask, Response, request
import os
import sys
from dotenv import load_dotenv, find_dotenv
from time import sleep

app = Flask(__name__)

WORKDIR = '/ci-server'
REPOSITORY_URL = 'https://github.com/ChrisPushkin/Gan_Shmuel_p.git'
TESTING_DIR = 'test/'
PRODUCTION_DIR = 'production/'

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


@app.route('/payload', methods=['POST'])
def gitWebHook():
	data = request.get_json()
	branch = data['ref'].split('/')[-1]

	os.system('rm -rf {}{}'.format(TESTING_DIR, branch))
	os.system('git clone {} --single-branch -b {} {}{}'.format(REPOSITORY_URL, branch, TESTING_DIR, branch))

	'''
	# TODO: CI for CI.
	if branch == 'devops':
		compose_file = find('docker-compose.yml', '{}{}'.format(TESTING_DIR, branch))

		os.system('docker-compose -f {} build'.format(compose_file))
		os.system('docker-compose restart')
		return Response(200)
	'''

	if branch == 'weight' or branch == 'provider':
		environment = 'test'

		# Finding the Dockerfile
		docker_file = find('Dockerfile', '{}{}'.format(TESTING_DIR, branch))
		docker_path = '/'.join(docker_file.split('/')[:-1])

		# Finding the docker-compose file
		compose_file = find('docker-compose.yml', '{}{}'.format(TESTING_DIR, branch))
		compose_path = '/'.join(compose_file.split('/')[:-1])

		# Load .env file as environment variables
		load_dotenv('{}/.env'.format(compose_path), override=True)

		# Build Dockerfile to get image artifact
		os.system('docker build -t {} ./{}'.format(branch, docker_path))

		# Run the test build
		os.chdir(compose_path)
		os.system('docker-compose -p {}-{} up -d'.format(environment, branch))
		os.chdir(WORKDIR)

		# MAIN TODO:
		# End-2-End testing
	
	if branch == 'master':
		environment = 'prod'

		# TODO: build all folders in master branch
		# 		test them and run as production

	'''
	# WILL BE USED LATER

	# Test complete, remove test containers and update production containers
	# ..to work with new images.
	#os.system('docker-compose -f {} kill'.format(compose_file))
	
	# Copy successful test clone to staging
	os.system('rm -rf {}{}'.format(PRODUCTION_DIR, compose_path))
	os.system('cp -rf {} {}'.format(compose_path, PRODUCTION_DIR))

	# Run app with production port
	os.environ['PORT'] = prod_port
	os.system('docker-compose -f {}{}/docker-compose.yml -p prod-{} up -d'.format(PRODUCTION_DIR, compose_path.split('/')[-1], os.environ['IMAGE_NAME']))
	'''
	return Response(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, threaded=True, debug=True)
