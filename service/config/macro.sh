#!/bin/bash


#############################################################################
# 将最新的 source 目录挂载到 docker中
# 将最新的 docker 脚本目录挂载到 docker中
GLOBAL_MACRO="-v /home/long/source:/source -v /mnt/disk/docker:/docker"

SYSTMD="--privileged=true -v /sys/fs/cgroup:/sys/fs/cgroup"
INITIAL=/usr/sbin/init
