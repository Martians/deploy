#!/bin/sh

###################################################################################################
#echo "yum disable fastestmirror"
#sudo sed -i "s/enabled.*/enabled=0/g" /etc/yum/pluginconf.d/fastestmirror.conf  

echo "yum update cache"
sudo yum clean all
sudo yum makecache 

echo
echo "yum install ..."
sudo yum install -y yum-plugin-priorities

sudo yum install -y bash-completion\
	net-tools.x64_64 vim tree yum-utils