#!/bin/bash

#############################################################################
## Local Network
DEVICE=ens33

HOST_LOCAL=192.168.10.10
NETMASK=255.255.254.0
GATEWAY=192.168.10.254
SUBNET=23

#############################################################################
## Alloc Network

# 两种方式配置地址
# echo $(alloc_host 1)
# echo $(alloc_host DB)
SEGMENT=192.168.10
# 方式1：SEGMENT + SUFFIX
	HOST_1=11
	HOST_2=12
	HOST_3=13

	HOST_TEST=99
	HOST_DB=91

# 方式2：保持该IP地址不变
	HOST_EXAMPLE=192.168.10.88

	# 根据类似于枚举的值，解析host的地址
	#	给出的枚举是：1 2 TEST DB
	#	大小写匹配
	alloc_host () {
		data=`dyn_var HOST_$1`

		# 判断是否包含 .
		if [[ $data =~ "." ]]; then
			echo "$data"
		
		# 有相应的 HOST_$1 变量，与 SEGMENT 做拼接
		elif [[ $data != "" ]]; then
			echo "$SEGMENT.$data"
		
		# 没有相应的 HOST_$1 变量
		else
			# 传入的是一个数字，最后一位取相对于HOST_1的大小
			#	如：$(alloc_host 5) 计算得到 15
			#	这样即使没有进行很多配置，可以自动得到IP信息
			if [ "$1" -gt 0 ] 2>/dev/null ;then 
				(( value = $HOST_1 + ($1 - 1) ))
				echo "$SEGMENT.$value"
			else
				echo "nothing"
			fi
		fi
	}


#############################################################################
#### 相对固定

# 此项必须进行设置，否则会使用默认值
#	public local(NAT source) proxy file
REPO_MASK="public local proxy"


BRIDGE=eth0m
DOMAIN="data.com"
HOST_DNS_PUBLIC=
#############################################################################
# HTTP docker 里边，对应的数据目录
DOCK_PATH_REPO=/html
DOCK_PATH_PROXY=/var/cache/apt-cacher-ng

#############################################################################
## Directory
HOST_PATH_REPO=/mnt/repo
HOST_PATH_PROXY=/mnt/proxy


#############################################################################
## 无需覆盖的配置

# 使用 origin（原生），或者base（经过改进的基础班）
#	影响 0_Server 模板，和Initializer脚本
USING_BASE=1

BUILD_PATH=1_build
IMAGE_PATH=template
BASE_SERVE_PATH=2_server/base


# 在docker内部，获取脚本的根路径
DOCK_BASE_PATH=/docker/service

# 存放docker内部执行的命令
DOCK_INNER_PATH=$DOCK_BASE_PATH/$BUILD_PATH/inner