# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config, task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed


def base(c):
    if 'base' not in c.install:
        parent = c.install.parent if 'parent' in c.install else default_config['install']['parent']
        c.install.base = os.path.join(parent, 'ignite')
    return c.install.base

@task
def prepare(c):
    hosts.execute('''yum install unzip java-1.8.0-openjdk-devel -y''', other=True, hide=None)
    # sed.append(c, 'IGNITE_HOME', '/opt/ignite', '/etc/profile')
    hosts.execute('''sudo echo export IGNITE_HOME={} >> /etc/profile'''.format(base(c)))

@task
def install(c):
    source = 'https://archive.apache.org/dist/ignite/2.6.0/apache-ignite-fabric-2.6.0-bin.zip'
    dest = "/tmp/{}".format(os.path.basename(source))

    download(c, 'ignite', source=source)
    master_copy(c, dest, async=False)

    hosts.execute('rm -rf /opt/*ignite*', other=True)
    for index in hosts.lists(other=True):
        unpack(hosts.conn(index), 'ignite', dest)

@task
def clean(c):
    hosts.execute('''rm -rf /opt/ignite''', hide=None)


c = hosts.conn(0)
# clean(c)
# prepare(c)
# install(c)