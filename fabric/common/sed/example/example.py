# coding=utf-8

# import sys, os
# sys.path.append(os.path.join(os.getcwd(), "../.."))
import common.sed as sed

def prepare(file):
    path = os.path.join(os.getcwd(), os.path.join('files', file))
    c.run('\cp {} /tmp/{}'.format(path, file))
    sed.path(os.path.join('/tmp', file))


def kafka_config():
    index = 0
    host_port = '9092'
    zook_host = '{}:2128/kafka'.format(host.item(0, 'host'))

    """ 配置环境参数
           必须给出全路径，fabric 连接之后，进入的是 $HOME 目录
    """
    prepare('kafka.properties')
    sed.grep(**{'sep': '='})

    sed.update(c, "log.dirs", host.item(0, 'disk', ','))
    sed.update(c, "broker.id", str(int(index) + 1))
    sed.update(c, "zookeeper.connect", zook_host)

    sed.enable(c, "advertised.listeners", 'PLAINTEXT://{}:{}'.format(host.item(index, 'host'), host_port))
    sed.append(c, 'auto.create.topics.enable=false', '^group.initial.rebalance.delay.ms', grep={'prefix': ''})


def maven_config():
    prepare('maven.xml')

    sed.append(c, '''
    <mirror>
        <id>alimaven</id>
        <name>aliyun maven</name>
        <url>http://maven.aliyun.com/nexus/content/groups/public/</url>;
        <mirrorOf>central</mirrorOf>
    </mirror>''', '</mirrors>', pos=-1)

from common.init import *
c = Connection('127.0.0.1')

# kafka_config()
maven_config()