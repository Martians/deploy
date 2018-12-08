# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config, task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed


def base(c):
    if 'base' not in c.install:
        c.install.base = (c.install.path if c.install.path else '/opt') + '/redis'
    return c.install.base


""" 1. 准备 
        安装：fab install && fab cluster
        修改：fab clear && fab cluster （增加instance个数等）
        删除：fab clean
    
    2. 使用
        fab start stop stat
"""
@task
def install(c):
    c = hosts.conn(0)
    install_varify(c)
    install_master(c)
    install_slave(c)

@task
def cluster(c):
    stop(c)
    create_cluster(c)

    start(c)
    cluster_master(c)

    cluster_stat(c)

@task
def clear(c):
    hosts.execute('cd {path}; rm nodes.conf server.log -rf'
                  .format(path=base(c), base=c.install.cluster.directory))

    for index in range(1, c.install.cluster.instance):
        hosts.execute('cd {path}/{base}/{index}; rm nodes.conf server.log -rf'
                      .format(path=base(c), base=c.install.cluster.directory, index=index))
    stop(c)

@task
def clean(c):
    stop(c)
    hosts.execute('rm {path} -rf'.format(path=base(c)))

@task
def start(c):
    hosts.execute("cd {path}; redis-server redis.conf".format(path=base(c)))

    for index in range(1, c.install.cluster.instance):
        hosts.execute('cd {path}/{base}/{index}; redis-server redis.conf'
                      .format(path=base(c), base=c.install.cluster.directory, index=index))
    stat(c)

@task
def stop(c):
    hosts.execute("killall -9 redis-server", err=False)
    stat(c)

@task
def stat(c):
    hosts.execute("echo redis-server `ps aux | grep redis-server | grep -v 'grep' | wc -l`", out=True, hide=True)

########################################################################################################################


def install_varify(c):
    """ 如果已经安装，就拒绝
    """
    lists = []
    for index in hosts.lists():
        c = hosts.conn(index)
        if file_exist(c, base(c), dir=True):
            lists.append(hosts.get_host(index))

    for host in lists:
        print("path [{}] already exist on host [{}]".format(base(c), host['host']))

    if len(lists):
        print("{} host not empty, install failed, please clean first!".format(len(lists)))
        exit(-1)


def compile_redis(c):
    with c.cd(c.install.compile + '/redis'):
        if not file_exist(c, 'src', 'redis-server'):
            c.run("make MALLOC=libc -j5")

        c.run("mkdir -p {}".format(base(c)))
        with c.cd("src"):
            c.run("sudo \\cp redis-server redis-cli /usr/local/bin".format(""))
            c.run("sudo \\cp redis-server redis-cli ../redis.conf {}".format(base(c)))


def install_master(c):
    download(c, "redis", http=c.install.source, path=c.install.compile)
    compile_redis(c)
    config_master(c)


def config_master(c):
    file = base(c) + "/redis.conf"
    sed.update(c, "bind", "0.0.0.0", file=file)
    sed.update(c, "daemonize", "yes", file=file)
    sed.update(c, "logfile", "server.log", file=file)
    sed.update(c, "stop-writes-on-bgsave-error", "no", prefix=".*", file=file)

    sed.enable(c, "cluster-enabled", "yes", file=file)
    sed.enable(c, "cluster-config-file", "nodes.conf", prefix=".*", file=file)

    sed.disable(c, "save", ".*", file=file)


def install_slave(c):
    copy_slave(c, base(c))
    config_slave(c)


def config_slave(c):
    for index in hosts.lists(other=True):
        c = hosts.conn(index)
        with c.cd(base(c)):
            c.run("sudo \\cp redis-server redis-cli /usr/local/bin".format(""))

########################################################################################################################
def cluster_stat(c):
    c = hosts.conn(0)
    c.run("echo CLUSTER NODES | redis-cli -c -p 6379".format())
    c.run("echo CLUSTER INFO | redis-cli -c -p 6379 | grep cluster_size".format())

def cluster_master(c):
    # exec.multi(c, '''
    #     yum install ruby rubygems -y
    #     curl -sSL https://rvm.io/mpapis.asc | gpg2 --import -
    #     curl -L get.rvm.io | bash -s stable
    #     find / -name rvm -print
    #     source /usr/local/rvm/scripts/rvm
    #     rvm list known
    #     rvm install 2.4.1
    #     rvm use 2.4.1
    #     rvm use 2.4.1 --default
    #     ruby --version''')
    #
    # exec.multi(c, '''
    #     wget https://rubygems.org/downloads/redis-4.0.3.gem
    #     gem install -l redis-4.0.3.gem ''')
    lists = []
    for host in hosts.lists(index=False):
        lists.append("{}:{}".format(host['host'], 6379))

        for index in range(1, c.install.cluster.instance):
            lists.append("{}:{}".format(host['host'], (int(c.install.cluster.portbase) + index)))

    c.run("redis-cli --cluster create {} --cluster-replicas {}"
          .format(' '.join(lists), c.install.cluster.replica), pty=True, warn=True)


def create_cluster(c):
    temp = os.path.dirname(base(c)) + "/temp"
    hosts.execute('''
            mkdir -p {temp}; rm -rf {temp}/*
            mkdir -p {path}; rm -rf {path}/{base}
            '''.format(path=base(c), temp=temp,
                       base=c.install.cluster.directory))
    for index in range(1, c.install.cluster.instance):
        hosts.execute(''' 
          mkdir -p {temp}/{index}; cd {temp}/{index}
          cp {path}/redis.conf {temp}/{index}
          
          sudo sed -i "s#\(^port \).*#\\1{port}#g" redis.conf
          sudo sed -i "s#\(^pidfile [^0-9]*\)[0-9]*\([^0-9]\)#\\1{port}\\2#g" redis.conf
          '''.format(path=base(c), temp=temp,
                     base=c.install.cluster.directory, index=index,
                     port=(int(c.install.cluster.portbase) + index)))
    hosts.execute('''
            mv {temp} {path}/{base}
            '''.format(path=base(c), temp=temp,
                       base=c.install.cluster.directory))