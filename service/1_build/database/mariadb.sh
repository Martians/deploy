#!/bin/bash
# http://blog.csdn.net/pugu12/article/details/51241174

ROOT_PASS=111111
USER=long 
PASS=111111
TEST_TABLE=test_table

#######################################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

#rm /etc/httpd/conf.d/local.conf -rf
if [ $(set_file_flag /installed) -eq 1 ]; then
  echo "already install, just start"
  systemctl start mariadb
  exit
fi

#######################################################################
# http://mirrors.ustc.edu.cn/help/mariadb.html
cat << EOF | sudo tee -a /etc/yum.repos.d/mariadb.repo
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.2/centos7-amd64
gpgkey=http://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=0
EOF
sudo sed -i 's#yum\.mariadb\.org#mirrors.ustc.edu.cn/mariadb/yum#' /etc/yum.repos.d/mariadb.repo
sudo sed -i 's#http://mirrors\.ustc\.edu\.cn#http://mirrors.ustc.edu.cn#g' /etc/yum.repos.d/mariadb.repo

# 最新源中使用https，就要取消代理
#	或者将https转换成http，gpgcheck改成0
#sed -i "s/\(proxy\)/#\1/g" /etc/yum.conf 

yum -y install mariadb mariadb-server

echo "update config"
echo "update /etc/my.cnf"

# table name upper or lower is ok
sed -i "/\[mysqld]/a\lower_case_table_names=1" /etc/my.cnf

sed -i "/\[mysqld_safe]/i\init_connect='SET collation_connection = utf8_unicode_ci'" /etc/my.cnf
sed -i "/\[mysqld_safe]/i\init_connect='SET NAMES utf8'" /etc/my.cnf
sed -i "/\[mysqld_safe]/i\character-set-server=utf8" /etc/my.cnf
sed -i "/\[mysqld_safe]/i\collation-server=utf8_unicode_ci" /etc/my.cnf
sed -i "/\[mysqld_safe]/i\skip-character-set-client-handshake" /etc/my.cnf
sed -i "/\[mysqld_safe]/i\ " /etc/my.cnf

echo "update /etc/my.cnf.d/client.cnf"
sed -i "/\[client]/a\default-character-set=utf8" /etc/my.cnf.d/client.cnf

echo "update /etc/my.cnf.d/mysql-clients.cnf"
sed -i "/\[mysql]/a\default-character-set=utf8" /etc/my.cnf.d/mysql-clients.cnf

echo "start mariadb"
systemctl start mariadb
sleep 1

#######################################################################
echo "initial mariadb"
mysql_secure_installation <<EOF

y
$ROOT_PASS
$ROOT_PASS
n
n
y
y
EOF
# mysqladmin -u root password "new_password";

systemctl restart mariadb
#######################################################################

echo "create user: $USER"
mysql -u root -p$ROOT_PASS <<EOF
CREATE USER '$USER'@'%' identified by '$PASS';
GRANT ALL PRIVILEGES ON *.* TO '$USER'@'%';
GRANT ALL PRIVILEGES ON *.* TO '$USER'@'%';
FLUSH PRIVILEGES;

USE mysql;		-- check result
SELECT host, user, password FROM user;  
SHOW grants for '$USER'@'%';
EOF

echo "create table"
echo "create database $TEST_TABLE; show databases; \q;" | mysql -u root -p$ROOT_PASS

<<'COMMENT'
SHOW DATABASES: 
SHOW TABLES:
DESCRIBE user;
SHOW COLUMNS FROM runoob_tbl;
SHOW INDEX FROM runoob_tbl;
SHOW grants;
#GRANT ALL PRIVILEGES ON *.* TO '$USER'@'%' IDENTIFIED BY '$PASS' WITH GRANT OPTION;

echo "create database spotproject; show databases; \q;" | mysql -u root -p111111
mysql -u root -p111111 -Dspotproject < /root/import.sql
mysql -u root -p111111 <<EOF
use spotproject;
select * from t_car;
EOF
COMMENT

#######################################################################
set_file_flag /installed 1
