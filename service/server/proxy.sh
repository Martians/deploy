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


if [ ! -n "$PROXY_SRC" -o ! -d "$PROXY_SRC" ]; then
    PROXY_SRC=~/proxy
fi
PROXY_DST=/var/cache/apt-cacher-ng

<<'COMMENT'
docker rmi -f $IMAGE
docker rm -f $NAME
COMMENT

if [[ "$#" > 0 ]]; then
    docker rm -f $NAME
    docker rmi -f $IMAGE
fi

###############################################################
if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
    set -x
	docker build -t $IMAGE -f 0_proxy .
    set +x
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
    echo -e  "${GREEN_COLOR}-- create docker -- ${RES}"
    set -x
    docker run -itd --name $NAME -h $NAME $GLOBAL_MACRO -v $PROXY_SRC:$PROXY_DST -p $PORT:$PORT $IMAGE
    set +x

elif [ "`docker ps | grep $NAME$`" == "" ]; then
    echo -e  "${GREEN_COLOR}-- starting docker ... --${RES}"
    docker start $NAME
else
    echo -e  "${GREEN_COLOR}-- already started --${RES}"
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
