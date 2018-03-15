#!/bin/bash
# http://blog.csdn.net/pugu12/article/details/51241174

ROOT_PASS=111111
USER=long 
PASS=111111
TEST_TABLE=test_table

CHECK_FILE=/executed
#######################################################################

#rm /etc/httpd/conf.d/local.conf -rf
if [ -f $CHECK_FILE ] && [ `more $CHECK_FILE` -eq 1 ]; then
  echo "already install, just start"
  systemctl start mariadb
  exit
fi

#######################################################################
#sh /docker/service/script/hadoop/mariadb.sh 
yum -y install mariadb mariadb-server

echo "update config"
echo "update /etc/my.cnf"
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
echo 1 > $CHECK_FILE