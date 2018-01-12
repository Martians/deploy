#!/bin/sh

source ./config.sh

PREFIX=hadoop
SUFFIX=1
NETWORK=hadoop-network

GREEN_COLOR='\E[1;32m'
RES='\E[0m'
CLIENT_CONFIG="-e CORE_CONF_fs_defaultFS=hdfs://namenode:8020 -e CLUSTER_NAME=$CLUSTER_NAME"

###############################################################
if [ "`docker network ls | grep $NETWORK`" = "" ]; then
  echo "prepare network"
  #docker network rm $NETWORK
  set -x
  docker network create --subnet=172.20.0.0/16 $NETWORK
  set +x
fi

if [[ "$1" == "inner" ]]; then
    inner=1
elif [[ "$#" > 0 ]]; then
    #docker rm -f namenode
    #docker rm -f datanode
    docker-compose stop
    docker-compose down    
fi
