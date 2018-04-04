#!/bin/sh

BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

A_RECORD="$1   IN   A   $2"
insert_not_exist "$A_RECORD" /var/named/$DOMAIN
result1=$?

X_RECORD="$(host_reverse $2)       IN   PTR  $1.$DOMAIN."
insert_not_exist "$X_RECORD" /var/named/$DOMAIN.arpa
result2=$?

# 任何一个发生了改变，都需要更新dns配置
if (( $result1 == 0 || $result1 == 0 )); then
	# 向文件中写入执行标志
	set_file_flag /tmp/dns_reload 1
fi