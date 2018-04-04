#!/bin/sh

BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

# 读取标志
result=$(set_file_flag /tmp/dns_reload)

# 清理标志
set_file_flag /tmp/dns_reload 0

echo $result

