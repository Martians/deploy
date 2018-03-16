#!/bin/bash

###############################################################
NAME=systemd
SSHD=5555
PORT="-p $SSHD:22 -p 3306:3306"

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; pwd)
cd $BASE_PATH

IMAGE=centos:host
ARGS="-v $(pwd):/docker"

EXEC=/usr/sbin/init
SYSTMD="--privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup"

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
	docker run -itd --name $NAME -h $NAME $PORT $ARGS $SYSTMD $IMAGE $EXEC
	# docker run -itd --name $NAME -h $NAME -v $HOST_PATH_REPO:/html -P $IMAGE
	set +x

elif [[ `docker ps | grep "$NAME$"` == "" ]]; then
	echo "starting docker $NAME ..."
	docker start $NAME

else
	echo "already started"
fi

###############################################################
script=/docker/server/mariadb.sh
echo "@@@@@@@@ exec $NAME: $script"
docker exec -it $NAME $script

###############################################################
echo "enter host: (root:111111)
    docker exec -it $NAME /bin/bash
    ssh -p$SSHD root@localhost    	
"

echo "@@@@@@@@ enter host @@@@@@@@@"
docker exec -it $NAME /bin/bash