#!/bin/sh

###################################################################################################
echo "yum install ..."
sudo yum install -y bash-completion\
	net-tools.x64_64 vim tree yum-utils

#echo "yum disable fastestmirror"
#sudo sed -i "s/enabled.*/enabled=0/g" /etc/yum/pluginconf.d/fastestmirror.conf  

echo "yum update repos list to aliyun"
sudo mkdir /etc/yum.repos.d/save -p
sudo mv /etc/yum.repos.d/*.* /etc/yum.repos.d/save
sudo wget -O /etc/yum.repos.d/CentOS-Base-aliyun.repo http://mirrors.aliyun.com/repo/Centos-7.repo

echo "yum update cache"
sudo yum clean all
sudo yum makecache

###################################################################################################
echo "system: stop firewalld and selinux"
sudo systemctl stop firewalld.service
sudo systemctl disable firewalld.service
sudo setenforce 0
sudo sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
