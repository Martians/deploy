#!/bin/bash

echo params：[$*]
export LANG=en_GB.utf8

# 第一次：更新配置文件
python3 fabric/docker/server.py

# 第二次：server安装
python3 fabric/docker/server.py $*