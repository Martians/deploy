#!/bin/bash
#********************************************
#   Copyright (c) Beijing DaoWoo Times Technology Co., Ltd. 2016
#
#   Author      : Xianghan Li (lixianghan@daowoo.com)
#   FILE        : Check_YeeFS_env.sh
#   USAGE       : sh Check_YeeStor_install_env.sh
#   eg		: Check_YeeFS_env.sh -h
#   DESCRIPTION : This scripts is using befor install YeeFS package. 
#   REQUIREMENTS: 
#                 1) Must be run with root.   
#   HISTORY     :
#       2014/03/13 Xianghan LI written
#
#********************************************

yum -y install perl perl-Net-SSLeay perl-IO-Socket-SSL perl-Net-SMTP-SSL gcc python python-devel python-lxml python-paramiko libzip-devel rrdtool-devel\
        python-setuptools python-pip python-lxml NetworkManager e2fsprogs parted ethtool ntp psmisc smartmontools libaio nfs-utils net-tools

if [ -f ./depend/paramiko-1.16.0.tar.gz ]
then
    easy_install ./depend/paramiko-1.16.0.tar.gz
fi
if [ -f ./depend/pycrypto-2.6.1.tar.gz ]
then
    easy_install ./depend/pycrypto-2.6.1.tar.gz
fi
if [ -f ./depend/ecdsa-0.13.tar.gz ]
then
    easy_install ./depend/ecdsa-0.13.tar.gz
fi

#easy_install paramiko

error()
{
    key=$1
    er_name=$2
    case $key in
        101)
            echo -e "\033[40;31mNo such [ $er_name ] rpm package, please use yum install it ! \033[0m" 
            ;;
        102)
            echo -e "\033[40;31mNo such [ $er_name ] package, please use apt-get install it ! \033[0m" 
            ;;
	103)
	    echo -e "Short of Mem Error!"
	    ;;
        ?)
            ??
    esac
}

usage()
{
	cat <<-END >&2
Usage: ${0##*/} 
   eg: ${0##*/} 
END
exit $E_OPTERROR
}
[ $# -eq 0 ] || usage

flg=0
grep "Ubuntu" /etc/issue >> /dev/null 2>&1 
if [ $? -eq 0 ]
then
	for i in perl perl-Net-SSLeay perl-IO-Socket-SSL perl-Net-SMTP-SSL gcc python python-devel python-lxml python-paramiko libzip-devel rrdtool-devel python-setuptools python-pip NetworkManager e2fsprogs parted ethtool ntp psmisc smartmontools libaio nfs-utils net-tools 
	do
	    dpkg -l |grep $i >> /dev/null 2>&1 
		if [ $? -ne 0 ]
		then
			error 102 $i 
			flg=1
		fi
	done
else
	for i in python python-devel python-lxml python-setuptools python-lxml NetworkManager e2fsprogs parted ethtool ntp psmisc
	do
	    rpm -q $i >> /dev/null 2>&1 
		if [ $? -ne 0 ]
		then
			error 101 $i 
			flg=1
		fi
	done
fi

if [ $flg -eq 0 ]
then
	flg=0
else
        echo -e "Check Failed"	
	exit 1
fi

mem_total_MB=`free -m | grep Mem  | awk {'print $2'}`
min_free_kbytes=`sysctl -a | grep min_free_kbytes | awk {'print $3'} `

if [ "$mem_total_MB" -ge "6144" ]
then
    if [ "$min_free_kbytes" -lt "2048575" ] 
    then
        echo "vm.min_free_kbytes=2048576" > /etc/sysctl.conf
        sysctl -p
    fi
else
	error 103 $i
	flg=1
fi

if [ $flg -eq 0 ]
then
	echo -e "\033[40;32mCheck evn \t\t: Successful \033[0m"
else
        echo -e "Check Failed"	
	exit 1
fi
