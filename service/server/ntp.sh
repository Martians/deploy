#!/bin/sh

NAME=ntp
PORT="123/udp"
REPO=""

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=centos:$NAME

<<'COMMENT'
docker rm -f $NAME
docker rmi -f $IMAGE
COMMENT

if [[ "$#" > 0 ]]; then
    docker rm -f $NAME
    docker rmi -f $IMAGE
fi
###############################################################

if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
	docker build -t $IMAGE -f 0_centos --build-arg SERVICE=$NAME \
		--build-arg LISTEN="$PORT" --build-arg REPO="$REPO" .
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
	echo "create docker"
	docker run -itd --name $NAME -p 123:$PORT -h $NAME $IMAGE
	# docker run -itd --name $NAME -P $IMAGE # not work?
elif [ "`docker ps | grep $NAME$`" == "" ]; then
	echo "start docker"
	docker start $NAME
else
	echo "start already"
fi

sudo netstat -antp | grep :$PORT[\t\ ] --color