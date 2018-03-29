#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

NAME=sshd
PORT=0
REPO="public local proxy"

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
success create_docker -n $NAME-1 -p $PORT -t $1
success create_docker -n $NAME-2 -p $PORT -t $1
success create_docker -n $NAME-3 -p $PORT -t $1

###############################################################
HOST1=$(alloc_host 1)
alloc_network $HOST1 $NAME-1

HOST2=$(alloc_host 2)
alloc_network $HOST2 $NAME-2

HOST3=$(alloc_host 3)
alloc_network $HOST3 $NAME-3

###############################################################

# docker 内部，网卡名称是 eth1
echo "show host address:"
docker exec $NAME-1 ip addr show eth1 | grep inet | grep [0-9.].*/ --color
docker exec $NAME-2 ip addr show eth1 | grep inet | grep [0-9.].*/ --color
docker exec $NAME-3 ip addr show eth1 | grep inet | grep [0-9.].*/ --color

echo "enter host:
    ssh root@$HOST1
    ssh root@$HOST2
    ssh root@$HOST3
"