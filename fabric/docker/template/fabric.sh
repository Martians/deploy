#!/bin/bash

## 安装python3
yum install epel-release wget -y

wget https://centos7.iuscommunity.org/ius-release.rpm
yum install ius-release.rpm -y
rm ius-release.rpm -rf

yum install python36u python36u-pip -y
ln -s /bin/python3.6 /bin/python3
ln -s /bin/pip3.6 /bin/pip3

## 修改pip源
mkdir ~/.pip
echo "[global]
index-url=https://pypi.tuna.tsinghua.edu.cn/simple
" > ~/.pip/pip.conf

## 修改locale
export LANG=en_GB.utf8

## 安装fabirc
python3 fabric/common/prepare.py pip3
rm ~/.cache/pip -rf

## 清理仓库
yum clean all; rm -rf /var/cache/yum/*d

