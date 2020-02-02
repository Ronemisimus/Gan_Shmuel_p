#!/bin/bash

docker container rm -f chat_app_1 chat_db_1
docker rmi -f chat_app chat_db
docker-compose up --build