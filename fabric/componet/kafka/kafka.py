# coding=utf-8

from invoke import task
from common import *
import system


class LocalConfig(LocalBase):
    """ 默认配置
    """
    def __init__(self):
        LocalBase.__init__(self, 'kafka')

        self.source = 'http://mirror.bit.edu.cn/apache/kafka/2.0.0/kafka_2.11-2.0.0.tgz'
        self.port = 9092
        self.zook_host = hosts.item(0, 'host') + ":2181/kafka"
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

@task
def install(c):
    c = hosts.one()
    download(c, local.name, source=local.source)
    copy_pack(c, dest=local.temp)

    prepare(c)
    hosts.execute('sudo rm -rf /opt/*{}*'.format(local.name))

    for index in hosts.lists():
        unpack(hosts.conn(index), local.name, path=package(local.temp))

    configure(c)


def prepare(c):
    system.install(0, 'java', 'unzip')

@task
def configure(c):
    sed.path(os.path.join(local.base, "config/server.properties"))
    sed.grep(**{'sep': '='})

    for index in hosts.lists():
        c = hosts.conn(index)

        sed.update(c, "log.dirs", hosts.item(0, 'disk', ','))
        sed.update(c, "broker.id", str(int(index) + 1))
        sed.update(c, "zookeeper.connect", local.zook_host)

        sed.enable(c, "advertised.listeners", 'PLAINTEXT://{}:{}'.format(hosts.item(index, 'host'), local.port))
        sed.append(c, 'auto.create.topics.enable=false', '^group.initial.rebalance.delay.ms', grep={'prefix': ''})

        for disk in hosts.item(index, 'disk', ',').split(','):
            c.run("sudo mkdir -p {}".format(disk))

@task
def start(c):
    c = hosts.conn(0)
    c.run('cd {}; nohup bin/zookeeper-server-start.sh config/zookeeper.properties 1>zookeeper.log 2>&1 &'.format(local.base))

    system.start('kafka.Kafka', 'cd {}; nohup bin/kafka-server-start.sh config/server.properties 1>/dev/null 2>&1 &'.format(local.base))

@task
def stop(c, force=False):
    c = hosts.conn(0)
    c.run('cd {}; bin/zookeeper-server-stop.sh'.format(local.base), hide=None, warn=True)

    system.stop('kafka', dir=local.base, exec='bin/kafka-server-stop.sh')

    if force:
        system.stop('kafka.Kafka')

@task
def clean(c):
    stop(c, True)

    system.clean('/opt/kafka, /tmp/zookeeper')

@task
def topic(c, type='desc', topic=local.topic, replica=local.replica, partition=local.partition):
    """ fab topic -t desc
        fab topic -t create -o test1 -r 3 -p 10
        fab topic -t delete -o test1
    """
    c = hosts.conn(0)
    with c.cd(local.base):
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
        c.run("cd {base}; echo 'get /controller' | {shell}".format(base=local.base, shell=shell), pty=True)
    else:
        c.run("cd {base}; echo 'ls /brokers/ids' | {shell}".format(base=local.base, shell=shell), pty=True)


@task
def produce(c, message=local.message, topic=local.topic, count=1):
    c = hosts.conn(0)
    with c.cd(local.base):
        for i in range(count):
            c.run('echo {} | bin/kafka-console-producer.sh {} --topic {}'.format(message, local.brok_list, topic), pty=True)


@task
def consume(c, topic=local.topic, group=local.group, touch=False):
    c = hosts.conn(0)
    with c.cd(local.base):
        c.run('bin/kafka-console-consumer.sh {} --topic {} --consumer-property group.id={} {} {}'
              .format(local.boot_list, topic, group, '--from-beginning', '--max-messages 1' if touch else ''), pty=True)

@task
def group(c, desc=False, group=local.group):
    """ fab group
        fab group -d -g local_group
    """
    c = hosts.conn(0)
    with c.cd(local.base):
        if desc:
            c.run('bin/kafka-consumer-groups.sh {} --describe --group {}'.format(local.boot_list, group), pty=True)
        else:
            c.run('bin/kafka-consumer-groups.sh {} --list'.format(local.boot_list), pty=True)

@task
def help(c):
    c = conn(c, True)
    system.help(c,'''
    fab install
    fab start
    
    fab topic -t create -o test1 -r 1 -p 1
    fab topic -o test1
    
    fab produce -t test1 -c 5
    fab consume -t test1 -g local
    fab group -d -g local''')

def maker(c):
    """ cluster copy
    ## config
    cp config/consumer.properties source.properties
    cp config/producer.properties target.properties


    # consumer
    # echo 'shallow.iterator.enable=false' >> source.properties
    group.id=mirror


    # producer
    echo '
#queue.enqueueTimeout.ms=-1
max.block.ms=600000
retries=10
' >> target.properties

    ## broker
    auto.create.topics.enable=true

    ## command
    bin/kafka-mirror-maker.sh --consumer.config source.properties --producer.config target.properties --num.streams 2 --whitelist=".*"

    ## 步骤
    source.properties：修改源集群的bootstrap.servers
    target.properties：修改目的集群的bootstrap.servers
    确保目的集群的配置，auto.create.topics.enable=true

    ## 执行
    设置--num.streams 为 consumer的线程数
    bin/kafka-mirror-maker.sh --consumer.config source.properties --producer.config target.properties --num.streams 2 --whitelist=".*"

    ## 查看
    设置为源集群的bootstrap-server
    bin/kafka-consumer-groups.sh --bootstrap-server 192.168.0.81:9092 --describe --group mirror

"""

# install(hosts.conn(0))
# start(hosts.conn(0))fab
# stop(hosts.conn(0))
# clean(hosts.conn(0))