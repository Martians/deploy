# coding=utf-8

# import sys, os
# sys.path.append(os.path.join(os.getcwd(), "../.."))

from invoke import task
from common import *
import system


class LocalConfig:
    """ 默认配置
    """
    def __init__(self):
        self.source = 'http://mirror.bit.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz'
        self.temp = '/tmp'

        self.port = 9092
        self.zook_host = hosts.get_item(0, 'host') + ":2181/kafka"
        self.zook_list = '--zookeeper {}'.format(self.zook_host)

        self.brok_host = ','.join(['{}:{}'.format(host['host'], self.port) for host in hosts.lists(index=False)])
        self.brok_list = '--broker-list ' + self.brok_host
        self.boot_list = '--bootstrap-server ' + self.brok_host

        self.group = 'local_group'
        self.topic = 'test'
        self.replica = 1
        self.partition = 1

        self.message = 'it is a message'


""" 提供个默认参数
    
    该变量定义在头部，这样在函数的默认参数中，也可以使用了
"""
local = LocalConfig()
name = 'kafka'

@task
def install(c):
    c = hosts.one()
    download(c, name, source=local.source)
    copy_pack(c, dest=local.temp, async=True)

    prepare(c)
    hosts.execute('sudo rm -rf /opt/*kafka*')

    for index in hosts.lists():
        unpack(hosts.conn(index), name, path=package(local.temp))

    configure(c)


def prepare(c):
    system.install(0, 'java', 'unzip')

@task
def configure(c):
    sed.path(os.path.join(base(name), "config/server.properties"))
    sed.grep(**{'sep': '='})

    for index in hosts.lists():
        c = hosts.conn(index)

        sed.update(c, "log.dirs", hosts.get_item(0, 'disk', ','))
        sed.update(c, "broker.id", str(int(index) + 1))
        sed.update(c, "zookeeper.connect", local.zook_host)

        sed.enable(c, "advertised.listeners", 'PLAINTEXT://{}:{}'.format(hosts.get_item(index, 'host'), local.port))
        sed.append(c, 'auto.create.topics.enable=false', '^group.initial.rebalance.delay.ms', grep={'prefix': ''})

        for disk in hosts.get_item(index, 'disk', ',').split(','):
            c.run("sudo mkdir -p {}".format(disk))

@task
def start(c):
    c = hosts.conn(0)
    c.run('cd {}; nohup bin/zookeeper-server-start.sh config/zookeeper.properties 1>zookeeper.log 2>&1 &'.format(base(name)))

    hosts.execute('cd {}; nohup bin/kafka-server-start.sh config/server.properties 1>/dev/null 2>&1 &'.format(base(name)))

@task
def stop(c):
    hosts.execute('cd {}; bin/kafka-server-stop.sh'.format(base(name)), hide=None, go_on=True)
    hosts.execute('cd {}; bin/zookeeper-server-stop.sh'.format(base(name)), hide=None, go_on=True)

@task
def clean(c):
    stop(c)
    # hosts.execute('killall -9 java', hide=None)
    hosts.execute('sudo rm -rf /opt/kafka', hide=None)
    hosts.execute('sudo rm -rf /tmp/zookeeper', hide=None)

    for index in hosts.lists():
        c = hosts.conn(index)

        for disk in hosts.get_item(index, 'disk', ',').split(','):
            c.run("sudo rm -rf {}/*".format(disk), pty=True)

""" fab kafka.topic -t desc
    fab kafka.topic -t create -o test1 -r 3 -p 10
    fab kafka.topic -t delete -o test1
"""
@task
def topic(c, type='desc', topic=local.topic, replica=local.replica, partition=local.partition):
    c = hosts.conn(0)
    with c.cd(base(name)):
        if type == 'create':
            c.run('''bin/kafka-topics.sh {} --create --topic {} --replication-factor {} --partitions {} '''
                  .format(local.zook_list, topic, replica, partition), pty=True)

        elif type == 'delete':
            c.run('''bin/kafka-topics.sh {} --delete --topic {}'''
                  .format(local.zook_list, topic), pty=True)
        else:
            # type == 'desc':
            c.run('bin/kafka-topics.sh {} --describe'.format(local.zook_list), pty=True)

@task
def stat(c, control=False):
    c = hosts.conn(0)
    shell = 'bin/zookeeper-shell.sh {}'.format(local.zook_host)
    if control:
        c.run("cd {base}; echo 'get /controller' | {shell}".format(base=base(name), shell=shell), pty=True)
    else:
        c.run("cd {base}; echo 'ls /brokers/ids' | {shell}".format(base=base(name), shell=shell), pty=True)


@task
def produce(c, message=local.message, topic=local.topic, count=1):
    c = hosts.conn(0)
    with c.cd(base(name)):
        for i in range(count):
            c.run('echo {} | bin/kafka-console-producer.sh {} --topic {}'.format(message, local.brok_list, topic), pty=True)


@task
def consume(c, topic=local.topic, group=local.group, touch=False):
    c = hosts.conn(0)
    with c.cd(base(name)):
        c.run('bin/kafka-console-consumer.sh {} --topic {} --consumer-property group.id={} {} {}'
              .format(local.boot_list, topic, group, '--from-beginning', '--max-messages 1' if touch else ''), pty=True)

@task
def group(c, type='desc', group=local.group):
    c = hosts.conn(0)
    with c.cd(base(name)):
        if type == 'desc':
            c.run('bin/kafka-consumer-groups.sh {} --describe --group {}'.format(local.boot_list, group), pty=True)
        else:
            c.run('bin/kafka-consumer-groups.sh {} --list'.format(local.boot_list), pty=True)

