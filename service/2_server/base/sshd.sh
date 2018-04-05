#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

# Usage: sh 2_server/base/sshd.sh [0|1] [systemd]
NAME=sshd
PORT=0
REPO="public local proxy"
HOST=1

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
if [[ $1 != "systemd" && $2 != "systemd" ]]; then
	success create_docker -n $NAME -p $PORT -t $1 
else
	color_output "use systemd sshd"
	success create_docker -n $NAME -p $PORT -i centos:sshd \
	-a $(encode $SYSTMD) -e $INITIAL -t $1 
fi
###############################################################
HOST=$(alloc_host $HOST)
alloc_network $HOST

###############################################################
display_host 1