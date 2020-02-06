#!/bin/bash

docker build -t provider ./app
docker-compose up --build