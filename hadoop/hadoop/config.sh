#!/bin/sh

######################################################
# only export, they can be used in docker-compose.yaml
export NAME_HOME=/mnt/docker/name
export DATA_HOME=/mnt/docker/data

export NETWORK=hadoop
export CLUSTER_NAME=local-hadoop

######################################################
# no need export, they can used as env inside docker
HDFS_CONF_dfs_replication=1
HDFS_CONF_dfs_permissions_enabled=false
CORE_CONF_fs_defaultFS=hdfs://namenode:8020

CORE_CONF_hadoop_proxyuser_root_groups=*
CORE_CONF_hadoop_proxyuser_root_hosts=*
CORE_CONF_nfs_superuser=root
NFS_MOUNT=/mnt/hdfs

YARN_CONF_yarn_resourcemanager_hostname=resource
YARN_CONF_yarn_log___aggregation___enable=true
YARN_CONF_yarn_nodemanager_remote___app___log___dir=/app-logs


######################################################
## client test command
CLIENT_CONFIG="-e CORE_CONF_fs_defaultFS=$CORE_CONF_fs_defaultFS"
CLIENT_INFO="--name hdfs-shell -h hdfs-shell --network $NETWORK"

export HADOOP_BASE=/opt/hadoop-2.7.2

HDFS_TEST="hdfs dfs -mkdir -p /test"
HDFS_CHECK="hdfs dfs -ls /"

YARN_CLIENT="-e YARN_CONF_yarn_resourcemanager_hostname=resource \
    -e YARN_CONF_yarn_log___aggregation___enable=true \
    -e YARN_CONF_yarn_nodemanager_remote___app___log___dir=/app-logs"
YARN_PREPARE="hadoop fs -rm -r /output"
YARN_EXAMPLE="hadoop jar $HADOOP_BASE/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.2.jar wordcount file://$HADOOP_BASE/etc/hadoop/hadoop-env.sh /output"
