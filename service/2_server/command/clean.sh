#!/bin/bash

docker rm -f  $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker ps -a
docker images -a

if [[ $1 == 1 ]]; then
	echo 11
	read -p "Are you sure to remove vaolume and network? [Y/y]: " res 
	
	if [[ $res == y || $res == Y ]]; then
		docker volume ls
		docker volume prune -f

		docker network ls
		docker network prune -f
	fi
fi