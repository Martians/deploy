#!/bin/sh

NAME=dns
PORT="53 53/udp"

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=centos_$NAME

<<'COMMENT'
docker rm -f $NAME
COMMENT
docker rmi -f $IMAGE

###############################################################

if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
	docker build -t $IMAGE -f 0_centos --build-arg SERVICE=$NAME --build-arg LISTEN="$PORT" .
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
	echo "create docker"
	docker run -itd --name $NAME -p 53:53/tcp -p 53:53/udp -h $NAME $IMAGE
	# docker run -itd --name $NAME -P $IMAGE # not work?
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
sudo netstat -antp | grep 53
# dig +short host1.data.com @127.0.0.1
