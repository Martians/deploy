#!/bin/sh

source ./base.sh $@

#docker-compose config
###############################################################
echo -e  "${GREEN_COLOR}-- remove -- ${RES}"
# will also start datanode
docker-compose -f docker-compose.yaml down
sudo rm $NAME_HOME -rf
sudo rm $DATA_HOME -rf