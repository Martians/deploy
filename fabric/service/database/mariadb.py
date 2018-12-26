# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../../.."))

from invoke import task
from common.init import *

import common.hosts as hosts
import common.sed as sed
import system


class LocalConfig:
    def __init__(self):
        self.table = 'test'

        self.root_pasw = '111111'
        self.user = 'long'
        self.pasw = '111111'


local = LocalConfig()

@task
def install(c):
    """
        yum remove -y MariaDB-server MariaDB-client

        官网：https://mariadb.com/kb/en/library/yum/
        配置：https://www.cnblogs.com/lclq/p/5760966.html
    """

    c = conn(c)
    """ 更新源
    """
    c.run('''echo '
[mariadb]
name = MariaDB
baseurl=http://yum.mariadb.org/10.1/centos7-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=0' > /etc/yum.repos.d/mariadb.repo ''')
    c.run('''sed -i 's#yum\.mariadb\.org#mirrors.ustc.edu.cn/mariadb/yum#' /etc/yum.repos.d/mariadb.repo''')

    system.install(c, 'MariaDB-server MariaDB-client')

    configure(c)

    initialize(c)


def configure(c):
    """ 配置文件
    """
    c = conn(c)
    sed.path('/etc/my.cnf.d/server.cnf')
    sed.append(c, '''
init_connect="SET collation_connection = utf8_unicode_ci" 
init_connect="SET NAMES utf8"
character-set-server=utf8 
collation-server=utf8_unicode_ci 
skip-character-set-client-handshake''', '\[mysqld\]')

    sed.path('/etc/my.cnf.d/mysql-clients.cnf')
    sed.append(c, '''default-character-set=utf8''', '\[mysql\]')

    """ 初始化 root
    """
    c.run('systemctl restart mariadb')
    c.run('''mysql_secure_installation << EOF

y
{pasw}
{pasw}
n
n
y
y
EOF'''.format(pasw=local.root_pasw), pty=True)


def initialize(c):
    """ 添加用户
    """
    c = conn(c)
    c.run('''mysql -u root -p{root_pasw} << EOF
CREATE USER IF NOT EXISTS '{user}'@'%' identified by '{pasw}';
GRANT ALL PRIVILEGES ON *.* TO '{user}'@'%';
FLUSH PRIVILEGES;

USE mysql;		-- check result
SELECT host, user, password FROM user;  
SHOW grants for '{user}'@'%';
EOF'''.format(root_pasw=local.root_pasw, user=local.user, pasw=local.pasw, pty=True))

    """ 添加测试库
    """
    c = conn(c)
    c.run('''echo "create database {table}; show databases; \q;" | mysql -u root -p{root_pasw}'''
          .format(table=local.table, user=local.user, root_pasw=local.root_pasw), pty=True)

@task
def remove(c):
    c = conn(c)
    c.run('yum remove -y mariadb')