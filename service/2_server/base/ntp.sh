#!/bin/bash

NAME=ntp
PORT="0"
REPO="public"
HOST=

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

###############################################################

# 确保必须的镜像已经安装好
create_prepare

# 创建镜像
success create_image  -n $NAME -r $(encode $REPO) -p $PORT -t $1

# 创建容器
ARGS="-p 123:123/udp"
success create_docker -n $NAME -p $PORT -a $(encode $ARGS) -t $1 
###############################################################
display_state
