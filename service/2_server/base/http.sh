#!/bin/bash

NAME=http
PORT="80"
REPO="public proxy"
HOST=

###############################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

###############################################################

create_image $NAME
#create_docker


#echo "prepare network"
#HOST=192.168.36.27
#sudo pipework $DEVICE $NAME $HOST/$SUBNET@$GATEWAY

#echo "test dns"
sudo netstat -antp | grep :$PORT[\t\ ] --color
echo "brower:
    docker exec -it http /bin/bash
    http://$LOCAL:$PORT
"