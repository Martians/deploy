#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

NAME=postgres

MORE=$1
#REPO=""

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

echo "always clear exist postgres host"
docker rm -f $NAME

###############################################################
if [[ "$#" > 0 ]]; then
	docker rm -f $NAME
fi

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
sudo pipework $DEVICE $NAME $DB_HOST/$SUBNET@$GATEWAY

echo "show host address:"
docker exec $NAME ip addr show eth1 | grep inet | grep [0-9.]*/ --color
echo

###############################################################
echo "@@@@@@@@ enter postgres host: /docker/service/script/hadoop/postgres.sh"
docker exec -it $NAME /docker/service/script/hadoop/postgres.sh

echo "enter host:
    docker exec -it $NAME /bin/bash
"
ssh root@$DB_HOST
