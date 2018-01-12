#!/bin/sh
######################################################
export NAME_HOME=/mnt/docker/name
export DATA_HOME=/mnt/docker/data

######################################################
CLUSTER_NAME=local-hadoop
HDFS_CONF_dfs_replication=1
CORE_CONF_fs_defaultFS=hdfs://namenode:8020


YARN_CONF_yarn_resourcemanager_hostname=resource
YARN_CONF_yarn_log___aggregation___enable=true
YARN_CONF_yarn_nodemanager_remote___app___log___dir=/app-logs