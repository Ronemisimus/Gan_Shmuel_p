#!/bin/bash

docker-compose down
#docker rmi -f $(docker image ls -a -f 'dangling=true' -q) provider
docker volume rm $(docker volume ls -f dangling=true)