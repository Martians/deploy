#!/bin/bash

NAME=proxy
PORT=3142
#REPO="public local"
REPO=""

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

# if [ ! -n "$HOST_PATH_PROXY" -o ! -d "$HOST_PATH_PROXY" ]; then
#     HOST_PATH_PROXY=~/proxy
# fi

###############################################################
# 创建 proxy镜像
create_proxy -t $1

ARGS="-v $HOST_PATH_PROXY:$DOCK_PATH_PROXY"
success create_docker -n $NAME -p $PORT -a $(encode $ARGS) -t $1 

###############################################################
display_brower

echo "check state:
    docker exec proxy du -ch --max-depth=1 /var/cache/apt-cacher-ng
    docker logs -f proxy 
"
