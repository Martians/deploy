#!/bin/sh

NAME=proxy
PORT=3142
# REPO="public local"
REPO=""

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=ubuntu:$NAME

if [ "$PROXY_SRC" -a ! -d $PROXY_SRC ]; then
    PROXY_SRC=~/proxy
fi
PROXY_DST=/var/cache/apt-cacher-ng

<<'COMMENT'
docker rmi -f $IMAGE
docker rm -f $NAME
COMMENT

###############################################################
if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
	docker build -t $IMAGE -f 0_proxy .
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
    echo "create docker"
    docker run -itd --name $NAME -h $NAME -v $PROXY_SRC:$PROXY_DST -p $PORT:$PORT $IMAGE
    
elif [ "`docker ps | grep $NAME$`" == "" ]; then
    echo "start docker"
    docker start $NAME
else
    echo "start already"
fi

sudo netstat -antp | grep :$PORT[\t\ ] --color
echo "brower:
    http://$LOCAL:$PORT
"

# docker exec -it proxy /bin/bash
# check state
echo "check state:
    docker exec proxy du -ch --max-depth=1 /var/cache/apt-cacher-ng
    docker logs -f proxy 
"

################################################################
## client
## centos: /docker/script/initialize.sh public local proxy
