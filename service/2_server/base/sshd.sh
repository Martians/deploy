#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

NAME=sshd
PORT=22
REPO="public local proxy"
# 1_HOST
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
success create_docker -n $NAME -p $PORT -t $1 

###############################################################
alloc_network $HOST

echo "clean cache:
    rm ~/.ssh/known_hosts -f
or,
    echo "StrictHostKeyChecking=no" > ~/.ssh/config
    echo "UserKnownHostsFile=/dev/null" >> ~/.ssh/config
"

# docker 内部，网卡名称是 eth1
echo "show host address:"
docker exec $NAME ip addr show eth1 | grep inet | grep [0-9.]*/ --color
echo

echo "enter host:
    docker exec -it $NAME /bin/bash
    ssh root@$HOST
"
