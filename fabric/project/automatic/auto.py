# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config, task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed

""" 1. slave节点，与simplebench中，配置的节点个数保持一致
    2. 
"""

def base(c):
    if 'base' not in c.install:
        parent = c.install.parent if c.install.parent else fabric_config.install.parent
        c.install.base = os.path.join(parent, 'ignite')
    return c.install.base

@task
def install_prepare(c):
    hosts.execute('''yum install unzip java-1.8.0-openjdk.x86_64 -y''', master=False, hide=None)
    sed.append(c, 'IGNITE_HOME', '/opt/ignite', '/etc/profile')

@task
def install_ignite(c):
    download(c, 'ignite', source=c.install.source)
    master_copy(c, "/tmp/*ignite*.zip")

    hosts.execute('rm -rf /opt/*ignite*')
    for index in hosts.lists(other=True):
        download(hosts.conn(index), 'ignite', source=c.install.source)

@task
def install_script(c):
    c.run("mkdir -p {}".format(os.path.dirname(c.install.work)))
    if not file_exist(c, c.install.work, "", dir=True):
        git_url = 'http://gitlab.internal.nimblex.cn/guijichaxun/SimpleBenchmark'
        c.run("git clone {} {}".format(git_url, c.install.work), pty=True)

    copy_slave(c, c.install.work + "/scripts", '/opt/ignite/', other=False)

@task
def install_jars(c):

    with c.cd(c.install.work):
        c.run("mvn package")
        copy_slave(c, "target/*.jar", '/opt/ignite/libs', other=False)

@task
def install_total(c):
    install_prepare(c)

    install_ignite(c)

    install_script(c)
    install_jars(c)

@task
def clean(c):
    hosts.execute('''rm -rf /opt/ignite''', hide=None)


# install_total(hosts.conn(0))
# hosts.conn(1).run("echo $IGNITE_HOME", replace_env=False)
sed.append(hosts.conn(0), 'IGNITE_HOME', '/opt/ignite', '/etc/profile')