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
        c.install.base = os.path.join(parent, 'kafka')
    return c.install.base

@task
def install(c):
    source = 'http://mirror.bit.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz'

    c = hosts.one()
    download(c, "kafka", source=source)
    copy_pack(c, package(), async=False)

    hosts.execute('rm -rf /opt/*kafka*', other=True)
    for index in hosts.lists(other=True):
        unpack(hosts.conn(index), 'kafka', dest)

    config(c)

def config(c):
    c = hosts.conn(0)

    conf = os.path.join(base(c), "conf")
    file = os.path.join(conf, "flink-conf.yaml")

    list = [host['host'] for host in hosts.lists(index=False, other=False)]
    c.run('echo "{}" > {}/slaves'.format('\n'.join(list), conf))


    sed.update(c, "jobmanager.heap.size:", c.flink.jobmanager.heap, file=file)

    sed.update(c, "taskmanager.heap.size:", c.flink.taskmanager.heap, file=file)
    sed.update(c, "taskmanager.numberOfTaskSlots:", str(c.flink.taskmanager.slot), file=file)

    sed.update(c, "parallelism.default:", str(c.flink.parallelism), file=file)

    # if 'disk' in c.flink:
    #     sed.append(c, "taskmanager.tmp.dirs:", 'aabbcc', file=file)
    master_copy(c, conf, async=False)


    sed.update(c, "broker.id=", hosts.get_host(0)['host'], file=file)

@task()
def start(c):
    c = hosts.conn(0)
    with c.cd(base(c)):
        c.run('bin//start-cluster.sh'.format(), pty=True)

@task
def clean(c):
    hosts.execute('''rm -rf /opt/flink''', hide=None)


c = hosts.one()
install(c)