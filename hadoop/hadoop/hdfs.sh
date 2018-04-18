#!/bin/sh

source ./base.sh $@

#docker-compose config
###############################################################
echo -e  "${GREEN_COLOR}-- start hdfs -- ${RES}"
docker-compose -f docker-compose.yaml up -d datanode 

echo "  enter host:
    docker exec -it ${PREFIX}_namenode_${SUFFIX} /bin/bash
    docker exec -it ${PREFIX}_datanode_${SUFFIX} /bin/bash
    docker run -it --rm $CLIENT_INFO $CLIENT_CONFIG uhopper/hadoop:2.7.2 /bin/bash
"
echo "  hdfs test:
    hdfs dfs -ls /
    hdfs dfs -mkdir /tmp
    hdfs dfs -put entrypoint.sh /tmp
    hdfs dfs -cat /tmp/entrypoint.sh
"
echo "test client:"
docker run -it --rm $CLIENT_INFO $CLIENT_CONFIG uhopper/hadoop:2.7.2 $HDFS_EXAMPLE
echo