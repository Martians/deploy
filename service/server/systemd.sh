#!/bin/sh
# config http://blog.csdn.net/field_yang/article/details/51568861

# http://blog.csdn.net/luckytanggu/article/details/71514798

NAME=systemd

MORE=$1
#REPO=""
PORT=22

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=centos:sshd

SYSTMD="--privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup"
Initial=/usr/sbin/init

<<'COMMENT'
docker rm -f sshd
docker rmi -f $IMAGE
COMMENT

echo "always clear exist sshd host"
docker rm -f $NAME

set -x
docker run -itd --name $NAME -h $NAME $GLOBAL_MACRO $SYSTMD $IMAGE $Initial
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
