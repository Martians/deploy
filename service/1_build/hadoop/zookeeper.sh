#!/bin/sh

###################################################################################################
DOWNLOAD=http://mirror.bit.edu.cn/apache/zookeeper/zookeeper-3.5.2-alpha/zookeeper-3.5.2-alpha.tar.gz
PACKAGE=/source/component/
NAME=zookeeper

DEST=/opt/zookeeper
DATA=/var/lib/zookeeper

DOCKN=$1
INDEX=$2

###################################################################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

if [ $(set_file_flag /installed) -eq 1 ]; then
	echo "already install, just start"
	# systemctl start zookeeper.service
	$DEST/bin/zkServer.sh start
	exit
fi

###################################################################################################
if [[ $DEST == "" ]]; then
	DEST=/$NAME
fi

# 如果包不存在，就下载下来；通常这个目录是宿主机的Packge目录
if [ ! -f $PACKAGE/$NAME*.tar.gz ]; then
    mkdir -p $PACKAGE/
    yum install wget -y
    wget $DOWNLOAD -P $PACKAGE/
fi

if [ ! -f $PACKAGE/$NAME* ]; then
	echo "can't find file"
	exit
fi

# 安装必备软件, jvm 可以共享安装
yum install java-1.8.0-openjdk.x86_64 nc -y
###################################################################################################
echo "clear ..."
rm $DEST -rf
rm $DATA -rf
mkdir -p $DATA

echo "unpackage ..."
BASE=$(dirname $DEST)
tar zxvf $PACKAGE/$NAME* -C $BASE
mv $BASE/$NAME* $DEST
cd $DEST

###################################################################################################
echo "configure ..."
\cp $DEST/conf/zoo_sample.cfg $DEST/conf/zoo.cfg
# datadir 到 /var\/lib\/zookeeper
sed -i "s/\(dataDir=\).*$/\1\/var\/lib\/zookeeper/g" $DEST/conf/zoo.cfg

sh -c "echo '
server.1=$3:2888:3888
server.2=$4:2888:3888
server.3=$5:2888:3888' >> $DEST/conf/zoo.cfg"

echo "$INDEX" > $DATA/myid

###################################################################################################
# 设置启动方式
# useradd zookeeper
# chown -h zookeeper.  /opt/zookeeper
# chown -R zookeeper.  /opt/zookeeper/
# chown -R zookeeper.  /var/lib/zookeeper

# sh -c "echo '
# [Unit]
# Description=zookeeper.service
# After=network.target


# [Service]
# Type=forking
# User=zookeeper
# Group=zookeeper
# ExecStart=/opt/zookeeper/bin/zkServer.sh start
# ExecStop=/opt/zookeeper/bin/zkServer.sh stop
# ExecReload=/opt/zookeeper/bin/zkServer.sh restart
# WorkingDirectory=/var/lib/zookeeper


# [Install]
# WantedBy=multi-user.target
# '> /etc/systemd/system/zookeeper.service"
# systemctl restart zookeeper.service
$DEST/bin/zkServer.sh start

#######################################################################
set_file_flag /installed 1
