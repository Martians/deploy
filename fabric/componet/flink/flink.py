# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    """ 默认配置
    """

    def __init__(self):
        LocalBase.__init__(self, 'flink')
        self.source = 'http://mirror.bit.edu.cn/apache/flink/flink-1.6.2/flink-1.6.2-bin-scala_2.11.tgz'


""" 提供个默认参数

    该变量定义在头部，这样在函数的默认参数中，也可以使用了
"""
local = LocalConfig()

@task
def install(c):
    c = hosts.one()
    download(c, local.name, source=local.source)
    copy_pack(c, dest=local.temp, async=True)

    system.install(0, 'java')
    hosts.execute('sudo rm -rf /opt/*{}*'.format(local.name))

    for index in hosts.lists():
        unpack(hosts.conn(index), local.name, path=package(local.temp))

    config(c)

def config(c):
    c = hosts.conn(0)

    conf = os.path.join(base(c), "conf")
    file = os.path.join(conf, "flink-conf.yaml")

    list = [host['host'] for host in hosts.lists(index=False, other=False)]
    c.run('echo "{}" > {}/slaves'.format('\n'.join(list), conf))

    sed.update(c, "jobmanager.rpc.address:", hosts.get(0)['host'], file=file)
    sed.update(c, "jobmanager.heap.size:", c.flink.jobmanager.heap, file=file)

    sed.update(c, "taskmanager.heap.size:", c.flink.taskmanager.heap, file=file)
    sed.update(c, "taskmanager.numberOfTaskSlots:", str(c.flink.taskmanager.slot), file=file)

    sed.update(c, "parallelism.default:", str(c.flink.parallelism), file=file)

    # if 'disk' in c.flink:
    #     sed.append(c, "taskmanager.tmp.dirs:", 'aabbcc', file=file)

    master_copy(c, conf, async=False)

@task()
def start(c):
    c = hosts.conn(0)
    with c.cd(base(c)):
        c.run('bin//start-cluster.sh'.format(), pty=True)

@task
def clean(c):
    hosts.execute('''rm -rf /opt/flink''', hide=None)

