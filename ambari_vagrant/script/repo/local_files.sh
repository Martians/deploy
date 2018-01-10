#!/bin/sh

sudo rm /etc/yum.repos.d/local_files.repo -rf
cat << EOF | sudo tee -a /etc/yum.repos.d/local_files.repo
[Local]
name=local file repository
baseurl=file:///vagrant/repo/common/centos7
gpgcheck=0
enabled=1
priority=1
proxy=_none_
EOF

