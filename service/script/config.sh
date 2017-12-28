#!/bin/sh

TYPE="desktop"
TYPE="notebook"

#<<'COMMENT'
#COMMENT

# repo setting
#############################################################################
DOMAIN="data.com"
BRIDGE=eth0m
SUBNET=24

#############################################################################
if [ $TYPE = "desktop" ]; then
	DEVICE=ens33

	LOCAL=192.168.36.10
	NETMASK="255.255.254.0"
	GATEWAY="192.168.37.254"
	SUBNET=23

	HOST1=192.168.36.11
	HOST2=192.168.36.12
	TEST_HOST=192.168.36.99

	REPO_SRC=/mnt/hgfs/repo
	PROXY_SRC=/mnt/hgfs/proxy

elif [ $TYPE = "notebook" ]; then
	DEVICE=ens38 

	LOCAL=192.168.127.129
	NETMASK="255.255.255.0"
	GATEWAY="192.168.127.2"

	HOST1=192.168.127.11
	HOST2=192.168.127.12
	TEST_HOST=192.168.127.99
else
	echo "type nothing"
	sleep 5
fi

# echo $LOCAL

#############################################################################
REPO_HOST=$LOCAL
PROXY_HOST=$LOCAL

REPO_DST=/html
