#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

###############################################################
# Usage: sh 2_server/base/cluster.sh [0|1] [systemd]
NAME=$(default_value $NAME_STUB sshd)
PORT=$(default_value $PORT_STUB 0)
HOST=$(default_value $HOST_STUB 1)
REPO="$(default_value $REPO_STUB "public local proxy")"
COUNT="$(default_value $COUNT_STUB 3)"

# 配置dns、ntp(但docker中ntp client无法无法生效)
CONFIG="$(default_value $CONFIGIG_STUB dns)"


# 如果需要额外参数，只需要如此设置
MORE="-v /mnt/hgfs/local/testing:/testing"
###############################################################
# 确保必须的镜像已经安装好
create_prepare

# 创建镜像, 使用sshd而不是$NAME
success create_image -n sshd -r $(encode $REPO) -p $PORT -t $1

# 执行修改/etc/hosts的脚本，将cluster中的host都加进去
script=$DOCK_BASE_PATH/$BUILD_PATH/server/cluster.sh

# 创建容器
for ((idx = 1; idx <= $COUNT; idx++)); do
	###########################################################################
	# 是否使用sysmted来启动	
	if [[ $1 != "systemd" && $2 != "systemd" ]]; then
		success create_docker -n $NAME-$idx -p $PORT -t $1
	else
		color_output "use systemd sshd"
		success create_docker -n $NAME-$idx -p $PORT -i centos:sshd \
			-a $(encode $SYSTMD) -e $INITIAL -t $1
	fi
	docker exec $NAME-$idx $script

	###########################################################################
	# 根据已经配置的宏，分配IP地址
	HOSTS=$(alloc_cluster_host $NAME $idx)
	alloc_network $HOSTS $NAME-$idx

	# 添加dns到dns server
	create_prepare $CONFIG

	###########################################################################
	# 需要配置dns服务器
	if [ $(string_exist "$CONFIG" dns) -eq 0 ]; then
		dns_add $NAME-$idx $HOSTS

		# 配置docker内部的dns服务器
		dns_config $NAME-$idx
	fi

	# 需要配置 ntp 服务器
	if [ $(string_exist "$CONFIG" ntp) -eq 0 ]; then
		ntp_config $NAME-$idx
	fi
done

if [ $(string_exist "$CONFIG" dns) -eq 0 ]; then
	# 检查是否需要重启
	dns_reload
fi

###############################################################
# 没有配置NAME_STUB，就直接显示；否则取消显示
if [[ $NAME_STUB == "" ]]; then
	display_cluster $NAME $COUNT
fi

# client内部测试
# yum install -y bind-utils

# docker 内部的dns服务器，需要修改为最多三个dns