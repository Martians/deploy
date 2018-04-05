#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

# Usage: sh 2_server/base/cluster.sh [0|1] [systemd]
NAME=sshd
PORT=0
REPO="public local proxy"
COUNT=5

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

###############################################################

# 确保必须的镜像已经安装好
create_prepare

# 创建镜像
success create_image -n $NAME -r $(encode $REPO) -p $PORT -t $1

# 执行修改/etc/hosts的脚本，将cluster中的host都加进去
script=$DOCK_BASE_PATH/$BUILD_PATH/server/cluster.sh

# 创建容器
for ((idx = 1; idx <= $COUNT; idx++)); do
	# 是否使用sysmted来启动	
	if [[ $1 != "systemd" && $2 != "systemd" ]]; then
		success create_docker -n $NAME-$idx -p $PORT -t $1
	else
		color_output "use systemd sshd"
		success create_docker -n $NAME-$idx -p $PORT -i centos:sshd \
			-a $(encode $SYSTMD) -e $INITIAL -t $1
	fi
	docker exec $NAME-$idx $script

	HOSTS=$(alloc_host $idx)
	alloc_network $HOSTS $NAME-$idx

	# 添加dns到dns server
	create_prepare dns
	dns_add $NAME-$idx $HOSTS

	# 配置docker内部的dns服务器
	dns_config $NAME-$idx
done

# 检查是否需要重启
dns_reload

###############################################################

# docker 内部，网卡名称是 eth1
echo "try start with last param [systemd]"
echo "show host address:"
for ((idx = 1; idx <= $COUNT; idx++)); do
	docker exec $NAME-$idx ip addr show eth1 | grep inet | grep [0-9.].*/ --color
done

echo "    docker exec $NAME-1 ping $NAME-2"
echo "enter host:"
for ((idx = 1; idx <= $COUNT; idx++)); do
	echo "    ssh root@$(alloc_host $idx)"
done

# client内部测试
# yum install -y bind-utils

# docker 内部的dns服务器，需要修改为最多三个dns