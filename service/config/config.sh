#!/bin/bash

# 工具函数
. ./utility.sh

# 加载默认配置
. ./default.sh

# 加载宏设置
. ./macro.sh

# 如果找到本地配置，就更新部分配置项
#CONFIG_PATH=~/.docker_config
CONFIG_PATH=./example/config_desktop.sh
CONFIG_PATH=./example/config_notebook.sh
if [ -f "$CONFIG_PATH" ]; then
	# echo "new path"
	. $CONFIG_PATH
fi

MACRO_PATH=~/.docker_macro
if [ -f "$MACRO_PATH" ]; then
	# echo "new path"
	. $MACRO_PATH
fi

# 赋值依赖于其他宏，最后进行设置
. ./depend.sh




## 测试
echo "local: "
echo "	Host: $LOCAL, device: $DEVICE"
echo "	subnet: $NETMASK, gateway: $GATEWAY, mask: $SUBNET"
echo "	domain: $DOMAIN"

echo "alloc:"
echo "	Host1: $(alloc_host 1)"
echo "	Test: $(alloc_host TEST)"
echo " 	DB: $(alloc_host DB)"

echo "server: "
echo "	http:  $REPO_HOST, dir: $REPO_SRC, dst: $REPO_DST"
echo "	proxy: $REPO_HOST, dir: $PROXY_SRC"

echo "macro: "
echo "	global: $GLOBAL_MACRO"
