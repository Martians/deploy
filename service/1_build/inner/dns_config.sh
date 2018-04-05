#!/bin/sh

BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

CONFIG="nameserver $(alloc_host DNS)"
DEST=/etc/resolv.conf
if grep -q "$CONFIG" $DEST; then
	# echo "already configed"
	exit
fi

# 临时配置
#	必须加到第一个dns的位置，否则无法生效？
# 	无法使用，会创建新文件：sed -i "1i\nameserver $(alloc_host DNS)/" /etc/resolv.conf 
exist="$(cat /etc/resolv.conf)"
echo "$CONFIG" > /etc/resolv.conf 
echo "$exist" >> /etc/resolv.conf 

# 永久配置
#	没有找到可以写入的配置文件

