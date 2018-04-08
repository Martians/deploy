#!/bin/bash
# config http://blog.csdn.net/field_yang/article/details/51568861

# https://hub.docker.com/r/jdeathe/centos-ssh/~/dockerfile/   supervisord
# https://hub.docker.com/r/kinogmt/centos-ssh/~/dockerfile/

# Usage: sh 2_server/base/cluster.sh [0|1] [systemd]

NAME_STUB="zookeeper"
H1=90
zoopeeker=ooo
###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

. $BASE_SERVE_PATH/cluster.sh $1 systemd
###############################################################

