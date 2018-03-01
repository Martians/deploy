#!/bin/sh
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

NAME=sshd
PORT=2222

REPO="public"
MORE=$1
#REPO=""

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/script/config.sh
IMAGE=centos:$NAME

<<'COMMENT'
docker rm -f $NAME
docker rmi -f $IMAGE
COMMENT

echo "always clear exist sshd host"
docker rm -f host

if [[ "$#" > 0 ]]; then
    docker rmi -f $IMAGE
fi

###############################################################
if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
    set -x
	docker build -t $IMAGE -f 0_server --build-arg SERVICE=$NAME --build-arg MORE="$MORE" \
		--build-arg LISTEN="$PORT" --build-arg REPO="$REPO" .
    set +x
fi

set -x
docker run -itd --name host -h host $IMAGE -p $PORT:$PORT
set +x

echo
###############################################################
echo "set  host address:"

echo "clean cache:
    rm ~/.ssh/known_hosts -f
or,
    echo "StrictHostKeyChecking=no" > ~/.ssh/config
    echo "UserKnownHostsFile=/dev/null" >> ~/.ssh/config
"

echo "enter host:
    docker exec -it host /bin/bash
    
    ssh root@$HOST2
"