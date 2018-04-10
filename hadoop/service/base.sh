#!/bin/sh
# https://devops.datenkollektiv.de/apache-hadoop-setting-up-a-local-test-environment.html
# https://www.2cto.com/net/201702/595149.html

source ./config.sh

PREFIX=hadoop
SUFFIX=1
NETWORK=hadoop-network

GREEN_COLOR='\E[1;32m'
RES='\E[0m'

CLIENT_CONFIG="-e CORE_CONF_fs_defaultFS=hdfs://namenode:8020 -e CLUSTER_NAME=$CLUSTER_NAME"
CLIENT_INFO="--name hdfs-shell -h hdfs-shell --network $NETWORK"

HADOOP_BASE=/opt/hadoop-2.7.2
HDFS_EXAMPLE="$HADOOP_BASE/bin/hdfs dfs -ls /"
YARN_CLIENT="-e YARN_CONF_yarn_resourcemanager_hostname=resource \
    -e YARN_CONF_yarn_log___aggregation___enable=true \
    -e YARN_CONF_yarn_nodemanager_remote___app___log___dir=/app-logs"
YARN_PREPARE="hadoop fs -rm -r /output"
YARN_EXAMPLE="hadoop jar $HADOOP_BASE/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.2.jar wordcount file://$HADOOP_BASE/etc/hadoop/hadoop-env.sh /output"
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
