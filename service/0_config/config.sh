#!/bin/bash

# 那些主动调用config.sh的脚本，已经设置好了 BASE_PATH，此处可以直接使用
# echo "config.sh: base path - $BASE_PATH"

# 工具函数
. $BASE_PATH/0_config/utility.sh

# 加载默认配置
. $BASE_PATH/0_config/default.sh

# 加载宏设置
. $BASE_PATH/0_config/macro.sh

# 如果找到本地配置，就更新部分配置项
CONFIG_PATH=~/.docker_config
CONFIG_PATH_2=$BASE_PATH/0_config/example/config_temp.sh
#CONFIG_PATH=$BASE_PATH/0_config/example/config_desktop.sh
#CONFIG_PATH=$BASE_PATH/0_config/example/config_notebook.sh
if [ -f "$CONFIG_PATH" ]; then
	# echo "new path"
	. $CONFIG_PATH
#else
	# 不能进行这个判断，在docker image执行过程中，会调用到这里
	#	此时构建docker的用户并非是当前用户，而是 root
	#color_output "You should define you own config: $CONFIG_PATH"
	#echo "cp $BASE_PATH/0_config/example/config_desktop.sh ~/.docker_config"
	#exit 1

# 在 Docker Image执行过程中，通过此处获取配置
#	此时构建docker的用户并非是当前用户，而是 root
#	这里是在构建时新复制出来的一份，也复制到了docker的image中
#	docker运行时，因为又将脚本目录挂载到了/docker下，因此是看不到这个文件的
#	这里initialize中又复制了一份到 /root/docker_config 供后续使用
elif [ -f "$CONFIG_PATH_2" ]; then
	. $CONFIG_PATH_2
fi

MACRO_PATH=~/.docker_macro
if [ -f "$MACRO_PATH" ]; then
	# echo "new path"
	. $MACRO_PATH
fi

# 赋值依赖于其他宏，最后进行设置
. $BASE_PATH/0_config/depend.sh

. $BASE_PATH/1_build/handle.sh

## 测试
# echo "local: "
# echo "	Host: $HOST_LOCAL, device: $DEVICE"
# echo "	subnet: $NETMASK, gateway: $GATEWAY, mask: $SUBNET"
# echo "	domain: $DOMAIN"

# echo "alloc:"
# echo "	Host1: $(alloc_host 1)"
# echo "	Test: $(alloc_host TEST)"
# echo " 	DB: $(alloc_host DB)"

# echo "server: "
# echo "	http:  $HOST_REPO, dir: $HOST_PATH_REPO, dst: $DOCK_PATH_REPO"
# echo "	proxy: $HOST_REPO, dir: $HOST_PATH_PROXY"

# echo "macro: "
# echo "	global: $GLOBAL_MACRO"
