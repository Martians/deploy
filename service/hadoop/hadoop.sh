

# https://devops.datenkollektiv.de/apache-hadoop-setting-up-a-local-test-environment.html
# https://www.2cto.com/net/201702/595149.html

source ./config.sh

echo "start docker"
docker-compose config
#docker-compose -f docker-compose.yaml -p hadoop-local up

<<'COMMENT'
  datanode:
    env_file: ./config.sh
    image: "uhopper/hadoop-datanode"
    #container_name: datanode
    #domainname: data.com
    hostname: datanode
    networks:
      hadoop-network:
        ipv4_address: $DATA_HOST
    volumes:
      - $DATA_HOME:$NAME_DEST
    environment:
      - NOTHING
    depends_on:
      - "namenode"
      
echo "prepare network"
NETWORK=hadoop-network
docker network rm $NETWORK
docker network create --subnet=172.20.0.0/16 $NETWORK

CLUSTER="local-hadoop"
NAMENODE=namenode
DATANODE=datanode

docker rm -f $NAMENODE
docker rm -f $DATANODE

echo "start client"
CONFIG='-e "CORE_CONF_fs_defaultFS=hdfs://$NAMENODE:8020" -e "CLUSTER_NAME=$CLUSTER"'

echo "
    docker exec -it $NAMENODE /bin/bash
    docker exec -it $DATANODE /bin/bash"

docker run -it --rm --name hdfs-shell --network $NETWORK $CONFIG uhopper/hadoop:2.7.2 \
   /bin/bash

   hdfs dfs -mkdir /tmp
   hdfs dfs -put entrypoint.sh /tmp
   hdfs dfs -cat /tmp/entrypoint.sh


# -p 50070:50070 -v //c//Users//admin//hadoop//share://home//share -e "CORE_CONF_fs_defaultFS=hdfs://172.18.0.10:8082" -e "HDFS_CONF_DFS_REPLICATION=2" -e "CLUSTER_NAME=cluster0" uhopper/hadoop-namenode:latest
COMMENT