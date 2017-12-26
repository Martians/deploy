#!/bin/sh

<<'COMMENT'
COMMENT

cd /etc/yum.repos.d/; mkdir -p save; mv *.repo save
curl -O http://mirrors.163.com/.help/CentOS7-Base-163.repo

yum makecache
yum install -y sudo vim net-tools telnet traceroute tree


echo "initialize complete ..."
