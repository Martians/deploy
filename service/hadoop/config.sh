#!/bin/sh
######################################################
export NAME_HOME=/mnt/docker/name
export DATA_HOME=/mnt/docker/data

export NAME_HOST=172.20.0.10
export DATA_HOST=172.20.0.11

export DOCKER_NETWORK=hadoop-network


######################################################
export NAME_DEST=/data/hdfs/name
export NAME_DEST=/data/hdfs/data

export CLUSTER_NAME=local-hadoop
export HDFS_CONF_dfs_replication=1
export CORE_CONF_fs_defaultFS=hdfs://namenode:8020