#!/bin/sh


NAME=dns
HOST=192.168.36.27

IMAGE=centos_$NAME
docker rm -f $NAME
docker rmi -f $IMAGE

echo "create image"
docker build -t $IMAGE -f 0_centos --build-arg SERVICE=$NAME .

echo "start docker"
docker run -itd --name $NAME $IMAGE

echo "prepare network"
sudo pipework ens33 $NAME $HOST/23@192.168.37.254
#/docker/server/dns.sh

echo "test dns"
# dig host1.data.com @$HOST