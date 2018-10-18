#!/bin/sh

source ./base.sh $@

#docker-compose config
###############################################################
echo -e  "${GREEN_COLOR}-- start nfs -- ${RES}"
# will also start datanode
docker exec -it datanode /opt/hadoop-2.7.2/sbin/hadoop-daemon.sh --script bin/hdfs start portmap
docker exec -it datanode /opt/hadoop-2.7.2/sbin/hadoop-daemon.sh --script bin/hdfs start nfs3 

echo -e  "${GREEN_COLOR}-- mount client -- ${RES}"
sudo mkdir $NFS_MOUNT -p 
sudo mount -t nfs -o proto=tcp,nolock,noacl,sync 127.0.0.1:/ $NFS_MOUNT
