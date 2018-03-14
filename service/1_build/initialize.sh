#!/bin/bash

##############################################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE_PATH

. 0_config/config.sh

##############################################################################
while getopts :r:ms opt
do
	case "$opt" in
	r) 	REPO=$OPTARG;;
	m)	MORE=$OPTARG;;
	s)	SERVICE=$OPTARG;;
	*) 	echo "Unknown option: $opt";;
esac
done

##############################################################################
## Repo
if [ "$REPO" ]; then
	# echo "use repo"
	. script/repo.sh $OPTARG
	if [ $? != 0 ]; then
		echo "set repo failed"
		exit $?
	fi
fi

##############################################################################
## System
. script/system.sh &&
	. script/common.sh

if [ $? != 0 ]; then
	echo "initialize system or common failed"
	exit $?
fi

##############################################################################
## More Script
if [ "$MORE" and -e "$MORE" ]; then
	echo "use More"
	. $MORE
	if [ $? != 0 ]; then
		echo "set more failed"
		exit $?
	fi
fi

##############################################################################
## Install service
. script/server/$SERVICE.sh

##############################################################################
## Clean
# update install
sudo yum clean all
sudo yum makecache 


##############################################################################
## Start srcipt
cp $BASE/script/server/start_$SERVICE.sh /start.sh




[ $PRIORITY -a $PRIORITY == 1 ] && \
	yum install -y yum-plugin-priorities

echo "yum install ..."
yum install -y sudo net-tools telnet traceroute tree vim 

#bash-completion 

##############################################################################
echo "initialize complete ..."

