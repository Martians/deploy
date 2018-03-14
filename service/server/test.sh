#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

NAME=test

MORE=$1
#REPO=""

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=centos:$NAME

<<'COMMENT'
docker rm -f sshd
docker rmi -f $IMAGE
COMMENT

echo "always clear exist sshd host"
docker rm -f $NAME

if [[ "$#" > 0 ]]; then
    docker rmi -f $IMAGE
fi

###############################################################
if [ ! `docker images $IMAGE -q` ]; then
	echo "create image: "
	set -x
	docker build -t $IMAGE -f 0_test --build-arg MORE="$MORE" .
	set +x
fi

set -x
docker run -itd --name $NAME -h $NAME $GLOBAL_MACRO $IMAGE 
set +x

echo
###############################################################
echo "set  host address:"
sudo pipework $DEVICE $NAME $TEST_HOST/$SUBNET@$GATEWAY

echo "show host address:"
docker exec $NAME ip addr show eth1 | grep inet | grep [0-9.]*/ --color
echo

echo "enter host:
    docker exec -it $NAME /bin/bash
    ssh root@$TEST_HOST
"

echo "@@@@@@@@ enter test host @@@@@@@@@"
docker exec -it $NAME /bin/bash
