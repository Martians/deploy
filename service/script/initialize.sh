#!/bin/sh
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/script/config.sh
##############################################################################
# update repolist

source $BASE/script/repo.sh $@

##############################################################################
# update install
sudo yum clean all
sudo yum makecache 

[ $PRIORITY -a $PRIORITY == 1 ] && \
	yum install -y yum-plugin-priorities

echo "yum install ..."
yum install -y sudo net-tools telnet traceroute tree vim 

#bash-completion 

##############################################################################
echo "initialize complete ..."
