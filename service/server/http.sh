#!/bin/sh

NAME=http
PORT="80"
REPO=""

###############################################################
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/command/create.sh
source $BASE/script/config.sh
IMAGE=centos:$NAME

# if repo not define, or define but not exist
if [ $REPO_SRC -a ! -d $REPO_SRC ]; then
	REPO_SRC=/var/log
fi

<<'COMMENT'
docker rm -f $NAME
docker rmi -f $IMAGE
COMMENT

###############################################################

if [ ! `docker images $IMAGE -q` ]; then
	echo "create image"
	docker build -t $IMAGE -f 0_centos --build-arg SERVICE=$NAME \
		--build-arg LISTEN="$PORT" --build-arg REPO="$REPO" .
fi

# check if docker ps output end with $NAME
if [ "`docker ps -a | grep $NAME$`" == "" ]; then
	echo "create docker"
	docker run -itd --name $NAME -h $NAME -v $REPO_SRC:$REPO_DST -p $PORT:$PORT $IMAGE
	# docker run -itd --name $NAME -h $NAME -v $REPO_SRC:/html -P $IMAGE
	
elif [ "`docker ps | grep $NAME$`" == "" ]; then
	echo "start docker"
	docker start $NAME
else
	echo "start already"
fi

#echo "prepare network"
#HOST=192.168.36.27
#sudo pipework $DEVICE $NAME $HOST/$SUBNET@$GATEWAY

#echo "test dns"
sudo netstat -antp | grep :$PORT[\t\ ] --color
echo "brower:
    http://$LOCAL:$PORT
"