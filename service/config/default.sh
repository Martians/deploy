#!/bin/bash

#############################################################################
## Local Network
DEVICE=ens33

LOCAL=192.168.36.10
NETMASK=255.255.254.0
GATEWAY=192.168.37.254
SUBNET=23

#############################################################################
## Alloc Network

# 两种方式配置地址
# echo $(alloc_host 1)
# echo $(alloc_host DB)
SEGMENT=192.168.36
# 方式1：SEGMENT + SUFFIX
	HOST_1=11
	HOST_2=12

	HOST_TEST=99
	HOST_DB=91

# 方式2：保持该IP地址不变
	HOST_EXAMPLE=192.168.36.88

	# 根据类似于枚举的值，解析host的地址
	#	给出的枚举是：1 2 TEST DB
	#	大小写匹配
	alloc_host () {
		data=`dyn_var HOST_$1`
		# 判断是否包含 .
		if [[ $data =~ "." ]]; then
			echo "$data"
		else
			echo "$SEGMENT.$data"
		fi
	}


#############################################################################
#### 相对固定

BRIDGE=eth0m
DOMAIN="data.com"
#############################################################################
# HTTP docker 里边，对应的数据目录
REPO_DST=/html

#############################################################################
## Directory
REPO_SRC=/mnt/repo
PROXY_SRC=/mnt/proxy