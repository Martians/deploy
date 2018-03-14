#!/bin/bash
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/script/config.sh
#####################################################################################
<<'COMMENT'
	docker rm -f  $(docker ps -aq)
	docker rmi -f $(docker images -aq)
	docker ps -a
	docker images -a
COMMENT

<<'COMMENT'
# [ `docker images ubuntu_local -q` ] || echo "try to make image"
if [ ! `docker images ubuntu_local -q` ]; then
	docker build -t ubuntu_local -f 0_ubuntu .
	docker history ubuntu_local
	# docker tag ubuntu_local ubuntu
fi

if [ `docker images ubuntu_local -q` ]; then
	docker images *_local
fi
COMMENT

if [ ! `docker images centos:base -q` ]; then
	docker build -t centos:base -f 0_centos .
	docker history centos:base
	# docker tag centos:base centos
fi


#####################################################################################
NETWORK=$LOCAL/$SUBNET 	          

if ifconfig | grep $BRIDGE > /dev/null; then
	echo "network exist"
else
	echo "create network"
	sudo ip addr del $NETWORK dev $DEVICE; \
			sudo ip link add link $DEVICE dev $BRIDGE type macvlan mode bridge; \
			sudo ip link set $BRIDGE up; \
			sudo ip addr add $NETWORK dev $BRIDGE; \
			sudo route add default gw $GATEWAY	

	echo "clear dangling images"
	docker rmi -f $(docker images -aq -f dangling=true)
fi
# sudo pipework $DEVICE test3 192.168.36.19/$SUBNET@$GATEWAY
# sudo pipework $BRIDGE test4 192.168.36.20/$SUBNET@$GATEWAY