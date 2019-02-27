#!/bin/bash

## 安装python3
yum install wget -y

wget https://centos7.iuscommunity.org/ius-release.rpm
yum install ius-release.rpm -y
rm ius-release.rpm -rf

yum install python36u python36u-pip -y
ln -s /bin/python3.6 /bin/python3
ln -s /bin/pip3.6 /bin/pip3

## 删除python安装源
yum remove ius-release epel-release -y

## 修改pip源
mkdir ~/.pip
echo "[global]
# https://blog.csdn.net/testcs_dn/article/details/54374849
# index-url=https://pypi.tuna.tsinghua.edu.cn/simple
index-url=https://mirrors.aliyun.com/pypi/simple
" > ~/.pip/pip.conf

## 修改locale
conf=/etc/bashrc
echo 'export LANG=en_GB.utf8' >> $conf
source $conf

## 安装fabirc
python3 fabric/common/prepare.py pip3
rm ~/.cache/pip -rf

########################################################################################################################
## 安装更多

## 清理仓库
yum clean all; rm -rf /var/cache/yum/*

