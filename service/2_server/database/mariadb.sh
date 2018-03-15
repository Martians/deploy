#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# http://blog.csdn.net/luckytanggu/article/details/71514798

NAME=mariadb
REPO="public local proxy"
PORT="0"
HOST=DB

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
HOST=$(alloc_host $HOST)
alloc_network $HOST

###############################################################
script=$DOCK_BASE_PATH/$BUILD_PATH/database/mariadb.sh
echo "@@@@@@@@ exec $NAME host: $script"
docker exec -it $NAME $script

###############################################################
display_host

echo "@@@@@@@@ enter host @@@@@@@@@"
docker exec -it $NAME /bin/bash
