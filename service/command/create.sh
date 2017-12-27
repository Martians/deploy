#!/bin/sh
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

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
	docker tag ubuntu_local ubuntu
fi

if [ `docker images ubuntu_local -q` ]; then
	docker images *_local
fi
COMMENT

if [ ! `docker images centos_local -q` ]; then
	docker build -t centos_local -f 0_base .
	docker history centos_local
	docker tag centos_local centos
fi


#####################################################################################
BRIDGE=eth0m                        # 新增网桥
DEVICE=ens33                        # 实际网卡
NETWORK=192.168.36.10/23            # host实际ip
GATE=192.168.37.254

if ifconfig | grep $BRIDGE > /dev/null; then
	echo "network exist"
else
	echo "create network"
	sudo ip addr del $NETWORK dev $DEVICE; \
			sudo ip link add link $DEVICE dev $BRIDGE type macvlan mode bridge; \
			sudo ip link set $BRIDGE up; \
			sudo ip addr add $NETWORK dev $BRIDGE; \
			sudo route add default gw $GATE	
fi
# sudo pipework ens33  test3 192.168.36.19/23@192.168.37.254  
# sudo pipework $BRIDGE test4 192.168.36.20/23@192.168.37.254 