#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

# Usage: sh 2_server/base/cluster.sh [0|1] [systemd]

# 配置IP的说明
# 1）配置宏：zookeeper-1、H1
# 2）解析宏：H1=192.168.10.19；H1=29(分配IP：192.168.$SEGMENT.(29-%HOST_1))
NAME_STUB="zookeeper"
H1=97
H2=98
H3=99

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

. $BASE_SERVE_PATH/cluster.sh $1 systemd
###############################################################

