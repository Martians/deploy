# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    """ 默认配置
    """
    def __init__(self):
        LocalBase.__init__(self, 'flink')
        # https://flink.apache.org/downloads.html
        self.source = 'http://mirrors.shu.edu.cn/apache/flink/flink-1.7.1/flink-1.7.1-bin-scala_2.11.tgz'


""" 提供个默认参数

    该变量定义在头部，这样在函数的默认参数中，也可以使用了
"""
local = LocalConfig()

@task
def install(c):
    c = hosts.one()
    download(c, local.name, source=local.source)
    copy_pack(c, dest=local.temp)

    system.install(0, 'java')
    hosts.execute('sudo rm -rf /opt/*{}*'.format(local.name))

    for index in hosts.lists():
        unpack(hosts.conn(index), local.name, path=package(local.temp))

    configure(c)


def configure(c):
    c = hosts.conn(0)
    conf = os.path.join(local.base, "conf")
    config_server()

    list = [host['host'] for host in hosts.lists(index=False, other=False)]
    c.run('echo "{}" > {}/slaves'.format('\n'.join(list), conf))

    sed.path(os.path.join(local.base, os.path.join(conf, "flink-conf.yaml")))
    sed.update(c, "jobmanager.rpc.address:", hosts.get(0)['host'])
    sed.update(c, "jobmanager.heap.size:", server.jobmanager.heap)

    sed.update(c, "taskmanager.heap.size:", server.taskmanager.heap)
    sed.update(c, "taskmanager.numberOfTaskSlots:", str(server.taskmanager.slot))

    sed.update(c, "parallelism.default:", str(server.parallelism))

    # if 'disk' in c.flink:
    #     sed.append(c, "taskmanager.tmp.dirs:", 'aabbcc')

    """ 从master复制到slave
    """
    copy_pack(c, conf, check=False, other=True)

@task
def start(c):
    c = hosts.conn(0)
    with c.cd(local.base):
        c.run(system.nohup('bin/start-cluster.sh'), pty=True)

@task
def stop(c, force=False):
    c = hosts.conn(0)
    with c.cd(local.base):
        c.run(system.nohup('bin/stop-cluster.sh'), pty=True)

    if force:
        system.process.kills('kafka')
        # system.stop('StandaloneSessionClusterEntrypoint')
        # system.stop('TaskManagerRunner')

@task
def clean(c):
    stop(c, True)

    system.clean('/opt/{}'.format(local.name))

@task
def help(c):
    c = conn(c, True)
    system.help(c, '''
    http://192.168.0.81:8081''')