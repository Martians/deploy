#!/bin/sh
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

##############################################################################
echo "install service ..."

# yum remove fakesystemd -y
# yum install systemd -y
