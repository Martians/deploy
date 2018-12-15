# coding=utf-8

import sys, os
sys.path.append(os.path.join(os.getcwd(), "../.."))

from fabric import Connection, SerialGroup as Group, Config
from invoke import task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed


class IgniteConfig:
    """ kafka 默认配置
    """
    def __init__(self):
        self.source = 'https://archive.apache.org/dist/ignite/2.6.0/apache-ignite-fabric-2.6.0-bin.zip'
        self.temp = '/tmp'

local = IgniteConfig()


def base(c):
    if 'base' not in c.install:
        parent = c.install.parent if 'parent' in c.install else default_config['install']['parent']
        c.install.base = os.path.join(parent, 'ignite')
    return c.install.base

@task
def prepare(c):
    hosts.execute('''yum install unzip java-1.8.0-openjdk-devel -y''', hide=None)
    # sed.append(c, 'export IGNITE_HOME=/opt/ignite', '', '/etc/profile')
    hosts.execute('''sudo echo export IGNITE_HOME={} >> /etc/profile'''.format(base(c)))

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
# install(c)