#!/bin/sh

source ./base.sh $@

#docker-compose config
###############################################################
echo -e  "${GREEN_COLOR}-- start hdfs -- ${RES}"
# will also start datanode
docker-compose -f docker-compose.yaml up -d datanode 

help_config
help_host
help_hdfs


echo "  test hdfs:
	docker exec -it namenode $HDFS_TEST
	docker exec -it namenode hdfs dfs -ls /
"
sleep 2
docker exec -it namenode $HDFS_TEST
docker exec -it namenode hdfs dfs -ls /
echo