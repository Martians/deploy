#!/bin/bash

touch /start.sh
chmod +x /start.sh

echo "params：[$*]"
export LANG=en_GB.utf8

# 第一次：更新配置文件
python3 fabric/docker/server.py

# 第二次：server安装
python3 fabric/docker/server.py $*

## 清理仓库
yum clean all; rm -rf /var/cache/yum/*

exit 0