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

# 执行修改/etc/hosts的脚本，将cluster中的host都加进去
script=$DOCK_BASE_PATH/$BUILD_PATH/server/cluster.sh

# 创建容器
for ((idx = 1; idx <= 3; idx++)); do
	
	success create_docker -n $NAME-$idx -p $PORT -t $1
	docker exec $NAME-$idx $script

	HOSTS=$(alloc_host $idx)
	alloc_network $HOSTS $NAME-$idx

	# 添加dns到dns server
	dns_add $NAME-$idx $HOSTS

	# 配置docker内部的dns服务器
	dns_config $NAME-$idx
done

# 检查是否需要重启
dns_reload

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

# 预先安装dns server
# dns_reload没有生效
# docker 内部的dns服务器，需要修改为最多三个dns