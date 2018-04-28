#!/bin/bash
# https://docs.yugabyte.com/latest/deploy/multi-node-cluster/

## 配置
:<<COMMENT
echo "
export HOST1=100.1.1.10
export HOST2=100.1.1.11
export HOST3=100.1.1.12
export DISK1=/mnt/disk1
export DISK2=/mnt/disk2
export LOCAL=1" >> ~/.bashrc 
source ~/.bashrc

echo "
export TESTS=1
export SOURC=/source/nosql
export HOST1=192.168.10.111
export HOST2=192.168.10.112
export HOST3=192.168.10.113
export DISK1=/mnt/disk1
export DISK2=/mnt/disk2
export LOCAL=1" >> ~/.bashrc 
source ~/.bashrc

COMMENT

if [ ! $LOCAL ] || [ ! $HOST1 ] || [ ! $HOST2 ] || [ ! $HOST3 ]; then
	echo "should config: HOST1 HOST2 HOST3; LOCAL=1"
	exit -1
else
	echo "HOST1: $HOST1"
	echo "HOST2: $HOST2"
	echo "HOST3: $HOST3"
	echo "LOCAL: $LOCAL"
fi

dyn_var() {
	echo `eval echo '$'${1}`
}

# loop_wrapper prefix
loop_wrapper() {
	PREFIX=$1

	INDEX=1
	while [ $(dyn_var $PREFIX$INDEX) ]; do
		# echo "$(dyn_var $PREFIX$INDEX)"
		echo "$(dyn_var $PREFIX$INDEX)"
		((INDEX=INDEX + 1))
	done
}

# comb_wrapper prefix sep
comb_wrapper() {
	first=1
	for i in $(loop_wrapper $1); do
		if (( $first == 1 )); then
			first=0
		else
			echo -n $2
		fi
		echo -n $i
	done
}

# comb_wrapper prefix sep
exec_wrapper() {
	PREFIX=$1
	shift
	
	for i in $(loop_wrapper $PREFIX); do
		echo "$* $i"
	done
}

##################################################################################################
NAME=yugabyte
DEST=/opt/yugabyte


##################################################################################################
MASTER_PORT=7100
SERVER_PORT=9100
LOCAL_HOST=$(dyn_var HOST$LOCAL)

DISKS=$(comb_wrapper DISK ,)
HOSTS=$HOST1:$MASTER_PORT,$HOST2:$MASTER_PORT,$HOST3:$MASTER_PORT

##################################################################################################
# install_package name dest local_path, url
install_package() {
	local NAME=$1
	local DEST=$2
	local URLS=$3
	local LOCAL=$4
	BASE=$(dirname $DEST)

	# 文件在当前路径存在
	if [ -f $BASE/$NAME* ]; then
		echo "already download package"
		SOURCE=$BASE
	# 文件在local路径中存在
	elif [ -f $LOCAL/$NAME* ]; then
		echo "package in local source"
		SOURCE=$LOCAL
	else
		echo "download package"
		wget $URLS -P $BASE
		SOURCE=$BASE
	fi

	rm $DEST -rf
	tar zxvf $SOURCE/$NAME* -C $BASE
	[[ $BASE ]] && mv $BASE/$NAME* $DEST
}

if [ -d $DEST ]; then
	echo "already installed ..."
else
	echo "install ..."
	install_package $NAME $DEST https://downloads.yugabyte.com/yugabyte-ce-0.9.10.0-linux.tar.gz $SOURC
fi

if [[ ! "$TESTS" ]]; then
	sudo yum install -y epel-release ntp
fi

cd $DEST
./bin/post_install.sh

##################################################################################################
echo "clear data path ..."  
mkdir -p $DISK1 $DISK2
rm 	$DISK1/* $DISK2/* -rf

echo "configure ..."
echo -e "--master_addresses=$HOSTS \n--fs_data_dirs=$DISKS" > master.conf
echo -e "--tserver_master_addrs=$HOSTS \n--fs_data_dirs=$DISKS" > server.conf

echo -e "--rpc_bind_addresses=$LOCAL_HOST:$MASTER_PORT" >> master.conf
echo -e "--rpc_bind_addresses=$LOCAL_HOST:$SERVER_PORT" >> server.conf

echo "config bin path ..." 
echo "\$PATH=\$PATH:$PWD" >> ~/.bashrc
