# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from fabric import Connection, SerialGroup as Group, Config
from invoke import task

from common import *


class IgniteConfig:
    """ 默认配置
    """
    def __init__(self):
        self.source = 'https://archive.apache.org/dist/ignite/2.6.0/apache-ignite-fabric-2.6.0-bin.zip'
        self.temp = '/tmp'


local = IgniteConfig()
name = 'ignite'

@task
def prepare(c):
    hosts.execute('''yum source unzip java-1.8.0-openjdk-devel -y''', hide=None)
    # sed.append(c, 'export IGNITE_HOME=/opt/ignite', '', '/etc/profile')
    hosts.execute('''sudo echo export IGNITE_HOME={} >> /etc/profile'''.format(base(name)))

@task
def install(c):
    c = hosts.one()
    download(c, "ignite", source=local.source)
    copy_pack(c, dest=local.temp, async=True)

    prepare(c)
    hosts.execute('sudo rm -rf /opt/*ignite*')

    for index in hosts.lists():
        unpack(hosts.conn(index), 'ignite', path=package(local.temp))

@task
def clean(c):
    hosts.execute('''rm -rf /opt/ignite''', hide=None)


c = hosts.conn(0)
# clean(c)
# prepare(c)
# source(c)