#!/bin/sh

source ./base.sh $@

echo -e  "${GREEN_COLOR}-- start client -- ${RES}"
echo "  enter host:
    docker run -it --rm $CLIENT_INFO $CLIENT_CONFIG uhopper/hadoop:2.7.2 /bin/bash
    $YARN_PREPARE; $YARN_EXAMPLE
"
echo "test client:"
docker run -it --rm $CLIENT_INFO $CLIENT_CONFIG $YARN_CLIENT uhopper/hadoop:2.7.2 /bin/bash

echo "
    hadoop fs -rm -r /ootput; hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.3.jar wordcount file://$HADOOP_HOME/etc/hadoop/hadoop-env.sh /output

    # core-site.xml
    <property><name>fs.defaultFS</name><value>hdfs://namenode:8020</value></property>

    # yarn-site.xml
    <property><name>yarn.resourcemanager.hostname</name><value>resource</value></property>
# 