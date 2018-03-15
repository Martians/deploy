#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

NAME=host

HOST1=192.168.36.91
HOST2=192.168.36.92

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=centos:base

<<'COMMENT'
docker rm -f $NAME
docker rmi -f $IMAGE
COMMENT

docker rm -f h1 h2 

if [[ "$#" > 0 ]]; then
    docker rmi -f $IMAGE
fi

###############################################################
docker run -itd --name h1 -h h1 $GLOBAL_MACRO $IMAGE 
docker run -itd --name h2 -h h2 $GLOBAL_MACRO $IMAGE 

<<'COMMENT'
echo
###############################################################
echo "set  host address:"
sudo pipework $DEVICE h1 $HOST1/$SUBNET@$GATEWAY
sudo pipework $DEVICE h2 $HOST2/$SUBNET@$GATEWAY
COMMENT

echo "show host address:"
docker exec h1 ip addr show eth0 | grep inet | grep [0-9.].*/ --color
docker exec h2 ip addr show eth0 | grep inet | grep [0-9.].*/ --color
echo

echo "enter host:
    docker exec -it h1 /bin/bash
    docker exec -it h2 /bin/bash
"
