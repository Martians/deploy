#!/bin/sh

source ./base.sh $@

echo -e  "${GREEN_COLOR}-- start yarn -- ${RES}"
docker-compose -f docker-compose.yaml up -d nodemanager 

echo "  enter host:
    docker exec -it ${PREFIX}_resource_${SUFFIX} /bin/bash
    docker exec -it ${PREFIX}_nodemanager_${SUFFIX} /bin/bash
    $YARN_EXAMPLE
"