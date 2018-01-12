#!/bin/sh

source ./base.sh $@

echo -e  "${GREEN_COLOR}-- start spark -- ${RES}"
docker-compose -f docker-compose.yaml up -d spark 
    
echo "  enter host:
    docker exec -it ${PREFIX}_spark_${SUFFIX} /bin/bash
    docker run uhopper/hadoop-spark <command>
"