#!/bin/sh
# config http://blog.csdn.net/field_yang/article/details/51568861

# http://blog.csdn.net/luckytanggu/article/details/71514798

NAME=generate

MORE=$1
#REPO=""
PORT="808"

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

if [[ "$#" > 0 ]]; then
	docker rm -f $NAME
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
	echo -e  "${GREEN_COLOR}-- create docker -- ${RES}"
	set -x
	docker run -itd --name $NAME -h $NAME $GLOBAL_MACRO $SYSTMD -p 808:808 -p 3360:3360 $IMAGE $Initial
	set +x
	
elif [ "`docker ps | grep $NAME$`" == "" ]; then
	echo -e  "${GREEN_COLOR}-- starting docker ... --${RES}"
	docker start $NAME
else
	echo -e  "${GREEN_COLOR}-- already started --${RES}"
fi

###############################################################
echo "set  host address:"
sudo pipework $DEVICE $NAME $TEST_HOST/$SUBNET@$GATEWAY

echo "show host address:"
docker exec $NAME ip addr show eth1 | grep inet | grep [0-9.]*/ --color
echo

###############################################################
echo "@@@@@@@@ enter generate host: /docker/script/hadoop/generate.sh"
docker exec -it $NAME /docker/script/hadoop/generate.sh

echo "enter host:
    docker exec -it $NAME /bin/bash
    http://$LOCAL:$PORT
"