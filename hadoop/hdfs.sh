#!/bin/sh

# https://devops.datenkollektiv.de/apache-hadoop-setting-up-a-local-test-environment.html
# https://www.2cto.com/net/201702/595149.html

source ./base.sh $@

#docker-compose config
###############################################################
echo -e  "${GREEN_COLOR}-- start hdfs -- ${RES}"
docker-compose -f docker-compose.yaml up -d datanode 

echo "  enter host:
    docker exec -it ${PREFIX}_namenode_${SUFFIX} /bin/bash
    docker exec -it ${PREFIX}_datanode_${SUFFIX} /bin/bash
    docker run -it --rm --name hdfs-shell --network $NETWORK $CONFIG uhopper/hadoop:2.7.2 /bin/bash
"
echo "  hdfs test:
    hdfs dfs -ls /
    hdfs dfs -mkdir /tmp
    hdfs dfs -put entrypoint.sh /tmp
    hdfs dfs -cat /tmp/entrypoint.sh
"
echo "test client:"
docker run -it --rm --name hdfs-shell --network $NETWORK $CONFIG uhopper/hadoop:2.7.2 \
/opt/hadoop-2.7.2/bin/hdfs dfs -ls /

echo