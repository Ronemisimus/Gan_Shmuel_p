from flask import Flask, Response, request
import os
import sys
from dotenv import load_dotenv, find_dotenv
from time import sleep
import subprocess
import requests

app = Flask(__name__)

WORKDIR = '/ci-server'
REPOSITORY_URL = 'https://github.com/ChrisPushkin/Gan_Shmuel_p.git'
TESTING_DIR = 'test/'
STAGE_DIR = 'stage/'
PRODUCTION_DIR = 'production/'
TEST_PORT = "8082"

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

def killCompose(environment, app):
	os.system('docker-compose -p {}-{} kill'.format(environment, app))
	os.system('docker-compose -p {}-{} rm -f'.format(environment, app))

@app.route('/payload', methods=['POST'])
def gitWebHook():
	data = request.get_json()
	branch = data['ref'].split('/')[-1]
	main_folder = os.getcwd()

	data['tests'] = {}

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
		# Finding the Dockerfile
		docker_file = find('Dockerfile', '{}{}'.format(TESTING_DIR, branch))
		docker_path = '/'.join(docker_file.split('/')[:-1])

		# Finding the docker-compose file
		compose_file = find('docker-compose.yml', '{}{}'.format(TESTING_DIR, branch))
		compose_path = '/'.join(compose_file.split('/')[:-1])

		# Load .env file as environment variables
		load_dotenv('{}/.env'.format(compose_path), override=True)
		stage_port = os.environ['PORT']

		# Build Dockerfile to get image artifact
		os.system('docker build -t {} ./{}'.format(branch, docker_path))

		# Start testing environment
		os.chdir(compose_path)
		environment = 'test'
		os.environ['PORT'] = TEST_PORT
		os.system('docker-compose -p {}-{} down -v && docker-compose -p {}-{} rm -fv'.format(environment, branch, environment, branch))
		os.system('docker-compose -p {}-{} up -d'.format(environment, branch))
		
		# Tests go here
		print('Running tests...')
		os.environ['TEST_URL'] = 'http://localhost'
		sleep(10)
		
		test_output = 'Could not open test file.'
		try:
			test_output = subprocess.check_output(['python3', 'test/tests.py']).decode('utf-8')
		except:
			os.system('docker-compose kill')
			os.system('docker-compose rm -f')
			print('Could not open test file.', file=sys.stderr)
		
		killCompose(environment, branch)
		data['tests'] = {'app_name': branch, 'test_result': test_output}
		requests.post('http://localhost:8084/log', json=data)

		if test_output.strip('\n') == '0':
			# Test was successfulprint(test_output, file=sys.stderr), run the tested image in stage environment
			# and move its source code to stage/ folder
			print('Test succedded, going to staging.', file=sys.stderr)

			environment = 'stage'
			os.environ['PORT'] = stage_port
			os.system('docker-compose -p {}-{} up -d'.format(environment, branch))

			os.chdir(main_folder)
			os.system('rm -rf {}{} && cp -R {}/ {}{}'.format(STAGE_DIR, branch, compose_path, STAGE_DIR, branch))
		else:
			print('Tests failed!\nThis build is not going to staging.', file=sys.stderr)
			print(test_output, file=sys.stderr)
			os.chdir(main_folder)

	if branch == 'master':
		compose_files = find_all('docker-compose.yml', '{}{}'.format(TESTING_DIR, branch))
		compose_paths = [('/').join(file.split('/')[:-1]) for file in compose_files]

		for path in compose_paths:
			environment = 'test'
			if path.find('devops') != -1:
				continue

			load_dotenv(dotenv_path='{}/.env'.format(path), override=True)
			app_name = os.environ['IMAGE_NAME']
			prod_port = os.environ['PROD_PORT']

			# Build app image
			os.system('docker build -t {} ./{}'.format(app_name, '/'.join(find('Dockerfile', path).split('/')[:-1])))

			# Run test docker-compose
			os.chdir(path)
			os.environ['PORT'] = TEST_PORT
			os.system('docker-compose -p {}-{} down -v && docker-compose -p {}-{} rm -fv'.format(environment, app_name, environment, app_name))
			os.system('docker-compose -p {}-{} up -d'.format(environment, app_name))

			# Tests go here
			print('Running tests...', file=sys.stderr)
			os.environ['TEST_URL'] = 'http://localhost'
			sleep(10)

			test_output = 'Could not open test file.'
			try:
				test_output = subprocess.check_output(['python3', 'test/tests.py']).decode('utf-8')
			except:
				os.system('docker-compose kill')
				os.system('docker-compose rm -f')
				print('Could not open test file.', file=sys.stderr)
			
			killCompose(environment, app_name)
			data['tests'] = {'app_name': app_name, 'test_result': test_output}
			print(data, file=sys.stderr)
			requests.post('http://localhost:8084/log', json=data)

			if test_output.strip('\n') == '0':
				# Test was successful, run the tested image in stage environment
				# and move its source code to stage/ folder
				print('Test succedded, going to staging.', file=sys.stderr)

				environment = 'prod'
				os.environ['PORT'] = prod_port
				os.system('docker-compose -p {}-{} up -d'.format(environment, app_name))

				os.chdir(main_folder)
				os.system('rm -rf {}{} && cp -R {}/ {}{}'.format(PRODUCTION_DIR, app_name, path, PRODUCTION_DIR, app_name))
			else:
				print('Tests failed!\nThis build is not going to production.', file=sys.stderr)
				print(test_output, file=sys.stderr)
				os.chdir(main_folder)
				continue
	return Response(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8085, debug=True)
