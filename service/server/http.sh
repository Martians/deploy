#!/bin/sh

NAME=http
PORT="80"
REPO=/home/long

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

###############################################################

if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
	docker build -t $IMAGE -f 0_centos --build-arg SERVICE=$NAME --build-arg LISTEN="$PORT" .
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
	echo "create docker"
	docker run -itd --name $NAME -h $NAME -v $REPO:/html -p $PORT:$PORT $IMAGE
	# docker run -itd --name $NAME -h $NAME -v $REPO:/html -P $IMAGE
	
elif [ "`docker ps | grep $NAME$`" == "" ]; then
	echo "start docker"
	docker start $NAME
else
	echo "start already"
fi

#echo "prepare network"
#HOST=192.168.36.27
#sudo pipework ens33 $NAME $HOST/$SUB@$GATEWAY

#echo "test dns"
sudo netstat -antp | grep :$PORT[\t\ ] --color
echo "brower:
    http://192.168.36.10
"