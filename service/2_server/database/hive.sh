#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# http://blog.csdn.net/luckytanggu/article/details/71514798

NAME=hive
HOST=192.168.36.92

MORE=$1
#REPO=""
PORT=""

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=centos:sshd

<<'COMMENT'
docker rm -f sshd
docker rmi -f $IMAGE
COMMENT

if [[ "$#" > 0 ]]; then
	docker rm -f $NAME
fi

###############################################################
# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
	echo -e  "${GREEN_COLOR}-- create docker -- ${RES}"
	set -x
	docker run -itd --name $NAME -h $NAME $GLOBAL_MACRO $SYSTMD $IMAGE $INITIAL
	set +x
	
elif [ "`docker ps | grep $NAME$`" == "" ]; then
	echo -e  "${GREEN_COLOR}-- starting docker ... --${RES}"
	docker start $NAME
else
	echo -e  "${GREEN_COLOR}-- already started --${RES}"
fi

###############################################################
echo "set  host address:"
sudo pipework $DEVICE $NAME $HOST/$SUBNET@$GATEWAY

echo "show host address:"
docker exec $NAME ip addr show eth1 | grep inet | grep [0-9.].*/ --color
echo

###############################################################
echo "@@@@@@@@ enter generate host: /docker/service/script/hadoop/hive.sh"
docker exec -it $NAME /docker/service/script/hadoop/hive.sh

echo "enter host:
    docker exec -it $NAME /bin/bash
    ssh root@$HOST
"

###############################################################
echo "beeline: !connect jdbc:hive2://localhost:10000/default"
docker exec -it hive /bin/bash

