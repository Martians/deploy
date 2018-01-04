#!/bin/sh
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

source $BASE/script/config.sh
##############################################################################
# update repolist

echo "save old repo"
cd /etc/yum.repos.d/; mkdir -p save; mv *.repo save

for var in $@; do
	[ $var == "public" ] && REPO_PUBLIC=1
	[ $var == "local" ] && REPO_LOCAL=1
	[ $var == "proxy" ] && REPO_PROXY=1
	[ $var == "file" ]  && REPO_FILE=1
done 

# no argument or set public
if [ $# == 0 -o $REPO_PUBLIC -a $REPO_PUBLIC == 1 ]; then
	echo "set repo: public" 
	curl -O http://mirrors.163.com/.help/CentOS7-Base-163.repo
fi

if [ $REPO_LOCAL -a $REPO_LOCAL == 1 ]; then
	echo "set repo: local" 
	PRIORITY=1
	sudo rm /etc/yum.repos.d/local.repo -rf
cat << EOF | sudo tee -a /etc/yum.repos.d/local.repo
[local_network]
name=local network common repo
baseurl=http://$REPO_HOST/common/centos7/
gpgcheck=0
enabled=1
priority=1
# this repo not use proxy
proxy=_none_
EOF
fi

if [ $REPO_PROXY -a $REPO_PROXY == 1 ]; then
	echo "set repo: proxy" 
	sudo sed -i "/cachedir/a\proxy=http://$PROXY_HOST:3142" /etc/yum.conf
fi

if [ $REPO_FILE -a $REPO_FILE == 1 ]; then
	echo "set repo: file" 
	PRIORITY=1
	sudo rm /etc/yum.repos.d/file.repo -rf
cat << EOF | sudo tee -a /etc/yum.repos.d/file.repo
[local_file]
name=local file repository
baseurl=file://$REPO_DST/common/centos7/
gpgcheck=0
enabled=1
priority=1
# this repo not use proxy
proxy=_none_
EOF
fi
