#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

# Usage: sh 2_server/base/sshd.sh [0|1] [systemd]
NAME=ubuntu
PORT=0
HOST=1

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

###############################################################
# 创建镜像，这里镜像的名字，改成sshd，而不是$NAME (否则，如果将sshd当做模板，这里会出错)
create_origin -p 0_ubuntu -i ubuntu:base -e "ubuntu/ssh.sh" -t $1

# 创建容器
if [[ $1 != "systemd" && $2 != "systemd" ]]; then
	success create_docker -i ubuntu:base -n $NAME -p $PORT -t $1 
else
	color_output "use systemd sshd"
	success create_docker -n $NAME -p $PORT -i ubuntu:base \
	-a $(encode $SYSTMD) -e $UBUNTU_INIT -t $1 
fi

###############################################################
# # 如果不是使用stub模式，就输出sshd的展示信息
# if [[ $NAME_STUB == "" ]]; then
HOST=$(alloc_host $HOST)
alloc_network $HOST

###############################################################
echo
echo "try start with last param [systemd]"
display_host 1
# fi