#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

# Usage: sh 2_server/base/sshd.sh [0|1] [systemd]
NAME=sshd
PORT=0
REPO="public local proxy"
HOST=5

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

###############################################################

# 将本文件当成一个模板，其他可以调用
# 	担心该方法容易出错，没有使用，有点复杂：会调用的地方：
# 	1）将其作为模板调用 2）其他服务依赖于sshd的 3）依赖，并要将sshd作为模板的
	# 可以在外部定义STUB变量，来覆盖这里的定义
	# NAME=$(default_value $NAME_STUB sshd)
	# PORT=$(default_value $PORT_STUB 0)
	# HOST=$(default_value $HOST_STUB 1)
	# REPO="$(default_value $REPO_STUB "public local proxy")"

	# echo "=============================="
	# echo "sshd: name: $NAME, REPO: $REPO"
###############################################################

# 确保必须的镜像已经安装好
create_prepare

# 创建镜像，这里镜像的名字，改成sshd，而不是$NAME (否则，如果将sshd当做模板，这里会出错)
success create_image -n sshd -r $(encode $REPO) -p $PORT -t $1

# 创建容器
if [[ $1 != "systemd" && $2 != "systemd" ]]; then
	success create_docker -n $NAME -p $PORT -t $1 
else
	color_output "use systemd sshd"
	success create_docker -n $NAME -p $PORT -i centos:sshd \
	-a $(encode $SYSTMD) -e $INITIAL -t $1 
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