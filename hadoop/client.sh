#!/bin/sh

source ./base.sh $@

echo -e  "${GREEN_COLOR}-- start client -- ${RES}"
echo "  enter host:
    docker run -it --rm --name hdfs-shell --network $NETWORK -h hdfs-shell $CONFIG uhopper/hadoop:2.7.2 /bin/bash
"
echo "test client:"
docker run -it --rm --name hdfs-shell --network $NETWORK -h hdfs-shell $CONFIG uhopper/hadoop:2.7.2 /bin/bash