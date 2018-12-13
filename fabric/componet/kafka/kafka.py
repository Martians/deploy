# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config
from invoke import task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed


def base(c):
    if 'base' not in c.install:
        parent = c.install.parent if 'parent' in c.install else default_config['install']['parent']
        c.install.base = os.path.join(parent, 'kafka')
    return c.install.base

@task
def install(c):
    source = 'http://mirror.bit.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz'
    temp = '/tmp'

    c = hosts.one()
    download(c, "kafka", source=source)
    copy_pack(c, dest=temp, async=True)

    hosts.execute('rm -rf /opt/*kafka*')
    for index in hosts.lists():
        unpack(hosts.conn(index), 'kafka', path=package(temp))

    configure(c)


def configure(c):

    file = os.path.join(base(c), "config/server.properties")
    for index in hosts.lists():
        c = hosts.conn(index)
        sed.update(c, "log.dirs", hosts.get_item(index, 'disk', ','), sep='=', file=file)
        sed.update(c, "broker.id", str(int(index) + 1), sep='=', file=file)
        sed.update(c, "zookeeper.connect", hosts.get_item(0, 'host') + ":2181", sep='=', more_sep=False, file=file)

        sed.enable(c, "advertised.listeners", 'PLAINTEXT://{}:9092'.format(hosts.get_item(index, 'host')),
                   sep='=', more_sep=False, file=file)
        sed.append(c, key='^group.initial.rebalance.delay.ms', data='auto.create.topics.enable=false', file=file)

@task()
def start(c):
    c = hosts.conn(0)
    with c.cd(base(c)):
        c.run('bin//start-cluster.sh'.format(), pty=True)

@task
def clean(c):
    hosts.execute('''rm -rf /opt/flink''', hide=None)


c = hosts.one()
configure(c)
