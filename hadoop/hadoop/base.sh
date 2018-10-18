#!/bin/sh
# https://devops.datenkollektiv.de/apache-hadoop-setting-up-a-local-test-environment.html
# https://www.2cto.com/net/201702/595149.html

source ./config.sh

GREEN_COLOR='\E[1;32m'
RES='\E[0m'

######################################################
## establis
# sh remove.sh && sh hdfs.sh && sh nfs3.sh 

## check network config: 
# docker inspect --format='{{json .NetworkSettings.Networks}}' namenode

###############################################################
## network
if [ "`docker network ls | grep $NETWORK`" = "" ]; then
  echo "prepare network"
  #docker network rm $NETWORK
  set -x
  docker network create --subnet=172.20.0.0/16 $NETWORK
  set +x
fi

# use remove.sh now
# if [[ "$1" == "inner" ]]; then
#     inner=1
# elif [[ "$#" > 0 ]]; then
#     #docker rm -f namenode
#     #docker rm -f datanode
#     docker-compose stop
#     docker-compose down    
# fi

######################################################
## help
help_config() {
  echo "  check config:
    docker exec -it namenode cat /etc/hadoop/hdfs-site.xml 
    docker exec -it namenode sh -c 'echo \$HDFS_CONF_dfs_replication'
"
}

help_host() {
  echo "  enter host:
    docker exec -it namenode /bin/bash
    docker exec -it datanode /bin/bash
"
  echo "  new client:
    docker run -it --rm $CLIENT_INFO $CLIENT_CONFIG uhopper/hadoop:2.7.2 /bin/bash
"
}

help_hdfs() {
  echo "  hdfs test:
    docker exec -it namenode /bin/bash
    docker exec -it namenode hdfs dfs -ls /

    hdfs dfs -ls /
    hdfs dfs -mkdir /tmp
    hdfs dfs -put entrypoint.sh /tmp
    hdfs dfs -cat /tmp/entrypoint.sh
"
}

help_client() {
  echo -e  "${GREEN_COLOR}-- start client -- ${RES}"

  echo "  enter host:
    docker run -it --rm $CLIENT_INFO $CLIENT_CONFIG uhopper/hadoop:2.7.2 /bin/bash
    $YARN_PREPARE; $YARN_EXAMPLE
"
}

help_mapr() {
  echo " mapreduce:
    hadoop fs -rm -r /ootput; hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar wordcount file://$HADOOP_HOME/etc/hadoop/hadoop-env.sh /output

    # core-site.xml
    <property><name>fs.defaultFS</name><value>hdfs://namenode:8020</value></property>

    # yarn-site.xml
    <property><name>yarn.resourcemanager.hostname</name><value>resource</value></property>
"
}
