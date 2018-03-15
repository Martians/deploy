#!/bin/bash

NAME=generate
PORT="808"
REPO="public local proxy"

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

###############################################################

# 确保必须的镜像已经安装好
create_prepare sshd

# 创建容器
success create_docker -n $NAME -p $PORT -i centos:sshd \
	-a $(encode $SYSTMD) -e $INITIAL -t $1 

###############################################################
script=$DOCK_BASE_PATH/$BUILD_PATH/database/generate.sh
echo "@@@@@@@@ exec $NAME host: $script"
docker exec -it $NAME $script

###############################################################
display_brower