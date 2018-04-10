#!/bin/sh
source /vagrant/config/config.sh

REPO_LOCAL=repo.$DOMAIN
#REPO_LOCAL=$REPO_HOST

sudo rm /etc/yum.repos.d/local_network.repo -rf
cat << EOF | sudo tee -a /etc/yum.repos.d/local_network.repo
[common]
name=local network common repo
baseurl=http://$REPO_LOCAL/common/centos7/
gpgcheck=0
enabled=1
priority=1
proxy=_none_
EOF

sudo rm /etc/yum.repos.d/ambari.repo -rf
cat << EOF | sudo tee -a /etc/yum.repos.d/ambari.repo
[ambari-2.6.0.0]
name=local ambari repo
baseurl=http://$REPO_LOCAL/ambari/centos7/2.x/updates/2.6.0.0/
gpgcheck=0
enabled=1
priority=1
proxy=_none_
EOF

<<'COMMENT'
[hdp]
name=local hdp repo
baseurl=http://$REPO_LOCAL/component/HDP/centos7/2.x/updates/2.6.3.0/
gpgcheck=0
enabled=1
priority=1
proxy=_none_
EOF
COMMENT