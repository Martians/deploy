#!/bin/bash

<<'COMMENT'
COMMENT

#################################################################
file_output "system.sh"
# step_output ""
# work_output ""
# yum clean all
# yum makecache 

#################################################################
yum install -y sudo vim net-tools telnet traceroute tree;  

#################################################################
# [ $PRIORITY -a $PRIORITY == 1 ] && \
# 	yum install -y yum-plugin-priorities
