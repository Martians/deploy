# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config
from invoke import Responder

from common.common import *
from common.install import *
from common.disk import *
import common.hosts as hosts
import common.sed as sed

########################################################################################################################
''' 如果已经安装，就拒绝
'''
def install_varify(c):
    lists = []
    for index in hosts.lists():
        c = hosts.conn(index)
        if file_exist(c, c.install.path, dir=True):
            lists.append(hosts.get_host(index))

    for host in lists:
        print("path [{}] already exist on host [{}]".format(c.install.path, host['host']))

    if len(lists):
        print("{} host not empty, install failed, please clean first!".format(len(lists)))
        exit(-1)

def compile_redis(c):
    with c.cd(c.install.compile):
        if not file_exist(c, 'src', 'redis-server'):
            c.run("make MALLOC=libc -j5")

        c.run("mkdir -p {}".format(c.install.path))
        with c.cd("src"):
            c.run("sudo \\cp redis-server redis-cli /usr/local/bin".format(""))
            c.run("sudo \\cp redis-server redis-cli ../redis.conf {}".format(c.install.path))


def install_master(c):
    download(c, "redis", c.install.source, c.install.compile)
    compile_redis(c)
    config_master(c)

def config_master(c):
    file = c.install.path + "/redis.conf"
    sed.update(c, "bind", "0.0.0.0", file=file)
    sed.update(c, "daemonize", "yes", file=file)
    sed.update(c, "logfile", "server.log", file=file)
    sed.update(c, "stop-writes-on-bgsave-error", "no", prefix=".*", file=file)

    sed.enable(c, "cluster-enabled", "yes", file=file)
    sed.enable(c, "cluster-config-file", "nodes.conf", prefix=".*", file=file)

    sed.disable(c, "save", ".*", file=file)

def install_slave(c):
    copy_slave(c, c.install.path)
    config_slave(c)

def config_slave(c):
    for index in hosts.lists(other=True):
        c = hosts.conn(index)
        with c.cd(c.install.path):
            c.run("sudo \\cp redis-server redis-cli /usr/local/bin".format(""))

def redis_clear(c):
    redis_stop(c)
    hosts.execute("rm -rf {}".format(c.install.path))

def redis_cluster(c):
    pass

########################################################################################################################

def redis_start(c):
    hosts.execute("redis-server {}/redis.conf".format(c.install.path))
    redis_stat(c)


def redis_stop(c):
    hosts.execute("killall -9 redis-server", err=False)
    redis_stat(c)


def redis_stat(c):
    hosts.execute("echo redis-server `ps aux | grep redis-server | grep -v 'grep' | wc -l`", output=True)

