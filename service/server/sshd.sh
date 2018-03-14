#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

NAME=sshd
PORT=22

REPO="public local proxy"
MORE=$1
#REPO=""

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

echo "always clear exist sshd host"
docker rm -f host1 host2 

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
docker run -itd --name host1 -h host1 $GLOBAL_MACRO $IMAGE 
docker run -itd --name host2 -h host2 $GLOBAL_MACRO $IMAGE 
set +x

echo
###############################################################
echo "set  host address:"
sudo pipework $DEVICE host1 $HOST1/$SUBNET@$GATEWAY
sudo pipework $DEVICE host2 $HOST2/$SUBNET@$GATEWAY

echo "clean cache:
    rm ~/.ssh/known_hosts -f
or,
    echo "StrictHostKeyChecking=no" > ~/.ssh/config
    echo "UserKnownHostsFile=/dev/null" >> ~/.ssh/config
"

echo "show host address:"
docker exec host1 ip addr show eth1 | grep inet | grep [0-9.]*/ --color
docker exec host2 ip addr show eth1 | grep inet | grep [0-9.]*/ --color
echo

echo "enter host:
    docker exec -it host1 /bin/bash
    docker exec -it host2 /bin/bash
    
    ssh root@$HOST1
    ssh root@$HOST2
"