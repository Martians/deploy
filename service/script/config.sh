#!/bin/sh

DOMAIN="data.com"

<<'COMMENT'
DEVICE=ens33

LOCAL=192.168.36.10
NETMASK="255.255.254.0"
GATEWAY="192.168.37.254"
SUBNET=23

HOST1=192.168.36.11
HOST2=192.168.36.12
COMMENT

DEVICE=ens38 

LOCAL=192.168.127.129
NETMASK="255.255.255.0"
GATEWAY="192.168.127.2"
SUBNET=24

HOST1=192.168.127.11
HOST2=192.168.127.12

#############################################################################
BRIDGE=eth0m                        # 新增网桥





