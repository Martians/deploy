

# https://devops.datenkollektiv.de/apache-hadoop-setting-up-a-local-test-environment.html
# https://www.2cto.com/net/201702/595149.html

source ./config.sh

#docker-compose config
NETWORK=hadoop-network

if [ ! `docker network ls | grep $NETWORK -q` ]; then
  echo "prepare network"
  #docker network rm $NETWORK
  set -x
  docker network create --subnet=172.20.0.0/16 $NETWORK
  set +x
fi

if [[ "$#" > 0 ]]; then
    #docker rm -f namenode
    #docker rm -f datanode
    docker-compose down    
fi

###############################################################
echo "start docker"
docker-compose -f docker-compose.yaml  up -d
    
echo "start client"
CONFIG="-e CORE_CONF_fs_defaultFS=hdfs://namenode:8020 -e CLUSTER_NAME=$CLUSTER_NAME"

echo "  enter host:
    docker exec -it namenode /bin/bash
    docker exec -it datanode /bin/bash
    docker exec -it resource /bin/bash
    docker exec -it nodemanager /bin/bash
    docker run -it --rm --name hdfs-shell --network $NETWORK $CONFIG uhopper/hadoop:2.7.2 /bin/bash
"
echo "  hdfs test:
    hdfs dfs -ls /
    hdfs dfs -mkdir /tmp
    hdfs dfs -put entrypoint.sh /tmp
    hdfs dfs -cat /tmp/entrypoint.sh
"

echo "enter client:"
docker run -it --rm --name hdfs-shell --network $NETWORK $CONFIG uhopper/hadoop:2.7.2 \
  /opt/hadoop-2.7.2/bin/hdfs dfs -ls /