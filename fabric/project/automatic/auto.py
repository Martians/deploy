# coding=utf-8
import os

from fabric import Connection, SerialGroup as Group, Config, task

from common.init import *
from common.pack import *

import common.hosts as hosts
import common.sed as sed

def base(c):
    if 'base' not in c.install:
        parent = c.install.parent if c.install.parent else fabric_config.install.parent
        c.install.base = os.path.join(parent, 'ignite')
    return c.install.base

@task
def install(c):
    download(c, 'ignite', source=c.install.source)
    copy_slave(c, "/tmp/*ignite*.zip")

    for index in hosts.lists():
        download(hosts.conn(index), 'ignite', source=c.install.source)


def compile(c):
    c.run("mkdir -p {}".format(c.install.work))
    if not file_exist(c, c.install.work, "enchmark", dir=True):
        git_url = 'http://gitlab.internal.nimblex.cn/guijichaxun/SimpleBenchmark'
        c.run("git clone {} {}/benchmark".format(git_url, c.install.work), pty=True)

    c.run("mvn package")

install(hosts.conn(0))
# compile(hosts.conn(0))