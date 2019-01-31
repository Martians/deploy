# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig:
    def __init__(self):
        self.table = 'test'
        self.user = 'postgres'
        self.pasw = '111111'
        self.data = '/var/lib/pgsql/9.5/data'


local = LocalConfig()

@task
def install(c):
    c = conn(c)

    system.install(c, 'postgresql95-server.x86_64 postgresql95-contrib.x86_64')
    c.run('''cat << EOF > /var/lib/pgsql/.pgsql_profile
export PGDATA={data}
export PATH=\$PATH:/usr/pgsql-9.5/bin
EOF'''.format(data=local.data))

    """ 初始化
    """
    c.run('''su - postgres <<EOF
source /var/lib/pgsql/.pgsql_profile 
rm /var/lib/pgsql/9.5/data -rf
echo "{pasw}" > /tmp/pwfile

initdb -U {user} --pwfile /tmp/pwfile
rm /tmp/pwfile -rf
EOF'''.format(user=local.user, pasw=local.pasw))

    configure(c)

    c.run('systemctl enable postgresql-9.5.service')
    c.run('systemctl start postgresql-9.5.service')


def configure(c):
    """ 配置文件
    """
    c = conn(c)

    """ 保存配置
    """
    c.run('\cp {conf}/postgresql.conf {conf}/postgresql.conf.save'.format(conf=local.data))
    c.run('\cp {conf}/pg_hba.conf {conf}/pg_hba.conf.save'.format(conf=local.data))

    sed.path(os.path.join(local.data, 'postgresql.conf'))

    sed.append(c, '''listen_addresses = '\\*' ''', '#listen_addresses', pos=-1)
    sed.append(c, '''port = 5432''', '#listen_addresses', pos=-1)

    sed.path(os.path.join(local.data, 'pg_hba.conf'))
    sed.append(c, '''host    all             all             0.0.0.0/0               md5''', '# Allow replication', pos=-1)

@task
def remove(c):
    c = conn(c)
    c.run('yum remove -y postgresql95-server.x86_64 postgresql95-contrib.x86_64')
    c.run("rm -rf {data}".format(data=local.data))

    """ psql -U user -d dbname
    """
@task
def start(c):
    c = conn(c)
    c.run('systemctl start postgresql-9.5.service')

@task
def stop(c):
    c = conn(c)
    c.run('systemctl stop postgresql-9.5.service')

@task
def stat(c):
    c = conn(c)
    c.run('systemctl status postgresql-9.5.service')

@task
def help(c):
    c = conn(c, True)
    system.help(c,'''
    psql -U postgres
    psql -U postgres -h 192.168.0.81 -p5432 [密码：111111]''')