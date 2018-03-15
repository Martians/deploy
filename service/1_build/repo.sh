#!/bin/bash

#################################################################
file_output "repo.sh"
work_output "repo mask:  $REPO_MASK"
work_output "repo param: $@"

for repo in $@; do
	check=0

	# 检查 config.sh 中的 mask是否设置了，同时设置的选项，才能生效
	for mask in $REPO_MASK; do
		if [[ $repo == $mask ]]; then
			check=1
		fi
	done
	if [ $check -eq 1 ]; then
		case $repo in
			public) echo " - using repo: public"; REPO_PUBLIC=1;;
			local)	echo " - using repo: local";  REPO_LOCAL=1;;
			proxy)	echo " - using repo: proxy";  REPO_PROXY=1;;
			file)	echo " - using repo: file";   REPO_FILE=1;;
		esac
	fi
done

#################################################################
work_output "save old repo"
cd /etc/yum.repos.d/; 
mkdir -p save; mv *.repo save

#################################################################
## Public
if [[ $REPO_PUBLIC == 1 ]]; then
	work_output "set repo: public" 
	curl -O http://mirrors.163.com/.help/CentOS7-Base-163.repo
fi

#################################################################
## Local：network http sourcd
if [[ $REPO_LOCAL == 1 ]]; then
	work_output "set repo: local" 
	PRIORITY=1
	sudo rm /etc/yum.repos.d/local.repo -rf
cat << EOF | sudo tee -a /etc/yum.repos.d/local.repo
[local_network]
name=local network common repo
baseurl=http://$HOST_REPO/common/centos7/
gpgcheck=0
enabled=1
priority=1
# this repo not use proxy
proxy=_none_
EOF
fi

#################################################################
## Proxy：local netowrk proxy
if [[ $REPO_PROXY == 1 ]]; then
	work_output "set repo: proxy" 
	sudo sed -i "/cachedir/a\proxy=http://$HOST_PROXY:3142" /etc/yum.conf
fi

#################################################################
## File, only http server itself use
if [[ $REPO_FILE == 1 ]]; then
	work_output "set repo: file" 
	PRIORITY=1
	sudo rm /etc/yum.repos.d/file.repo -rf
cat << EOF | sudo tee -a /etc/yum.repos.d/file.repo
[local_file]
name=local file repository
baseurl=file://$DOCK_PATH_REPO/common/centos7/
gpgcheck=0
enabled=1
priority=1
# this repo not use proxy
proxy=_none_
EOF
fi
