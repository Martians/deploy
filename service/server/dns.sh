#!/bin/bash

NAME=dns
PORT="53 53/udp"
REPO=""

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

if [[ "$#" > 0 ]]; then
    docker rm -f $NAME
    docker rmi -f $IMAGE
fi
###############################################################

if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
	set -x
	docker build -t $IMAGE -f 0_server --build-arg SERVICE=$NAME \
		--build-arg LISTEN="$PORT" --build-arg REPO="$REPO" .
	set +x
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
	echo -e  "${GREEN_COLOR}-- create docker -- ${RES}"	set -x
	docker run -itd --name $NAME -p 53:53/tcp -p 53:53/udp -h $NAME $IMAGE
	set +x
	# docker run -itd --name $NAME -P $IMAGE # not work?
elif [ "`docker ps | grep $NAME$`" == "" ]; then
	echo -e  "${GREEN_COLOR}-- starting docker ... --${RES}"
	docker start $NAME
else
	echo -e  "${GREEN_COLOR}-- already started --${RES}"
fi

#echo "prepare network"
#HOST=192.168.36.27
#sudo pipework $DEVICE $NAME $HOST/$SUBNET@$GATEWAY

#echo "test dns"
sudo netstat -antp | grep 53
echo "
    dig +short host1.data.com @127.0.0.1
"
