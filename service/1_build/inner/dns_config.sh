#!/bin/sh

BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

# 临时配置
insert_not_exist "server $(alloc_host DNS)" /etc/resolv.conf 

# 永久配置

