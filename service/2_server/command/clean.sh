#!/bin/bash

if [[ $1 == 1 || $1 == y || $1 == Y ]]; then
	read -p "Are you sure to remove vaolume and network? [Y/y]: " res 

	if [[ $res == y || $res == Y ]]; then
		total=1
	fi
fi

docker rm -f  $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker ps -a
docker images -a

if [[ $total == 1 ]]; then
	docker volume ls
	docker volume prune -f

	docker network ls
	docker network prune -f
fi

