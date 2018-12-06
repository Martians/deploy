#!/bin/bash
#################################
PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

function rootness()
{
	if [ $EUID -ne 0 ]
	then
        	echo "Error:This script must be run as root!" 1>&2
        exit 1
	fi
}

function basic()
{

	#CentOS=7
	#YUM
#	mkdir -p /tmp/back
#	mv /etc/yum.repos.d/* /tmp/back
#	-bash: wget: command not found
#	wget -P /etc/yum.repos.d/ http://192.168.11.77/CentOS-local.repo
#	cp CentOS-local.repo /etc/yum.repos.d/
#	mv /tmp/back /etc/yum.repos.d/
#	yum clean all
#	yum makecache
	#Firewall
	systemctl stop firewalld.service
	systemctl disable firewalld.service
	#NetworkManager
	systemctl stop NetworkManager.service
	systemctl disable NetworkManager.service
	#Cpuspeed
	cpupower frequency-set -g performance
    chmod +x /etc/rc.local
}

# Core
function core()
{
	grep -q -w "ulimit -S -c unlimited" /root/.bashrc || sed -i -e'4a\ulimit -S -c unlimited' /root/.bashrc
	grep -q -w "ulimit -H -c unlimited" /root/.bashrc || sed -i -e'4a\ulimit -H -c unlimited' /root/.bashrc
	grep -q -w "ulimit -c unlimited" /root/.bashrc || sed -i -e'4a\ulimit -c unlimited' /root/.bashrc
	grep -q -w "kernel.core_pattern=/yfs/%e.%p.core" /etc/sysctl.conf || sed -i -e'4a\kernel.core_pattern=/yfs/%e.%p.core' /etc/sysctl.conf
	grep -q -w "fs.suid_dumpable = 2" /etc/sysctl.conf || sed -i -e'4a\fs.suid_dumpable = 2' /etc/sysctl.conf
	sed -i 's/#DefaultLimitCORE=/DefaultLimitCORE=infinity/g' /etc/systemd/system.conf
	echo "*       hard        core        unlimited" > /etc/security/limits.d/core.conf
	echo "*       soft        core        unlimited" >> /etc/security/limits.d/core.conf
	systemctl daemon-reload 
	systemctl daemon-reexec
	source /root/.bashrc
}

function swap()
{	
	swapoff -a
	if [ -z "`grep 'swapoff -a' /etc/rc.local`" ]
	then
       		echo "swapoff -a" >> /etc/rc.local
	fi
}

#timezone
function timezone()
{
   mv /etc/localtime /etc/localtime.old
   if [ -f "/usr/share/zoneinfo/Asia/Shanghai" ]; then
	  ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
   else
      echo "Can not find time zone [Asia/Shanghai], skip time zone update action!"
	  exit 1
   fi
}


#history
function History()
{
	if [ -z "`grep 'shopt -s histappend' /root/.bashrc`" ]
	then
	     echo "shopt -s histappend" >> /root/.bashrc
	     echo "PROMPT_COMMADN='history -a'" >> /root/.bashrc
	fi
	if [ -z "`grep 'export HISTTIMEFORMAT' /etc/profile`" ]
	then
	     echo "export HISTTIMEFORMAT=\"%Y/%m/%d %H:%M:%S  \"" >> /etc/profile
	fi
	
     # 2015-08-11: update time format for display	
	if [ -z "`grep 'export TIME_STYLE' /etc/profile`" ]
	then
	   echo "export TIME_STYLE='+%Y %m/%d %H:%M:%S' " >> /etc/profile 
	fi 
	
	if [ -z "`grep 'export TIME_STYLE' /root/.bashrc`" ]
	then
	   echo "export TIME_STYLE='+%Y %m/%d %H:%M:%S' " >> /root/.bashrc
	fi  
}


# Selinux
function selinux()
{
	if [ -s /etc/selinux/config ] && grep 'SELINUX=enforcing' /etc/selinux/config
	then
		sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
		setenforce 0
	fi
}


function ssh_repair()
{
	sed -i "s/#UseDNS\ yes/UseDNS\ no/g" /etc/ssh/sshd_config
	sed -i "s/GSSAPIAuthentication\ yes/GSSAPIAuthentication\ no/g" /etc/ssh/ssh_config
	systemctl restart sshd.service
}

function python_repair()
{
	yum -y install /root/prepare/python-*.rpm
}


rootness
basic
core
swap
timezone
selinux
History
ssh_repair
python_repair


yum -y install net-tools vim

cp accountlog.sh /etc/profile.d/
chmod +x /etc/profile.d/accountlog.sh
echo -e "\033[40;32m------Please reboot the machine!------\033[0m"
