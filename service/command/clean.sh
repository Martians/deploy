#!/bin/bash

docker rm -f  $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker ps -a
docker images -a
