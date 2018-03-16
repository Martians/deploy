#!/bin/bash

###############################################################
NAME=host
SSHD=2222
PORT="-p $SSHD:22"

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; pwd)
cd $BASE_PATH

IMAGE=centos:host
ARGS="-v $(pwd):/docker"
EXEC=

###############################################################
# 数据清理
if [[ "$1" == 1 ]]; then
	docker rm  -f $NAME
	docker rmi -f $IMAGE

elif [[ "$1" == 0 ]]; then
	docker rm  -f $NAME
fi

###############################################################
# 创建镜像
if [ ! `docker images $IMAGE -q` ]; then
	echo "create image for $NAME"

	set -x
	docker build -t $IMAGE -f build/ssh_centos .
	set +x
fi

###############################################################
# 创建容器
if [[ `docker ps -a | grep "$NAME$"` == "" ]]; then
	echo "create docker $NAME"

	set -x
	docker run -itd --name $NAME -h $NAME $PORT $ARGS $IMAGE $EXEC
	# docker run -itd --name $NAME -h $NAME -v $HOST_PATH_REPO:/html -P $IMAGE
	set +x

elif [[ `docker ps | grep "$NAME$"` == "" ]]; then
	echo "starting docker $NAME ..."
	docker start $NAME

else
	echo "already started"
fi

###############################################################
echo "enter host: (root:111111)
    docker exec -it $NAME /bin/bash
    ssh -p$SSHD root@localhost    	
"

# echo "@@@@@@@@ enter host @@@@@@@@@"
# docker exec -it $NAME /bin/bash