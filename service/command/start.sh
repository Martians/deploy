#!/bin/sh

IMAGE=centos
HOST1=192.168.36.11
HOST2=192.168.36.12

echo "remove exist host:"
docker rm -f h1 h2 
docker run -itd --name h1 --privileged=true $IMAGE 
docker run -itd --name h2 --privileged=true $IMAGE 
echo

echo "set  host address:"
sudo pipework ens33 h1 $HOST1/23@192.168.37.254
sudo pipework ens33 h2 $HOST2/23@192.168.37.254

echo "show host address:"
docker exec h1 ip addr show eth1 | grep inet
docker exec h2 ip addr show eth1 | grep inet
echo

echo "enter host:
    docker exec -it h1 /bin/bash
    docker exec -it h2 /bin/bash
"
